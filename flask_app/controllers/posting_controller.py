from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.posting_model import Posting
from flask_app.models.user_model import User
#Saturday November 19, 2022 - Boyd B. Lever
@app.route('/dashboard')
def dashboard():
    #if the user is not logged in, they are redirected to login
    if not "user_id" in session:
        return redirect('/') 
    data = {
        "id" : session['user_id']
        }
    user = User.get_user_by_id(data) #users[0]
    postings = Posting.get_all_postings()
    return render_template('dashboard.html', user=user, postings=postings)

@app.route('/postings/new')
def newposting():
    data = {
        "id" : session['user_id']
        }
    user = User.get_user_by_id(data) #users[0]
    return render_template('newposting.html', user=user)

@app.route('/createposting', methods=['POST'])
def create_posting():
    
    if Posting.validate_posting(request.form):
        
        data = {
            "time":request.form['time'],
            "lines_of_code": request.form['lines_of_code'],
            "favorite_algo":request.form['favorite_algo'],
            "explanation":request.form['explanation'],
            "dream_job":request.form['dream_job'],
            "user_id":session['user_id']
        }
        Posting.report_a_posting(data)
        return redirect('/dashboard')
    else: 
        return redirect('/postings/new')

@app.route('/show/<int:id>')
def show(id):
    data = {
        "id": id
    }
    posting = Posting.get_one_posting(data)
    data2 = {
        "id" : session['user_id']
    }
    return render_template('show.html', posting=posting, user=User.get_user_by_id(data2))


@app.route('/posting/delete/<int:id>')
def delete(id):
    data = {
        "id": id
    }
    Posting.remove_posting(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    data = {
        "id" : session['user_id']
        }
    data2 = {
        "id" : id
    }
    user = User.get_user_by_id(data)
    posting = Posting.get_one_posting(data2)
    return render_template('edit.html', user=user, posting=posting)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    
    if Posting.validate_posting(request.form):

        data = {
            "time":request.form['time'],
            "lines_of_code": request.form['lines_of_code'],
            "favorite_algo":request.form['favorite_algo'],
            "explanation":request.form['explanation'],
            "dream_job":request.form['dream_job'],
            "id": id
        }
        Posting.update_posting(data)
        return redirect('/dashboard')
    else:
        return redirect(f'/edit/{id}')