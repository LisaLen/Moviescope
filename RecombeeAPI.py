from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import json

client = RecombeeClient('leniashina', '3LkVzrObkifF37aVdpVaRTunAWrOsHO0AphHv53Y3ijxi9912894T9Heqx3kw8x3')

with open ('static/dataset/movie_user_ratings.json') as fdata:
    interactions = json.loads(fdata.read())

requests  =[]
    #interate through oll interactions and create object for each interaction
for interaction in interactions:
    r = AddRating(interaction['userid'],
                  interaction['imdbid'],
                  interaction['rating'],
                  cascade_create=True)
    #send single interaction
    #client.send(r)

    #making a list of interactions
    requests.append(r)

br = Batch(requests)
try:
    # Send the data to Recombee, use Batch for faster processing of larger data
    print('Send ratings')
    client.send(br)

    # # Get recommendations for user 'user-25'
    # recommended = client.send(RecommendItemsToUser('user-25', 5))
    # print("Recommended items: %s" % recommended)

except APIException as e:
    print(e)


