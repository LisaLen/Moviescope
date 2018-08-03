from jinja2 import StrictUndefined
from flask import (Flask, request, render_template, redirect, flash, session,jsonify)
from flask_debugtoolbar import DebugToolbarExtension
# import uuid
# import hashlib
from model import connect_to_db, db, User, Movie, Review, Genre, MovieGenre, WishList
import RecombeeAPI
import datetime

#import requests

#mport os # to access OS environment variables

import JustWatchAPI
import OMDB_API
from units import hash_password, check_password, create_new_movie, create_new_review

app = Flask(__name__)
app.secret_key = 'ABC'


@app.route('/')
def open_singin_singup_page():
    '''Show SignIn/SignUp page'''

    if session.get('current_user'):
        return redirect('homepage')
        
    return render_template('signin_signup.html')
    

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Action for login form; log a user in'''

    email = request.form.get('email')
    password = request.form.get('password')

    #query to get user object using email
    user = User.query.filter_by(email=email).first()
                
    if user:
        if check_password(user.password, password):
            #stor user_id in session
            session['current_user'] = user.user_id
            fname, lname = user.fname, user.lname  

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
    return render_template('signin_signup.html')

@app.route('/email-check', methods=['POST'] )
def check_email_in_db():
    '''check if user with given email exists in DB'''

    email = request.form.get('email')
    if User.query.filter_by(email=email).first():
        return 'email exists'
    return 'OK'

@app.route('/sign-up', methods=['POST'])
def register_new_user():
    '''create new user'''
   
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        password = hash_password(request.form.get('password'))
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        new_user = User(email=email, password=password, 
                        fname=fname, lname=lname, )
        db.session.add(new_user)
        db.session.commit()

        #add new user to DB at RecombeeAPI 
        add_new_user_to_recombee(user_id)
    
        flash('New user has been added. Please sign-in to continue')
        return redirect('/')
    else:
        flash (f'Username with email: {email} already exists in databese')
        return redirect('/')
        
@app.route('/homepage')
def open_homepage():
    ''' Show homepage; show mivie list for a particular user''' 

    if not session.get('current_user'): 
        return redirect('/')  
      

    print(session['current_user'])       
    recommendations = RecombeeAPI.get_recommendations_for_user(session['current_user'])
    print(recommendations)

    recom_movies = []

    for recommendation in recommendations:
        recom_movie = OMDB_API.api_request(recommendation)
        recom_movies.append(recom_movie)

    print(recom_movies)

    # returns [(<Movie>, <Review>)]
    movies_reviews = db.session.query(Movie, Review).join(Review)\
                                    .options(db.subqueryload(Movie.genres))\
                                    .filter_by(user_id=session['current_user']).all()
    movies_reviews.reverse()
 
    return render_template('homepage.html', movies_reviews=movies_reviews,
                                            recom_movies=recom_movies)
       

@app.route('/add-movie')
def link_to_add_movie():
    ''' Show add_moview page'''

    if not session.get('current_user'): 
        return redirect('/')  

    return render_template('add_movie.html')
    
@app.route('/wish-list')
def open_wish_list():
    ''' Show wish_list page'''

    if not session.get('current_user'): 
        return redirect('/')  

    user = User.query.filter_by(user_id=session['current_user']).one()
    wishlist = user.wishlist
    wishlist.reverse()

    return render_template('wish_list.html', wishlist=wishlist)

    
@app.route('/movie-page')
def open_movie_page():
    ''' Show movie page'''

    if not session.get('current_user'): 
        return redirect('/')  

    user = User.query.filter_by(user_id=session['current_user']).one()
    imdb_id = request.args.get('imdb_id')

    #get movie information from OMDB APi
    movie_info = OMDB_API.api_request(imdb_id)
  
    #fetching recommendations for current user
    recommendations = RecombeeAPI.get_recommendations_for_user_item(imdb_id, user.user_id)

    #to stor movie information for recommended movies ( stored in json)
    recom_movies = []

    for recommendation in recommendations:
        recom_movie = OMDB_API.api_request(recommendation)
        recom_movies.append(recom_movie)
    
    movie = Movie.query.filter_by(imdb_id=imdb_id).first()

    rating, in_wishlist  = None, False
    
    if movie:
        #check if imdb_id in current user's wishlist
        in_wishlist = (movie in user.wishlist)

        #check if we have movie in current user's journal  
        review = Review.query.filter_by(movie_id=movie.movie_id, 
                                        user_id=session['current_user']).first()
        if review:
            rating = review.rating
        
    return render_template('movie_page.html', movie=movie_info, 
                                              recom_movies=recom_movies,                                             
                                              rating=rating,
                                              in_wishlist=in_wishlist)

@app.route('/watch-it')
def show_watch_options():
    '''show watch_it page'''

    if not session.get('current_user'): 
        return redirect('/')  

    movie_title = request.args.get('movie_title')
    
    #taking relseas year only
    release_year = int(request.args.get('released')[:4])
    poster_img = request.args.get('poster_img')

    where_watch = JustWatchAPI.to_watch(movie_title, release_year)
       
    return render_template('watch_it.html', poster_img=poster_img,
                                            where_watch=where_watch)


@app.route('/check-imdbid-in_journal')
def chek_if_movie_in_journal():
    '''Checks if selected movie in current_user's journal. 
    Returns True if movie is in current_user's journal '''

    imdb_id = request.args.get('imdb_id')

    if db.session.query(Movie).join(Review)\
                              .filter(Review.user_id==session.get('current_user'), \
                               Movie.imdb_id==imdb_id).first():
        return 'True' 
    return 'False'   

