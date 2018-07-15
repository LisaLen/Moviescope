from jinja2 import StrictUndefined

from flask import (Flask, request, render_template, redirect, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Review, Genre, MovieGenre
import datetime

app = Flask(__name__)

app.secret_key = 'ABC'

@app.route('/')
def open_singin_singup_page():
    '''Show SignIn/SignUp page'''

    return render_template('signin_signup.html')


@app.route('/sign-in', methods=["POST"])
def sin_in():
    '''Action for login form; log a user in'''

    login = request.form['login']
    password = request.form['password']
    print (password)

    #query to get user object using login
    user = User.query.filter_by(login=login).first()
    print(user)

    if user:
        if password == user.password:
            #fetchs user_id for loged-in user
            user_id = User.query.filter_by(login=login).one().user_id
            session['current_user'] = user_id
            fname = user.fname
            lname = user.lname
            flash (f'Logged in as {fname} {lname}' )
            return redirect('/homepage')
        else: 
            flash('Wrong password')
            return redirect('/')
    else: 
        flash ('Username doesn\'t exist')
        return redirect('/')

@app.route('/logout')
def logout():
    '''User log-out'''
    session.clear()

    return redirect('/')

@app.route('/sign-up', methods=['POST'])
def sign_up():
    '''Check is email exists in DB'''

    email = request.form['email']
    user = User.query.filter_by(email=email).first()
 
    if user is None:
        return render_template('new_user_registration.html', email=email)
    else:
        flash (f'Username with email: {email} already exists in databese')
        return redirect('/')


@app.route('/new-user-registration', methods=['POST'])
def register_new_user():

   
    login = request.form['login']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.args['email']

    new_user = User(login=login, password=password, 
                    fname=fname, lname=lname, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    flash('New user has been added. Please sign-in to continue')
    return redirect('/')

@app.route('/homepage')
def open_homepage():
    ''' Show homepage; show mivie list for a particular user'''
    if 'current_user' in session: 
                       
        #returns [(<Movie>, rating)]
        movies_ratings = db.session.query(Movie, Review.rating).join(Review).filter_by(user_id=session['current_user'])    

        return render_template('homepage.html', movies_ratings=movies_ratings)
    
    else: 
        return render_template('signin_signup.html')

@app.route('/add-movie')
def link_to_add_movie():
    ''' Show add_moview page'''

    return render_template('add_movie.html')


def create_new_movie(imdb_id, movie_url, imdb_rating, title, plot, release_date, poster_img):
    '''Create new movie row in DB, returns Movie object'''

    new_movie = Movie(imdb_id=imdb_id, 
                      movie_url=movie_url,
                      imdb_rating=imdb_rating,
                      title=title,
                      plot=plot,
                      usa_release_date=release_date,
                      poster_img=poster_img)

    print('###############################')
    print('\n')
    print('\n')

    print(new_movie)
    print('\n')

    print('\n')
    print('###############################')

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

    print('###############################')
    print('\n')
    print('\n')

    print(new_review)

    print('\n')

    print('\n')
    print('###############################')

    db.session.add(new_review)
    db.session.commit()

    return new_review

def create_movie_genres_connection(movie_id, genres):
    '''Takes list of genres and build connection with given movie_id'''

    #checking, if we have genres of new_movie in DB and fetching genre_id
    genres_tpl = db.session.execute('SELECT genre_title FROM genres').fetchall()
  

    for genre in genres:
        if (genre, ) not in genres_tpl: 

            #add new genre into Genres table
            new_genre = Genre(genre_title=genre)
            db.session.add(new_genre)
            db.session.commit()

        genre_id = Genre.query.filter_by(genre_title=genre).first().genre_id
        #create new relation genre_id for new_movie in Genres_Movies table
        new_movie_genre=MovieGenre(movie_id=movie_id, genre_id=genre_id)
        db.session.add(new_movie_genre)

    db.session.commit()
    print('movie - genre connection is created')




@app.route('/add-movie-to-journal')
def add_new_movie():
    '''Add new movie, rating and review into journal'''
    movie_title = request.args.get('title')
    imdb_id = request.args.get('imdbid')
    imdb_rating = request.args.get('imdb_rating')
    release_date = request.args.get('released')
    genres = request.args.get('genre').split(', ') #string with several genres; converting string to list
    plot = request.args.get('plot')
    movie_url = request.args.get('movie_url')
    poster_img = request.args.get('poster_img')
    rating = int(request.args.get('rating'))
    review = request.args.get('review')

    #review day is always current day
    date_review = datetime.date.today().strftime("%d-%b-%Y")

    print('###############################')
    print('\n')
    print('\n')

    print('\n')
    print (movie_title, imdb_id, imdb_rating, release_date, 
    genres, movie_url, plot, poster_img, rating, review, date_review)
    print('\n')
    print('\n')

    print('\n')

    print('\n')
    print('###############################')
    

    new_movie = create_new_movie(imdb_id, movie_url, imdb_rating,
                      movie_title, plot, release_date, poster_img)

    new_review = create_new_review(new_movie.movie_id, session.get('current_user'), review, rating, date_review)

    create_movie_genres_connection(new_movie.movie_id, genres)
     

    
    print('current user id', session.get('current_user'))

   
 

    flash ('movie was added')

    return redirect('/homepage')




if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
