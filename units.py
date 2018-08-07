import uuid
import hashlib
from model import connect_to_db, db, User, Movie, Review, Genre, MovieGenre, WishList

def hash_password(password):
    '''hashes password'''
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
 
def check_password(hashed_password, user_password):
    '''checks if entered password is the same as stored one'''
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def create_new_movie(imdb_id, movie_url, imdb_rating, title, plot, release_date, poster_img, genres):
    '''Create new movie row in DB, returns Movie object
       genres =[Genre1, Genre2...]'''

    #create instance of new movie
    new_movie = Movie(imdb_id=imdb_id, 
                      movie_url=movie_url,
                      imdb_rating=imdb_rating,
                      title=title,
                      plot=plot,
                      usa_release_date=release_date,
                      poster_img=poster_img,
                      genres= [])   

    #fetching existing genres in DB
    genres_tpl = db.session.query(Genre.genre_title).all()

    #adding new genres to DB and add all genres to new movie
    for genre in genres:
        if (genre, ) not in genres_tpl: 
            #create new genre object
            new_genre = Genre(genre_title=genre)

        else:
            #fetching genre object for genre existing in DB
            new_genre = Genre.query.filter_by(genre_title=genre).one()

        new_movie.genres.append(new_genre)
    db.session.add(new_movie)
    db.session.commit()
    return new_movie

def create_new_review(movie_id, user_id, review, rating, date_review):
    '''Creates new review row in DB, returns Review object'''

    new_review = Review(movie_id=movie_id,
                        user_id=user_id,
                        review=review,
                        rating=rating,
                        date_review=date_review)
    db.session.add(new_review)
    db.session.commit()
    return new_review
