# import modules for rendering templates, message display, and url generation
from flask import render_template, url_for, flash, redirect

# import wtForm classes for registration and login forms
from project.forms import RegistrationForm, LoginForm, AddForm

# import app
from project import app

# import mysql db
from project import db

#import bcrypt
from project import bcrypt

#home page route
@app.route('/')
@app.route('/home')
def home():
    
    # set up db cursor
    mycursor = db.cursor()

    # run sample query for the homepage
    mycursor.execute("""SELECT userID, userName, userEmail FROM Users;""")
    data = mycursor.fetchall()
	
    # render the homepage template, passing data to display
    return render_template('home.html', data = data)

#about page route
@app.route('/about')
def about():
    return render_template('about.html')

#registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():

    # create registration form object
    form = RegistrationForm()

    # if registration form has been validly submitted
    if form.validate_on_submit():

        # hash the password that the user ended
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # set up db cursor
        mycursor = db.cursor()

        # run the query to add the user to the database
        query = f"INSERT INTO Users (userName, userEmail, userPW) VALUES ('{form.username.data}', '{form.email.data}', '{hashed_pw}');"
        mycursor.execute(query)

        # commit the query
        db.commit()

    	# display success message if user successfully registered
        flash(f'Your account has been created. Please login.', 'success')

        # render homepage
        return redirect(url_for('home'))

    # if no data has been submitted, display the registration page
    return render_template('register.html', title='Register', form = form)

#add page route
@app.route('/add', methods=['GET', 'POST'])
def add():

    # create add item form object
    form = AddForm()

    # if add itme form is validly submitted
    if form.validate_on_submit():

        # grab the type of item from the form
        value = dict(form.item.choices).get(form.item.data)

        # display success message (this is temporary)
        flash(f'You created a request for {value} to be provided by {form.dateNeeded.data}.', 'success')

        # redirect to the home page
        return redirect(url_for('home'))

    # if no data has been submitted, display the add item page
    return render_template('add.html', title='Make Your Request', form = form)

# login page route
@app.route('/login', methods=['GET', 'POST'])
def login():

    # create login form object
    form = LoginForm()

    # if login form has been validly submitted
    if form.validate_on_submit():

    	# display success message if user successfully logs in
    	if form.email.data == 'test' and form.password.data == 'password':
    		flash('You are now logged in!', 'success')

            # redirect tome page
    		return redirect(url_for('home'))

         # otherwise, display an error message   
    	else:
    		flash('Username and password combination not found. Please try again.', 'danger')

    # re-display the login page
    return render_template('login.html', title='Login', form = form)