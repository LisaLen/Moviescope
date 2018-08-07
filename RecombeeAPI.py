from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import json

import os # to access OS environment variables

client = RecombeeClient(os.environ['DB_NAME'],
                        os.environ['SECRET_TOKEN'])

def add_new_user_to_recombee(user_id):
    '''add new user to recombee.com DB'''

    try:
        client.send(AddUser(user_id))
        return True
    except:
        return False

def send_new_rating_to_API(user_id, imdb_id, rating):
    '''sends new rating information to recombee.com DB'''

    # Rating rescaled to interval [-1.0,1.0], where -1.0 means the worst 
    # rating possible, 0.0 means neutral, and 1.0 means absolutely positive rating. 
    # For example, in the case of 5-star evaluations, 
    # rating = (numStars-3)/2 formula may be used for the conversion.

    converted_rating = (rating-3)/2 

    #given imdb_id: tt0123456, rid off tt with slicing
    interaction = {'user_id': user_id,
                    'imdb_id': imdb_id[2:],
                    'rating': converted_rating}
    r = AddRating(interaction['user_id'],
                  interaction['imdb_id'],
                  interaction['rating'],
                  cascade_create=True)
    try:
        client.send(r)
        return True
    except:
        return False

def get_recommendations_for_user(user_id, recoms=6):
    '''returns list with 5 recommended movies(imdb_id) for given user'''
    # make API request and get response
    # {'recomms': [{'id': '0120179'}, {'id': '0109813'}, {'id': '0115798'}, {'id': '0121765'}, {'id': '0112462'}], 
    # 'recommId': '974edbca-4840-42d4-ae5e-63b2bcd0eba4'}

    recommended = client.send(RecommendItemsToUser(str(user_id), recoms, cascade_create=True))
    recome_movies = []

    for recom in recommended['recomms']:
        recom_imdb = 'tt' + str(recom['id'])
        recome_movies.append(recom_imdb)
    return recome_movies

    
def get_recommendations_for_user_item(imdb_id, user_id, recoms=6):
    '''returns list with 5 recommended movies(imdb_id) for given user and given movie'''
    # make API request and get response
    # {'recomms': [{'id': '0120179'}, {'id': '0109813'}, {'id': '0115798'}, {'id': '0121765'}, {'id': '0112462'}], 
    # 'recommId': '974edbca-4840-42d4-ae5e-63b2bcd0eba4'}

    recommended = client.send(RecommendItemsToItem(imdb_id[2:], str(user_id), recoms, cascade_create=True))
    recome_movies = []

    for recom in recommended['recomms']:
        recom_imdb = 'tt' + str(recom['id'])
        recome_movies.append(recom_imdb)

    return recome_movies

    

if __name__ == '__main__':

    recommended = client.send(RecommendUsersToItem('0266697', 5))

    
















# {"userid": "672", "imdbid": "0266697", "rating": "5"},
# {"userid": "672", "imdbid": "0314331", "rating": "5"},






