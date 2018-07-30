#!/usr/bin/env python3
from model import Base, User, PetType, PetFamily
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect, flash
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

@app.route('/family/<int:f_id>/type/form')
def pet_type_form(f_id):
    return render_template('petTypeForm.html', f_id=f_id) 

@app.route('/type/<int:id>/edit-form')
def pet_type_edit_form(id):
    pet = PetType.get(id)
    if not pet:
        return ('', 404)
        
    return render_template('petTypeForm.html', pet=pet)

# Sorry for use this GET, but im very late on this curse
@app.route('/type/<int:id>/delete', methods=['GET'])
def delete_pet_type(id):
    pet = PetType.get(id)
    if not pet:
        return ('', 404)

    # Only owner can edit pet type    
    if pet.user_id != login_session['user_id']:
        flash('You should not be here.')
        return redirect('/')

    PetType.delete(pet)
    flash(pet.name + ' deleted!')
    return redirect('/')

@app.route('/type/<int:id>/edit', methods=['POST'])
def edit_pet_type(id):
    pet = PetType.get(id)
    if not pet:
        return ('', 404)

    # Only owner can edit pet type    
    if pet.user_id != login_session['user_id']:
        flash('You should not be here.')
        return redirect('/') 
        
    data = request.form

    # Validate required fields
    errors = {}
    if not data.get('name'):
        errors['name'] = 'Name is required'
    if not data.get('detail'):
        errors['detail'] = 'Detail is required'

    if len(errors.keys()):
        return (render_template('petTypeForm.html', 
                                errors=errors, 
                                pet=pet), 400)

    # Save pet type in db                                 
    try:
        PetType.update(pet, data['name'], data['detail'])
        return redirect('/')
    except Exception as e:
        flash(e)
        return (render_template('petTypeForm.html',
                                pet=pet), 422)                            

@app.route('/family/<int:f_id>/type/add', methods=['POST'])
def add_pet_type(f_id):
    data = request.form
    
    # Validate required fields
    errors = {}
    if not data.get('name'):
        errors['name'] = 'Name is required'
    if not data.get('detail'):
        errors['detail'] = 'Detail is required'    

    if len(errors.keys()):
        return (render_template('petTypeForm.html', 
                                errors=errors, 
                                pet=data, 
                                f_id=f_id
                                ), 400)

    # Save pet type in db                                 
    try:
        PetType.create(data['name'], data['detail'],
                       login_session['user_id'], f_id)
        return redirect('/')
    except Exception as e:
        flash(e)
        return (render_template('petTypeForm.html',
                                pet=data, 
                                f_id=f_id), 422)

@app.route('/family/<int:id>/type')
def pet_types(id):
    pets = PetType.list_by_family_id(id)
    if not pets:
        return ('', 404)
    
    family_name = pets[0].family.name
    return render_template('petTypes.html', pets=pets, family_name=family_name)                               

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
    user = User.get_or_create(info['name'], info['email'], info['picture'])

    #Set session variables
    set_login_session(info['name'], info['email'], info['picture'], 
                      user.id, credentials.access_token)
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
        clear_login_session()
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response   

def clear_login_session():
    del login_session['name']
    del login_session['picture']
    del login_session['email']
    del login_session['user_id']
    del login_session['access_token']

def set_login_session(name, email, picture, user_id, token):
    login_session['name'] = name
    login_session['picture'] = picture
    login_session['email'] = email
    login_session['user_id'] = user_id
    login_session['access_token'] = token

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