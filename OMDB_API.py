import os # to access OS environment variables
import requests
import json

def api_request(imdb_id):
    '''takes imdb_id as str and returns url request for OMDB API'''

    url = 'http://www.omdbapi.com/?i=' + imdb_id + '&apikey=' + os.environ['OMDB_API_KEY'] + '&plot=full'
    return requests.get(url).json()
     