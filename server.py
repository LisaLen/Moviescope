from jinja2 import StrictUndefined

from flask import (Flask, request, render_template, redirect, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Review, Genre, MovieGenre
from datetime import datetime

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
    if session: 
                       
        #returns [(<Movie>, rating)]
        movies_ratings = db.session.query(Movie, Review.rating).join(Review).filter_by(user_id=session['current_user'])    

        return render_template('homepage.html', movies_ratings=movies_ratings)
    
    else: 
        return render_template('signin_signup.html')

@app.route('/add-movie')
def link_to_add_movie():
    ''' Show add_moview page'''

    return render_template('add_movie.html')

@app.route('/add-movie-to-journal')
def add_new_movie():
    '''Add new movie, rating and review into journal'''
    movie_title = request.args.get('title')
    rating = int(request.args.get('rating'))
    review = request.args.get('review')
    #date = datetime.strptime(request.args.get('review_date'), '%d-%b-%Y')
    print (movie_title, rating, review)
    flash ('movie was added')


    new_movie = Movie(title=movie_title)
    db.session.add(new_movie) 
    db.session.commit()

    print(new_movie.movie_id)
    print(session['current_user'])

    new_review = Review(movie_id=new_movie.movie_id, 
                        user_id=session['current_user'],
                        review=review,
                        rating=rating)

    db.session.add(new_review)
    db.session.commit()

    return redirect('homepage')




if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
