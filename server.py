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

    if not session.get('current_user'): 
        return render_template('signin_signup.html')
    else:
        return redirect('/homepage')

   

@app.route('/sign-in', methods=['GET', 'POST'])
def sin_in():
    '''Action for login form; log a user in'''
    if request.method == 'POST':
        
        login = request.form['login']
        password = request.form['password']
        
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
    else:
        return redirect('/homepage')

@app.route('/logout')
def logout():
    '''User log-out'''
    session.clear()
    user = User.query.filter_by(login=login).one()
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
                       
        #returns [(<Movie>, <Review>)]
        movies_reviews = db.session.query(Movie, Review).join(Review).filter_by(user_id=session['current_user']).all()  
        print('###############################')
        print('\n')
        print('\n')

        print(movies_reviews)
        print('\n')

        print('\n')
        print('###############################')

        return render_template('homepage.html', movies_reviews=movies_reviews)
    
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

    # print('###############################')
    # print('\n')
    # print('\n')

    # print(new_movie)
    # print('\n')

    # print('\n')
    # print('###############################')

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

    # print('###############################')
    # print('\n')
    # print('\n')

    # print(new_review)

    # print('\n')

    # print('\n')
    # print('###############################')

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


@app.route('/check-imdbid-indb')
def chek_if_movie_in_journal():
    '''Checks if selected movie in current_user's journal. 
    Returns True if movie is in current_user's journal '''

    imdb_id = request.args.get('imdb_id')
    print('###############################')
    print('\n')
    print('\n')
    print('\n')
    print('imdb_id', imdb_id)
    print('\n')
    print('\n')
    print('\n')
    print('query', db.session.query(Movie).join(Review).filter(User.user_id==session.get('current_user'), Movie.imdb_id==imdb_id).first())
    print('###############################')


    if db.session.query(Movie).join(Review).filter(User.user_id==session.get('current_user'), Movie.imdb_id==imdb_id).first():
        return 'True' 
    return 'False'   

@app.route('/add-movie-to-journal')
def add_new_movie():
    '''Add new movie, rating and review into journal'''

    #get all imdb_ids from DB, it returns [(imdb_id, ).....]
    imdb_id = request.args.get('imdbid')
    movie_title = request.args.get('title')
    
    if not Movie.query.filter_by(imdb_id=imdb_id).first():
        #if given imdb_id doesn't exist in DB, then create new_movie in DB
        imdb_rating = request.args.get('imdb_rating')
        release_date = request.args.get('released')
        
        plot = request.args.get('plot')
        movie_url = request.args.get('movie_url')
        poster_img = request.args.get('poster_img')
        # print('###############################')
        # print('\n')
        # print('\n')

        # print('\n')
        # print (movie_title, imdb_id, imdb_rating, release_date, 
        # movie_url, plot, poster_img)
        # print('\n')
        # print('\n')

        # print('\n')

        # print('\n')
        # print('###############################')
        
        new_movie = create_new_movie(imdb_id, movie_url, imdb_rating,
                          movie_title, plot, release_date, poster_img)

    else:
        new_movie=Movie.query.filter_by(imdb_id=imdb_id).one()
        

    genres = request.args.get('genre').split(', ') #string with several genres; converting string to list
    rating = int(request.args.get('rating'))
    review = request.args.get('review')

    #review day is always current day
    date_review = datetime.date.today().strftime("%d-%b-%Y")

    new_review = create_new_review(new_movie.movie_id, session.get('current_user'), review, rating, date_review)

    create_movie_genres_connection(new_movie.movie_id, genres)
     
    # print('###############################')
    # print('\n')
    # print('\n')

    # print('\n')
    # print (rating, review, date_review)
    # print('\n')
    # print('\n')

    # print('\n')
    # print ('new movie', new_movie)
    # print('new review', new_review)
    # print('\n')
    # print('\n')
    # print('current user id', session.get('current_user'))

    # print('\n')

    # print('\n')
    # print('###############################')

    flash ('movie was added')

    return redirect('/homepage')



if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
