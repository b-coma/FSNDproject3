from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, User, Category, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import datetime
from sqlalchemy import Column, Integer, DateTime

app = Flask(__name__)

# forget this line and you get a weird 'file not found' error for the JSON
CLIENT_ID = json.loads(
    open('/vagrant/catalog/client_secrets.json', 'r').read(
        ))['web']['client_id']
APPLICATION_NAME = "Catalog App"

#  Connect to Database and create database session
engine = create_engine('sqlite:///catalog3.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#  Create anti-forgery state token.  This adds security.
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# this is quite a lengthy connect procedure to authenticate with
# Google OAuth.  This was difficult, and in retrospect I'd recommend
# going with Facebook or some other 3rd party
# MUCH of the gconnect method was adapted from the Udacity lesson
# on Google OAuth
@app.route('/gconnect', methods=['POST'])
def gconnect():
    #  if the tokens don't match, weird stuff is going on
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #  Obtain authorization code
    code = request.data

    try:
        # had to use absolute path here for the file and i'm not sure why
        oauth_flow = flow_from_clientsecrets(
            '/vagrant/catalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    # catch errors
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Check that the access token is valid.
    access_token = credentials.access_token
    # here's the url for OAuth
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # send the request
    result = json.loads(h.request(url, 'GET')[1])
    # hope this works, if not, forget it (catch error)
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check the result against the user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # we're matching client id against token id, although if they don't match
    # then it would be ultra fishy
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # store the access token
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # put the access token in the session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # grab the interesting stuff - email, name, picture
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # bind the DB to add user
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # if user does not exist in db, add it
    if (session.query(User).filter_by(
            email=login_session['email']).count() < 1):
        newUser = User(email=login_session['email'])
        session.add(newUser)
        session.commit()

    # display this to the user
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: '
    output += '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Disconnect from google OAuth.  There is weirdness with logging out
# if you are connected in another tab.  don't do that.
# MUCH of the gdisconnect method was adapted from the Udacity lesson
# on Google OAuth
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is ' + access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url += login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#  Display all items in db
@app.route('/')
@app.route('/items/')
def showItems():
    # need to add this for every procedure with DB interaction,
    # otherwise we get a thread error
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # grab email from session IF it is there
    email = login_session.get('email')
    if email is None:  # no session, not logged in
        user_id = 0
    else:
        # see if user exists
        if (session.query(User).filter_by(
                email=login_session['email']).count() < 1):
            user_id = 0
        else:  # if user exists in db, grab ID for compare
            user = session.query(User).filter_by(email=email).one()
            user_id = user.id
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.date_added.desc()).all()
    return render_template(
        'allItems.html', categories=categories, items=items, user_id=user_id)

#  Display info on one individual item at a time
@app.route('/items/<int:item_id>/')
def showOneItem(item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # if user is logged in and in DB, send ID, otherwise 0
    email = login_session.get('email')
    if email is None:
        user_id = 0
    else:
        user = session.query(User).filter_by(email=email).one()
        user_id = user.id
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    return render_template(
        'showItem.html', item=item, category=category, user_id=user_id)


@app.route('/items/category/<int:category_id>/')
def showCategory(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    email = login_session.get('email')
    if email is None:
        user_id = 0
    else:
        user = session.query(User).filter_by(email=email).one()
        user_id = user.id
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return render_template(
        'showCategory.html',
        items=items,
        category=category,
        user_id=user_id)


#  Create new category
@app.route('/items/category/new/', methods=['GET', 'POST'])
def newCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        # added authentication check per review feedback
        # can't create new category if not logged in
        if 'username' not in login_session:
            return redirect(url_for('showLogin'))
        # create new category in DB and redirect to showItems on submit
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showItems'))
    else:
        return render_template('newCategory.html')

#  Create new item
@app.route('/items/<int:category_id>/newItem/', methods=['GET', 'POST'])
def newItem(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # added authentication check per review feedback
    # can't create new item if not logged in
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        # add new item to db complete with all info including
        # user who created it
        user = session.query(User).filter_by(
            email=login_session['email']).one()
        newItem = Item(
                name=request.form['name'],
                description=request.form['description'],
                category_id=category_id,
                date_added=datetime.datetime.utcnow(),
                user_id=user.id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newItem.html')

#  Edit item page
@app.route('/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # added authentication check per review feedback
    # can't edit an item if not logged in
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    itemToEdit = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        # update name and/or desc if they were updated in the form
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('showOneItem', item_id=item_id))
    else:
        # add this for authorization check
        email = login_session.get('email')
        if email is None:
            user_id = 0
        else:
            user = session.query(User).filter_by(email=email).one()
            user_id = user.id
        return render_template(
            'editItem.html', item=itemToEdit, user_id=user_id)

#  Delete item page
@app.route('/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # added authentication check per review feedback
    # can't delete an item if not logged in
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    # find item in order to delete it
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems'))
    else:
        # add this for authorization check
        email = login_session.get('email')
        if email is None:
            user_id = 0
        else:
            user = session.query(User).filter_by(email=email).one()
            user_id = user.id
        return render_template(
            'deleteItem.html', item=itemToDelete, user_id=user_id)

# JSON Endpoint for one specific item in db
@app.route('/items/<int:item_id>/JSON')
def itemJSON(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


# JSON Endpoint for all items in db
@app.route('/items/JSON')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])

# JSON endpoint for all users in DB.  useful for debug
@app.route('/items/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(users=[u.serialize for u in users])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
