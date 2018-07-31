from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import json

import os # to access OS environment variables

client = RecombeeClient(os.environ['DB_NAME'],
                        os.environ['SECRET_TOKEN'])


def send_new_rating_to_API(userid, imdb_id, rating):
    '''sends new rating information to recombee.com DB'''

    interaction = {'userid': userid,
                    'imdb_id': imdb_id,
                    'rating': rating}

    r = AddRating(interaction['userid'],
                  interaction['imdb_id'],
                  interaction['rating'],
                  cascade_create=True)
    # try:
    client.send(r)
    # return True

    # except APIException as e:
    #     print(e)
    #     return False

def get_recommendations_for_user(user_id, recoms=6):
    '''returns list with 5 recommended movies(imdb_id) for given user'''

    
    #make API request and get response
    #{'recomms': [{'id': '0120179'}, {'id': '0109813'}, {'id': '0115798'}, {'id': '0121765'}, {'id': '0112462'}], 
    #'recommId': '974edbca-4840-42d4-ae5e-63b2bcd0eba4'}

    
    recommended = client.send(RecommendItemsToUser(str(user_id), recoms))
    recome_movies = []

    for recom in recommended['recomms']:
        recom_imdb = 'tt' + str(recom['id'])
        recome_movies.append(recom_imdb)

    print(recome_movies)
    return recome_movies



def get_recommendations_for_user_item(imdb_id, user_id, recoms=6):
    '''returns list with 5 recommended movies(imdb_id) for given user and given movie'''

    #make API request and get response
    #{'recomms': [{'id': '0120179'}, {'id': '0109813'}, {'id': '0115798'}, {'id': '0121765'}, {'id': '0112462'}], 
    #'recommId': '974edbca-4840-42d4-ae5e-63b2bcd0eba4'}

    #given imdb_id: tt0123456, rid off tt with slicing
    recommended = client.send(RecommendItemsToItem(imdb_id[2:], str(user_id), recoms))

    recome_movies = []

    for recom in recommended['recomms']:
        recom_imdb = 'tt' + str(recom['id'])
        recome_movies.append(recom_imdb)

    print(recome_movies)
    return recome_movies







