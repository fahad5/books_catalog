from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Books, User
from flask import session as login_session
import random, string, json, httplib2, requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database
engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()




@app.route('/')
@app.route('/catalog')
def showCategories():
	categories = session.query(Category).all()
	global books 

	books = session.query(Books).all()

	return render_template('categories.html', categories = categories, books = books)


@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/items')
def showCategory(catalog_id):
	# Get all categories
	categories = session.query(Category).all()

	# Get category
	category = session.query(Category).filter_by(id = catalog_id).first()

	# Get Category name
	categoryName = category.name

	# Get all items for that category
	books = session.query(Books).filter_by(category_id = catalog_id).all()

	# Get count of category items
	CountBooks = session.query(Books).filter_by(category_id = catalog_id).count()

	return render_template('category.html', categories = categories, books = books, categoryName = categoryName, CountBooks = CountBooks)






@app.route('/catalog/add', methods=['GET', 'POST'])
def addCategoryItem():
	# Check if user is logged in
	if 'username' not in login_session:
	    return redirect('/login')

	if request.method == 'POST':
		if not request.form['name']:
			flash('Please add Book name')
			return redirect(url_for('addCategoryItem'))

		if not request.form['description']:
			flash('Please add a description')
			return redirect(url_for('addCategoryItem'))

		# Add category item
		newBook = Books(name = request.form['name'], description = request.form['description'], category_id = request.form['category'], user_id = login_session['user_id'])
		session.add(newBook)
		session.commit()

		return redirect(url_for('showCategories'))
	else:
		# Get all categories
		categories = session.query(Category).all()

		return render_template('addCategoryItem.html', categories = categories)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(catalog_id, item_id):
	# Check if user is logged in
	if 'username' not in login_session:
	    return redirect('/login')

	# Get category item
	book = session.query(Books).filter_by(id = item_id).first()

	# Get creator of item
	creator = getUserInfo(book.user_id)

	# Check if logged in user is creator of category item
	if creator.id != login_session['user_id']:
		return redirect('/login')

	# Get all categories
	categories = session.query(Category).all()

	if request.method == 'POST':
		if request.form['name']:
			book.name = request.form['name']
		if request.form['description']:
			book.description = request.form['description']
		if request.form['category']:
			book.category_id = request.form['category']
		return redirect(url_for('showCategoryItem', catalog_id = book.category_id ,item_id = book.id))
	else:
		return render_template('editCategoryItem.html', categories = categories, book = book)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(catalog_id, item_id):
	# Check if user is logged in
	if 'username' not in login_session:
	    return redirect('/login')

	# Get category item
	book = session.query(Books).filter_by(id = item_id).first()

	# Get creator of item
	creator = getUserInfo(book.user_id)

	# Check if logged in user is creator of category item
	if creator.id != login_session['user_id']:
		return redirect('/login')

	if request.method == 'POST':
		session.delete(book)
		session.commit()
		return redirect(url_for('showCategory', catalog_id = book.category_id))
	else:
		return render_template('deleteCategoryItem.html', book = book)

@app.route('/login')
def login():
	# Create anti-forgery state token
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state

	return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():

	if login_session['provider'] == 'google':
		gdisconnect()
		del login_session['gplus_id']
		del login_session['access_token']

	del login_session['username']
	del login_session['email']
	del login_session['picture']
	del login_session['user_id']
	del login_session['provider']

	return redirect(url_for('showCategories'))


@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def showCategoryItem(catalog_id, item_id):
	global books 
	# Get category item
	book = session.query(Books).filter_by(id = item_id).first()

	# Get creator of item
	creator = getUserInfo(book.user_id)


	return render_template('categoryItem.html', book = book, creator = creator)



def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate anti-forgery state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print ("Token's client ID does not match app's.")
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')

	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	login_session['provider'] = 'google'

	# See if user exists
	user_id = getUserID(data["email"])
	if not user_id:
	    user_id = createUser(login_session)
	login_session['user_id'] = user_id

	return "Login Successful"

@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user.
	access_token = login_session.get('access_token')

	if access_token is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] != '200':
	    # For whatever reason, the given token was invalid.
	    response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
	    response.headers['Content-Type'] = 'application/json'



@app.route('/catalog/json')
def catalogJSON():
    categories = session.query(Category).all()
    items = session.query(Books).all()
    return jsonify( Categories=[category.serialize for category in categories], Items=[item.serialize for item in items])


@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/items/JSON')
def itemsJSON():
    items = session.query(Books).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<path:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Books).filter_by(category=category).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<path:category_name>/<path:item_name>/JSON')
def ItemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Books).filter_by(name=item_name,category=category).first()
    return jsonify(item=[item.serialize])


if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super_secret_key'
	app.run(host = '0.0.0.0', port = 8888)