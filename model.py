# Models and database functions for Moviescope project

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

#Models

class User(db.Model):
    '''Users of Moviescope app'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    fname = db.Column(db.String(32), nullable=True)
    lname = db.Column(db.String(40), nullable=True)
  

    # relationship with movies which are in wish list

    wishlist = db.relationship('Movie',
                                secondary='wishlists',
                                backref='users')

       
    def __repr__(self):
        '''Provides helpful representation when printed'''
        return (f'<user_id = {self.user_id}, '
                f'email = {self.email}, '
                f'password = {self.password}, '
                f'fname = {self.fname}, '
                f'lname = {self.lname}>')

class Movie(db.Model):
    '''Movies saved in Moviescope app'''

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True, )
    imdb_id = db.Column(db.String(10), nullable=True)
    movie_url = db.Column(db.String(150), nullable=True)
    imdb_rating = db.Column(db.Float, nullable=True)
    title = db.Column(db.String(100), nullable=False)
    plot = db.Column(db.Text, nullable=True)
    usa_release_date = db.Column(db.Date, nullable=True)
    poster_img = db.Column(db.String(150), nullable=False, default='N/A')
    
    genres = db.relationship('Genre', 
                             secondary='movies_genres',
                             backref='movies')

    #movie.users - shows list of users which wishlists contain this movie

    def __repr__(self):
        '''Provides helpful representation when printed'''
        return (f'< movie_id = {self.movie_id}, '
                f'imdb_id = {self.imdb_id}, '
                f'movie_url = {self.movie_url}, '
                f'imdb_rating = {self.imdb_rating}, '
                f'title = {self.title}, '
                f'usa_release_date = {self.usa_release_date},'
                f'poster_img = {self.poster_img}>')

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
    date_review = db.Column(db.Date, nullable=True)

    movie = db.relationship('Movie', backref='reviews')
    user = db.relationship('User', backref='reviews')



    def __repr__(self):
        '''Provides helpful representation when printed'''

        return (f'<review_id = {self.review_id}, '
                f'movie_id = {self.movie_id}, '
                f'user_id = {self.user_id}, '
                f'review = {self.review}, '
                f'rating = {self.rating}, '
                f'date_review = {self.date_review}>')

class Genre(db.Model):
    '''Movie genres'''

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_title = db.Column(db.String(20), nullable=False)
    

    def __repr__(self):

        return (f'<genre_id = {self.genre_id}, '
                f'genre_title = {self.genre_title}>')
                


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

class WishList(db.Model):
    '''user's wish list of movies - assisiation bable for user_id and movie_id in wish list'''

    __tablename__ = 'wishlists'

    wishlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, 
                         db.ForeignKey('movies.movie_id'), nullable=False)

    def __repr__(self):
        return (f'<wishlist_id = self.wishlist_id>'
                f'<user_id = self.user_id>'
                f'<movie_id = self.movie_id>')

def set_val_user_id():
        """Set value for the next user_id after seeding database - for testing purposes"""

        # Get the Max user_id in the database
        result = db.session.query(func.max(User.user_id)).one()
        #max_id = int(result[0])
      
        # Set the value for the next user_id to be max_id + 1
        query = "SELECT setval('users_user_id_seq', :new_id)"
        db.session.execute(query, {'new_id': 672})
        db.session.commit()

def set_val_user_id_test():
        """Set value for the next user_id after seeding database - for testing purposes"""

        # Get the Max user_id in the database
        result = db.session.query(func.max(User.user_id)).one()
        max_id = int(result[0])
      
        # Set the value for the next user_id to be max_id + 1
        query = "SELECT setval('users_user_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()


def example_data():
    """Create example data for the test database."""

    genre_test1 = Genre(genre_title='test_genre1')
    genre_test2 = Genre(genre_title='test_genre2')
    

    movie1 = Movie( imdb_id = 'tt0112462', movie_url = 'https://www.warnerbros.com/batman-forever',
                    imdb_rating=5.4, 
                    title='Batman Forever',
                    plot='''Batman must battle former district attorney Harvey Dent, who is 
                    now Two-Face and Edward Nygma, The Riddler with help from an amorous psychologist 
                    and a young circus acrobat who becomes his sidekick, Robin.''',
                    usa_release_date='2008-07-16',
                    genres=[genre_test1])

    movie2 = Movie( imdb_id='tt0109813', movie_url='https://www.facebook.com/TheFlintstonesMovie',
                    imdb_rating=4.8, 
                    title='The Flintstones',
                    plot='''In this live-action feature of the cartoon show, 
                    Fred Flintstone finally gets the job he's always wanted, but it may just come at a price.''',
                    usa_release_date='1994-05-27',
                    genres=[genre_test2])

    movie3 = Movie( imdb_id='tt0109854', movie_url='TestURL',
                    imdb_rating=3, 
                    title='Full Cycle',
                    plot='''TestPlot3''',
                    usa_release_date='1994-11-27',
                    genres=[genre_test1, genre_test2])

    movie4 = Movie( imdb_id='tt0145678', movie_url='TestURL4',
                    imdb_rating=10, 
                    title='WorkingTitle',
                    plot='''TestPlot4''',
                    usa_release_date='1981-05-27',
                    genres=[genre_test1, genre_test2])

    user1 = User(user_id=1, email='testemail1@gmail.com', password='123', fname='Test1', lname='Supertest1', wishlist=[movie3, movie4])
    user2 = User(user_id=2, email='testemail2@gmail.com', password='456', fname='Test2', lname='Supertest2')
  

    review1 = Review(movie=movie1,
                      user =user1,                   
                      review ='I don\'t really like it',
                      rating = 3)
    review2 = Review(movie=movie2,
                      user =user1,                   
                      review ='It\s funny, but too old',
                      rating = 4)
    review3 = Review(movie=movie1,
                      user =user2,                   
                      review ='Supper cool',
                      rating = 5)
    review4 = Review(movie=movie2,
                      user =user2,                   
                      review ='boring',
                      rating = 1)

    
    db.session.add_all([user1, user2, movie1, movie2, movie3, movie4])
    db.session.add_all([review1, review2, review3, review4, genre_test1, genre_test2])
    db.session.commit()

    set_val_user_id_test()



def connect_to_db(app, db_uri="postgresql:///journal"):
    '''Connect the database to Flask app'''

    #Configure to use PostgreSQL DB
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__== '__main__':
    '''For interactive mode to be able to work with db directly'''

    from server import app
    connect_to_db(app)
    print('Connected to DB')

    # db.create_all()
#to stay inline with user IDs of Recombee.com db
    # query = "SELECT setval('users_user_id_seq', :new_id)"
    # db.session.execute(query, {'new_id': 671})
    



