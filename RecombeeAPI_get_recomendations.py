from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import json

client = RecombeeClient('leniashina', '3LkVzrObkifF37aVdpVaRTunAWrOsHO0AphHv53Y3ijxi9912894T9Heqx3kw8x3')

# recommended = client.send(RecommendItemsToUser('672', 5))
recommended = client.send(RecommendItemsToItem('0118688','672', 5))


print(recommended)