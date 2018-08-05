import os # to access OS environment variables
import requests
import json

def api_request(imdb_id):
    '''takes imdb_id as str and json response from OMDB API'''

    url = 'http://www.omdbapi.com/?i=' + imdb_id + '&apikey=' + os.environ['OMDB_API_KEY'] + '&plot=short'
    return requests.get(url).json()
     