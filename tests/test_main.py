#Perform main tests

import time

from catwigopy import Catwigopy

consumer_key, consumer_secret, access_token, access_token_secret = ["WGH1yjqPiQg92igLjnhCg1wlC", "UwlSBz5Xxk7gConanvjq3XLOyHoCfVZk6JPSF7XOZMJvDu9NN4", "254490342-urFr0JJqjpHxYEvfg1JC2a2DtnHGIrD1lFqxSiOU", "EkxTbenoDae8cmDepAPJkDQ0WLyna6gNc4drmx07KWieh"]

cat = Catwigopy('sciencemagazine', consumer_key, consumer_secret, access_token, access_token_secret)
print(cat.get_user_description())
print(cat.get_user_classification())