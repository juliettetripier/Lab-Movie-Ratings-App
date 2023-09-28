"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


# Functions start here!

if __name__ == '__main__':
    from server import app
    connect_to_db(app) 


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title, 
                  overview=overview, 
                  release_date=release_date, 
                  poster_path=poster_path)
    return movie


def all_movies():
    return Movie.query.all()


def get_movie_by_id(movie_id):
    return Movie.query.get(movie_id)


def get_movie_by_title(movie_title):
    return Movie.query.filter_by(title=movie_title).first()


def all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_rating(user_id, movie, score):
    """Create and return a rating"""
    user = get_user_by_id(user_id)
    rating = Rating(user=user, movie=movie, score=score)
    return rating

def get_user_by_email(email):
    user = User.query.filter(email == User.email).first()
    return user