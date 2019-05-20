import pandas as pd
import numpy as np
import threading
from multiprocessing import Pool
from catwigopy.auxiliar import *
from catwigopy.twitter_manager import *


class User:
    name = None
    user_name = None
    image = None
    description = None
    tweets = None
    analysis_results = None

    def __init__(self, user_name, image_url, name, description):
        self.user_name = user_name
        self.image = image_url
        self.name = name
        self.description = description
        self.analysis_results = {'nmf': None, 'kmeans': None}
