#!/usr/bin/env python3
from model import Base, User, PetType, PetFamily
from flask import Flask, jsonify, request, url_for, abort, g, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from definitions import GOOGLE_SECRET
from flask import session as login_session
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import requests

auth = HTTPBasicAuth()
app = Flask(__name__)


@app.route('/')
def index():
    news = PetType.news()
    families = PetFamily.all()
    return render_template('home.html',
                           news=news,
                           families=families)

@app.route('/gconnect', methods = ['POST'])
def gconnect():
    # Obtain google authorization code
    auth_code = request.json.get('auth_code')

     # Upgrade the authorization code into a credentials object
    try:
        oauth_flow = flow_from_clientsecrets(GOOGLE_SECRET, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Check that the access token is valid.    
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s&alt=json' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get user info
    info = get_google_user_info(credentials.access_token)
    user = User.get_or_create(info.name, info.email, info.picture)

    login_session['name'] = info.name
    login_session['picture'] = info.picture
    login_session['email'] = info.email
    login_session['user_id'] = user.id
    login_session['access_token'] = credentials.access_token
    return ('', 204)

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response   

def get_google_user_info(access_token):
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    
    data = answer.json()

    return dict(name=data['name'],
                picture=data['picture'],
                email=data['email'])

if __name__ == '__main__':
    app.secret_key = 'nobody will try this'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)