@app.route('/chek-imdbid-in-wishlist')
def check_if_movie_in_wishlist():
    ''' Checks if selected movie in DB and in current_user's wishlist 
    Returns dictionary{movie_in_DB: True of False,
                        movie_in_wishlist: True or False} '''

    imdb_id = request.args.get('imdb_id')
    current_user = User.query.filter_by(user_id=session.get('current_user')).one()
    new_movie = Movie.query.filter_by(imdb_id=imdb_id).first()

    results = {'movie_in_db': False,
               'movie_in_wishlist': False}
    if new_movie:
        results['movie_in_db'] = True
        if new_movie in current_user.wishlist:
            results['movie_in_wishlist'] = True

    return jsonify(results)


@app.route('/add-movie-to-db')
def add_movie_to_database():
    '''add new moview to DB'''
   
    imdb_id = request.args.get('imdb_id')
    movie_title = request.args.get('movie_title')
    imdb_rating = request.args.get('imdb_rating')
    release_date = request.args.get('released')
    plot = request.args.get('plot')
    movie_url = request.args.get('movie_url')
    poster_img = request.args.get('poster_img')
    genres = request.args.get('genre').split(', ') #string with several genres; converting string to list

            
    new_movie = create_new_movie(imdb_id, movie_url, imdb_rating,
                          movie_title, plot, release_date, poster_img, genres)

    db.session.add(new_movie)
    try:
        db.session.commit()
        return 'OK'
    except:
        return 'ERROR'


@app.route('/add-to-wishlist')
def add_movie_to_user_wishlist():
    '''add movie to current user's wish list'''

    imdb_id = request.args.get('imdb_id')
    
    movie = Movie.query.filter_by(imdb_id=imdb_id).one()

    current_user = User.query.filter_by(user_id=session.get('current_user')).one()
    
    try:
        current_user.wishlist.append(movie)
        db.session.add(current_user)
        db.session.commit()
        return 'OK'

    except:
        return 'ERROR'     

@app.route('/add-movie-to-journal')
def add_new_movie():
    '''Add new movie, rating and review into journal'''

    imdb_id = request.args.get('imdbid')
    new_movie=Movie.query.filter_by(imdb_id=imdb_id).first()
        
    if not new_movie:
        #if given imdb_id doesn't exist in DB, then create new_movie in DB
        movie_title = request.args.get('title')
        genres = request.args.get('genre').split(', ') #string with several genres; converting string to list
        imdb_rating = request.args.get('imdb_rating')
        release_date = request.args.get('released')
        plot = request.args.get('plot')
        movie_url = request.args.get('movie_url')
        poster_img = request.args.get('poster_img')
            
        new_movie = create_new_movie(imdb_id, movie_url, imdb_rating,
                          movie_title, plot, release_date, poster_img, genres)

    rating = int(request.args.get('rating'))
    review = request.args.get('review')

    #review day is always current day
    date_review = datetime.date.today().strftime("%Y-%m-%d")

    new_review = create_new_review(new_movie.movie_id, session.get('current_user'), review, rating, date_review)
    RecombeeAPI.send_new_rating_to_API(session.get('current_user'), imdb_id, rating)


    flash ('movie was added')

    return redirect('/homepage')

@app.route('/delete-from-joural.json')
def delete_movie_from_journal():
    '''deletes movie_id-user_id relationship and user's review for given movie_id in reviews table. It doesn't delete movie from DB'''

    movie_id = request.args.get('movie_id')

    #fetching review for given movie_id and current user
    try:
        Review.query.filter_by(movie_id=movie_id, user_id=session.get('current_user')).delete()
        db.session.commit()
        return 'confirmed'
    except: 
        return 'ERROR' 

@app.route('/edit-review.json')
def edit_rating_and_review():
    '''edits rating and review of selected movie'''

    movie_id = request.args.get('movie_id')
    new_rating = request.args.get('new_rating')
    new_review =  request.args.get('new_review')
    date_review = datetime.date.today().strftime("%Y-%m-%d")
    
     #fetching review for given movie_id and current user
    review = Review.query.filter_by(movie_id=movie_id, user_id=session.get('current_user')).one()

    review.rating = new_rating
    review.review = new_review
    review.date_review = date_review
   
    try:
        db.session.commit()
        return jsonify({'date_review': date_review})

    except:
        return 'ERROR'     

@app.route('/delete-from-wishlist.json')
def delete_movie_from_wishlist():
    '''deletes movie_id-user_id relationship from wishlists. It doesn't delete movie from DB'''

    movie_id = request.args.get('movie_id')

    #fetching review for given movie_id and current user
    try:
        WishList.query.filter_by(movie_id=movie_id, user_id=session.get('current_user')).delete()
        db.session.commit()
        return 'confirmed'
    except: 
        return 'ERROR' 


if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
