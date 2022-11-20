from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id=data['id']
        self.github=data['github']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (github, first_name, last_name, email, password) VALUES (%(github)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("Headboard").query_db(query,data)  
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL("Headboard").query_db(query,data)
        
        if len(results) < 1:
            return False
        # results are a list of ojects
        user = cls(results[0])
        return user

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL("Headboard").query_db(query,data)
        users = []
        for user in results:
            users.append(cls(user))
        return users[0]

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len (user['github']) < 11:
            flash("Share your github account.")
        if len(user['first_name']) < 2:
            flash("Enter your real first name.") 
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Enter your real last name.")
            is_valid = False
        #email must have valid email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Problem with your email address.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password should be at least 8 characters long.")
            is_valid = False
        # password and confirm pw need to match
        if user['password'] != user['confirm_password']:
            flash("Password not confirmed.")
            is_valid = False
        # user cannot already exist in Headboard
        user_in_db = User.get_by_email(user)
        # user is not registered in the db
        if user_in_db:
            flash("Problem with email or password")
            is_valid = False
        # if len(User.get_by_email(user)) > 0: #create classmethod get_by_email
        #     flash("User already exists.")
        #     is_valid = False
        return is_valid
