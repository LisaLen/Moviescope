#run this file one time to seed DB at Recombee.com

from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import json
import os # to access OS environment variables

client = RecombeeClient(os.environ['DB_NAME'],
                        os.environ['SECRET_TOKEN'])

with open ('static/dataset/movie_user_ratings.json') as fdata:
    interactions = json.loads(fdata.read())

requests  =[]
    #interate through all interactions and create object for each interaction
for interaction in interactions:
    r = AddRating(interaction['userid'],
                  interaction['imdbid'],
                  interaction['rating'],
                  cascade_create=True)
   
    #making a list of interactions
    requests.append(r)

br = Batch(requests)
try:
    # Send the data to Recombee, use Batch for faster processing of larger data
    print('Send ratings')
    client.send(br)

except APIException as e:
    print(e)


