"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies')
def get_movies():
    list_of_movies = crud.all_movies()
    return render_template('/all_movies.html', list_of_movies=list_of_movies)

@app.route('/movies/<movie_id>')
def movie_detail(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def show_profile():
    user_list = crud.all_users()
    return render_template('all_users.html', user_list=user_list)

@app.route('/users/<user_id>')
def user_detail(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users', methods=["POST"])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:
        flash('A user with that email already exists. Please try again.')
    else:
        db.session.add(crud.create_user(email, password))
        db.session.commit()
        flash('Your account was successfully created.')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:
        if password == user.password:
            session['user'] = user.user_id
            flash('Logged in!')
            return redirect('/')
        else: 
            flash('Wrong password :(')
            return redirect('/')
    else:
        flash('There is no user with this email.')
        return redirect('/')

@app.route('/rate-movie', methods=['POST'])
def add_rating():
    if session['user']:
        rating = request.form.get('rating')

        movie_title = request.form.get('movie_title')
        movie = crud.get_movie_by_title(movie_title)

        new_rating = crud.create_rating(session['user'], movie, rating)

        db.session.add(new_rating)
        db.session.commit()

        flash(f"Your rating has been added to {movie_title}!")
        return redirect('/movies')
    else:
        flash("Please log in before submitting a rating.")
        return redirect('/movies')


    
# steps:

# - make form in movie_details.html
#     post request
#     action goes to flask route
#     use dropdown menu 1-5
#     submit


# in server.py:

#     make route

#     check if user logged in
#         get rating info out of post request
#         create instance of Rating class
#         add + commit rating to db
#         flash rating confirmation
#         redirect to movie details page
#     else:
#         flash('please log in') message
#         redirect to homepage


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

