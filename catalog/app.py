from model import Base, User
from flask import Flask, jsonify, request, url_for, abort, g, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from definitions import GOOGLE_SECRET
from flask import session as login_session

from flask_httpauth import HTTPBasicAuth
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

auth = HTTPBasicAuth()

engine = create_engine('postgresql:///catalog')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/g-plus-auth', methods = ['POST'])
def login():
    auth_code = request.json.get('auth_code')
    try:
        oauth_flow = flow_from_clientsecrets(GOOGLE_SECRET, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s&alt=json' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    userinfo_url =  "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    
    data = answer.json()

    name = data['name']
    picture = data['picture']
    email = data['email']

    user = session.query(User).filter_by(email=email).first()
    if not user:
        user = User(
            name =name,
            picture = picture, 
            email = email, )
        session.add(user)
        session.commit()

    login_session['username'] = name
    login_session['picture'] = picture
    login_session['email'] = email
    login_session['user_id'] = user.id

    return ('', 204)

if __name__ == '__main__':
    app.secret_key = 'nobody will try this'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)