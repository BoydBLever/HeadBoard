from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User

class Posting:
    def __init__(self, data):
        self.id=data['id']
        self.time=data['time']
        self.lines_of_code=data['lines_of_code']
        self.favorite_algo=data['favorite_algo']
        self.explanation=data['explanation']
        self.dream_job=data['dream_job']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.user=None

    @classmethod
    def report_a_posting(cls, data):
        query = "INSERT INTO postings (time, lines_of_code, favorite_algo, explanation, dream_job, created_at, updated_at, user_id) VALUES (%(time)s, %(lines_of_code)s, %(favorite_algo)s, %(explanation)s, %(dream_job)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL("Headboard").query_db(query,data)
    
    @classmethod
    def get_all_postings(cls):
        query = "SELECT * FROM postings JOIN users ON users.id = postings.user_id;"
        results = connectToMySQL("Headboard").query_db(query)
        postings = []
        for items in results:
            posting=cls(items)
            user_data = {
                "id" : items["users.id"], 
                "github" : items["github"],
                "first_name" : items["first_name"],
                "last_name" : items["last_name"],
                "email" : items["email"],
                "password" : items["password"],
                "created_at" : items["users.created_at"],
                "updated_at" : items["users.updated_at"]
                }
            posting.user=User(user_data)
            postings.append(posting)
        return postings
    
    @classmethod
    def get_one_posting(cls, data):
        query = "SELECT * FROM postings JOIN users ON users.id = postings.user_id WHERE postings.id = %(id)s;"
        result = connectToMySQL("Headboard").query_db(query,data)
        print(result)
        posting = cls(result[0])
        user_data = {
            "id" : result[0]["users.id"], 
            "github" : result[0]["github"],
            "first_name" : result[0]["first_name"],
            "last_name" : result[0]["last_name"],
            "email" : result[0]["email"],
            "password" : result[0]["password"],
            "created_at" : result[0]["users.created_at"],
            "updated_at" : result[0]["users.updated_at"]
        }
        posting.user=User(user_data)
        return posting

    @classmethod
    def remove_posting(cls, data):
        query = "DELETE FROM postings WHERE id = %(id)s;"
        return connectToMySQL('Headboard').query_db(query,data)

    @classmethod
    def update_posting(cls, data):
        query = "UPDATE postings SET time = %(time)s, lines_of_code = %(lines_of_code)s, favorite_algo = %(favorite_algo)s, explanation = %(explanation)s, dream_job= %(dream_job)s  WHERE id = %(id)s;"
        return connectToMySQL('Headboard').query_db(query,data)

    @staticmethod
    def validate_posting(posting):
        is_valid = True
        if len(posting['time']) < 0:
            flash("Years coding: Input should be zero or greater.") 
            is_valid = False
        if len(posting['lines_of_code']) < 0:
            flash("Lines of code: Input should be zero or greater.")
            is_valid = False
        if len(posting['favorite_algo']) == 0:
            flash("Input missing: Favorite algorithm name.")
            is_valid = False
        if len(posting['explanation']) == 0:
            flash("Input missing: Why you like that algorithm or function.")
            is_valid = False
        if len(posting['dream_job']) == 0:
            flash("Input missing: Dream job.")
        return is_valid