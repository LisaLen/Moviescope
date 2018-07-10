# Models and database functions for Movie Journal project

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Models

class User(db.Model):
    '''Users of Movie-Journal app'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login = db.Column(db.String(68), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    fname = db.Column(db.String(32), nullable=True)
    lname = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        '''Provides helpful representation when printed'''
        return (f'<user_id = self.user_id>'
                f'<login = self.login>'
                f'<password = self.password>'
                f'<fname = self.fname>'
                f'<lname = self.lname>'
                f'<email = self.email>')

class Movie(db.Model):
    '''Movies saved in Movie-Journal app'''

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    imdb_id = db.Column(db.Integer, nullable=True)
    imdb_url = db.Column(db.String(150), nullable=True)
    imdb_rating = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(100), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    
    genres = db.relationship('Genre', 
                             secondary='movies_genres',
                             backref='movies')

    def __repr__(self):
        '''Provides helpful representation when printed'''
        return (f'< movie_id = self.movie_id>'
                f'<imdb_id = self.imdb_id>'
                f'<imdb_url = self.imdb_url>'
                f'<imdb_rating = self.imdb_rating>'
                f'<title = self.title>'
                f'<released_at = slf.released_at>')

class Review(db.Model):
    '''Users' reviews and ratings'''

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, 
                         db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), nullable=False)
    review = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    date_review = db.Column(db.DateTime, nullable=True)

    movie = db.relationship('Movie', backref='reviews')
    user = db.relationship('User', backref='reviews')



    def __repr__(self):
        '''Provides helpful representation when printed'''

        return (f'<review_id = self.review_id>'
                f'<movie_id = self.movie_id>'
                f'<user_id = self.user_id>'
                f'<review = self.review>'
                f'<rating = self.rating>'
                f'<date_review = self.date_review>')

class Genre(db.Model):
    '''Movie genres'''

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genge_title = db.Column(db.String(20), nullable=False)
    

    def __repr__(self):

        return (f'<genre_id = self.genre_id>'
                f'<genge_title = self.genge_title>'
                f'<movie_id = self.movie_id>')


class MovieGenre(db.Model):
    '''Association table for movies and genres'''

    __tablename__ = 'movies_genres'

    moviegenre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, 
                         db.ForeignKey('movies.movie_id'), nullable=False)
    genre_id = db.Column(db.Integer, 
                         db.ForeignKey('genres.genre_id'), nullable=False)

    def __repr__(self):
        return (f'<moviegenre_id = self.moviegenre_id>'
                f'<movie_id = self.movie_id>'
                f'<genre_id = self.genre_id>')




def connect_to_db(app):
    '''Connect the database to Flask app'''

    #Configure to use PostgreSQL DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///journal'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__== '__main__':
    '''For interactive mode to be able to work with db directly'''

    from server import app
    connect_to_db(app)
    print('Connected to DB')



