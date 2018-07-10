from flask import (Flask, request, render_template, redirect, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = 'ABC'

@app.route('/')
def open_singin_singup_page():
    '''Show SignIn/SignUp page'''

    print('opening signin page')

    return render_template('signin_signup.html')

@app.route('/homepage')
def open_homepage():
    ''' Show homepage'''

    return render_template('homepage.html')










if __name__ == '__main__':
    DebugToolbarExtension(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
