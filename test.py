# tests to test server.py

import unittest
from server import app
from model import connect_to_db, db, example_data

class SignInTestCase(unittest.TestCase):
    '''integration tests, testing Flask server'''

    def setUp(self):
        '''Code to run before every test.'''

        self.client = app.test_client()
        app.config['TESTING'] = True
   
    def test_index(self):
        '''Does user see sing-in page?'''
        #test client makes a request to app, app is NOT actually running
        
        result = self.client.get('/')
        self.assertIn(b'<h1>Registration</h1>', result.data)
        self.assertIn(b'class="navbar-toggler', result.data)

    def test_logout(self):
        '''Does user see sing-in page?'''
        #test client makes a request to app, app is NOT actually running
        
        result = self.client.get('/logout',  follow_redirects=True)
        self.assertIn(b'<h1>Registration</h1>', result.data)
        self.assertIn(b'class="navbar-toggler', result.data)

    def test_homepage_not_in_session(self):
        '''tests /homepage when user not in session'''

        result = self.client.get('/homepage', follow_redirects=True)
        self.assertIn(b'<h1>Registration</h1>', result.data)
        self.assertIn(b'class="navbar-toggler', result.data)

    def test_add_movie_not_in_session(self):
        '''test /add-movie when user not in session'''

        result = self.client.get('/add-movie',  follow_redirects=True)
        self.assertIn(b'<h1>Registration</h1>', result.data)
        self.assertIn(b'class="navbar-toggler', result.data)



    

class JournalTestsDatabase(unittest.TestCase):

    def setUp(self):
        '''Code to run before every test.'''

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1


        #connect to testDB
        connect_to_db(app, "postgresql:///testdb")

        #create table and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_sign_in_success(self):
        '''Does user sign in to account?'''
        
        result = self.client.post('/sign-in', data={'email': 'testemail1@gmail.com', 'password': '123'}, follow_redirects=True)
        # print(result)
        self.assertIn(b'<h2>My Watched Movies List</h2>', result.data)
        self.assertIn(b'<span>Logged in as Test1 Supertest1 </span>',result.data)
        self.assertIn(b'<a class="nav-link" href=\'/add-movie\'>Add Movie</a>',result.data)
        self.assertIn(b'tb_journal', result.data)
        self.assertIn(b'Edit Review </button>', result.data)
        self.assertIn(b'Delete </button>', result.data)

    def test_sign_in_wrong_password(self):
        '''Does user sign in to account?'''
        
        result = self.client.post('/sign-in', data={'email': 'testemail1@gmail.com', 'password': '789'}, follow_redirects=True)
        # print(result)
        self.assertIn(b'Wrong password', result.data)

    def test_sign_in_no_user(self):
        '''Does user sign in to account?'''
        
        result = self.client.post('/sign-in', data={'email': 'testemail@gmail.com', 'password': '123'}, follow_redirects=True)
        self.assertIn(b'<span>Username doesn', result.data)
        self.assertIn(b'exist </span>', result.data)




    def test_registration_form_new_email(self):
        '''cheks sending form information to server'''

  
        result = self.client.post('/sign-up', data={'email': 'testemail@gmail.com', 'password': '12345',
                                                    'fname': 'testfname',
                                                    'lname': 'testlname'},
                                              follow_redirects=True)

       
        self.assertIn(b'<span>New user has been added. Please sign-in to continue </span>', result.data)

    def test_registration_form_existing_email(self):
        '''cheks registration form if email already exists in DB'''

  
        result = self.client.post('/sign-up', data={'email': 'testemail1@gmail.com', 'password': '123',
                                                    'fname': 'Test1',
                                                    'lname': 'Supertest2'},
                                              follow_redirects=True)

       
        self.assertNotIn(b'<span>New user has been added. Please sign-in to continue </span>', result.data)
        self.assertIn(b'Username with email: testemail1@gmail.com already exists in databese', result.data)

    def test_add_movie(self):
        '''tests add_movie form'''

        result = self.client.get('/add-movie-to-journal', query_string={'title': 'NewMovie', 
                                                                'imdbid': 'tt0123456',
                                                                'imdb_rating': '8.5',
                                                                'released': '2018-07-24',
                                                                'genre': ['testgenre1, testgenre2'],
                                                                'rating': 5,
                                                                'review': 'testing review',
                                                                'plot': 'testingplot',
                                                                'movie_url': 'http//testingurl',
                                                                'poster_img': 'N/A'},
                                                                follow_redirects=True)


       
        self.assertIn(b'href=\' http//testingurl\'>NewMovie </td>', result.data)      
        self.assertIn(b'testingplot', result.data)
        self.assertIn(b'2018-07-24', result.data)
        self.assertIn(b'testgenre1', result.data )
        self.assertIn(b'testing review</td>', result.data)




class FlaskTestsLoggedIn(unittest.TestCase):
    '''testing reroute when user in session'''

    def setUp(self):
        app.config['TESTIN'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_signin_in_session(self):
        '''testing sign-in redirect if user in session'''

        result = self.client.get('/', follow_redirects=True)
        self.assertIn(b'<h2>My Watched Movies List</h2>', result.data)
    
    def test_homepage_in_session(self):
        '''tests /homepage when user in session'''

        result = self.client.get('/homepage', follow_redirects=True)
        self.assertIn(b'<h2>My Watched Movies List</h2>', result.data)



    def test_movie_table(self):
        result = self.client.get('/homepage')

        self.assertIn(b'img src=', result.data)
        self.assertIn(b' https://www.warnerbros.com/batman-forever\'>Batman Forever </td>', result.data)      
        self.assertIn(b'Batman must battle former', result.data)
        self.assertIn(b'2008-07-16', result.data)
        self.assertIn(b'test_genre', result.data )
        self.assertIn(b'really like it</td>', result.data)


    
       
    def test_add_movie_in_session(self):
        '''tests /add-movie route when user in session'''
        result = self.client.get('/add-movie')

        self.assertIn(b'IMDb</button>', result.data)

    def test_delete_from_journal(self):
        '''tests if function deletes movie from current user's journal'''

        result = self.client.get('/delete-from-joural.json', query_string={'imdb_id': 'tt0112462'})
        
        self.assertEqual(result.data, b'confirmed')

    def test_chek_if_movie_in_journal(self):
        '''tests if function returns True when imdb is in curent user's journal'''

        result = self.client.get('/check-imdbid-indb', query_string={'imdb_id': 'tt0112462'})
        self.assertEqual(result.data, b'True')

    def test_wish_list_in_session(self):
        '''tests /add-movie route when user in session'''

        result = self.client.get('/wish-list')

        self.assertIn(b'My Wish List', result.data)

    def test_wish_list_table(self):
        result = self.client.get('/wish-list')

        self.assertIn(b'img src=', result.data)
        self.assertIn(b'Full Cycle </td>', result.data)      
        self.assertIn(b'TestPlot3', result.data)
        self.assertIn(b'test_genre3', result.data )

    def test_delete_from_wishlist(self):
        '''tests if function deletes movie from current user's journal'''

        result = self.client.get('/delete-from-wishlist.json', query_string={'movie_id': '3'})
        
        self.assertEqual(result.data, b'confirmed')


class MyAppUnitTestCase(unittest.TestCase):
    '''unitTests'''

    def setUp(self):
        app.config['TESTIN'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()

   
    def test_chek_if_movie_not_in_journal(self):
        '''tests if function returns False when imdb is not in curent user's journal'''

        result = self.client.get('/check-imdbid-indb', query_string={'imdb_id': 'tt7654321'})
        self.assertEqual(result.data, b'False')




if __name__ == '__main__':
    unittest.main()



