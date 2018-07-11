from jinja2 import StrictUndefined

from flask import (Flask, request, render_template, redirect, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Review, Genre, MovieGenre

app = Flask(__name__)

app.secret_key = 'ABC'

@app.route('/')
def open_singin_singup_page():
    '''Show SignIn/SignUp page'''

    return render_template('signin_signup.html')

@app.route('/homepage')
def open_homepage():
    ''' Show homepage; show mivie list for a particular user'''
    if session: 
        movie_dict={}
        user_id = User.query.filter_by(login=session['current_user']).one().user_id
        print(user_id)

        #returns [(<Movie>, rating)]
        movies_ratings = db.session.query(Movie, Review.rating).join(Review).filter_by(user_id=user_id)    
        print(movies_ratings)   
        
        return render_template('homepage.html', movies_ratings=movies_ratings)
    else: 
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
            session['current_user'] = login
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
 
    if user:
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


if __name__ == '__main__':
    app.debug = True
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
