from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #Registration Validations
    if User.validate_user(request.form): #class method must be created
        print("Validation success")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
        data = {
        "github":request.form['github'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
        }
        #call the save @classmethod on User
        user_id = User.save(data) #class method is created
        #store user id into session
        session['user_id'] = user_id 
        return redirect('/dashboard')
    else:
        print("Validation fails")
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    #Login Authentications
    #see if the email provided exists in the database
    data = {
        "email" : request.form["email"]
        }
    user_in_db = User.get_by_email(data)

    #if user is not in the database
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['user_password']):
        flash("Invalid Email/Password")
        return redirect('/')
        # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
        #never render on a post
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#user controller can probably just be login / registration / logout
