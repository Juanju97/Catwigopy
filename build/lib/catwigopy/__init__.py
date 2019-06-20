import catwigopy.twitter_manager as tm
from catwigopy.User import User
from catwigopy.auxiliar import *
from catwigopy.analysis import *
import pandas as pd
import pickle
import pkg_resources

name = "catwigopy"


class Catwigopy:

    # Class attribute configured via class method.
    api = None
    _user = None
    topics_top_terms = None
    nmf = None
    tfidf = None
    tfidf_vectorizer = None

    def __init__(self, user_name, consumer_key, consumer_secret, access_token, access_token_secret, number_of_tweets=1200):
        self.api = tm.do_authentication(consumer_key, consumer_secret, access_token, access_token_secret)
        result = tm.search_user_tweets(self.api, user_name, number_of_tweets)
        self._user = User(user_name, result[1], result[2], result[3], pd.DataFrame(result[0]))

    # Classify using NMF with the best hyperparameter configuration acquired in training phase.
    def get_user_classification(self):
        if self.nmf is None:
            # Create routes
            resource_package = __name__
            resource_path = '/'.join(('data', 'models', 'nmf', 'nmf.pickle'))
            resource_path2 = '/'.join(('data', 'models', 'nmf', 'tfidf.pickle'))
            resource_path3 = '/'.join(('data', 'models', 'nmf', 'tfidf_vectorizer.pickle'))

            # If exists, load the models
            if pkg_resources.resource_exists(resource_package, resource_path) and \
                    pkg_resources.resource_exists(resource_package, resource_path2) and \
                    pkg_resources.resource_exists(resource_package, resource_path3):

                with open(pkg_resources.resource_filename(resource_package, resource_path), 'rb') as f:
                    self.nmf = pickle.load(f)

                with open(pkg_resources.resource_filename(resource_package, resource_path2), 'rb') as f:
                    self.tfidf = pickle.load(f)

                with open(pkg_resources.resource_filename(resource_package, resource_path3), 'rb') as f:
                    self.tfidf_vectorizer = pickle.load(f)

        if self._user.analysis_results['nmf'] is None:
            doc = " ".join(self._user.tweets['preprocessed_tweet'])
            self._user.analysis_results['nmf'] = apply_nmf(self.nmf, self.tfidf, self.tfidf_vectorizer, doc)

        return self._user.analysis_results['nmf']

    def get_user_name(self):
        return self._user.name

    def get_user_username(self):
        return self._user.user_name

    def get_user_description(self):
        return self._user.description

    def get_user_image(self):
        return self._user.image

    # Returns a dict with shape {name_of_category: [{text: term_i, count: 21}, {text: term_j, count: 15} ...], ...}
    def get_topics_top_terms(self, nterms=30):
        if self.nmf is None:
            # Create routes
            resource_package = __name__
            resource_path = '/'.join(('data', 'models', 'nmf', 'nmf.pickle'))
            resource_path2 = '/'.join(('data', 'models', 'nmf', 'tfidf.pickle'))
            resource_path3 = '/'.join(('data', 'models', 'nmf', 'tfidf_vectorizer.pickle'))

            # If exists, load the models
            if pkg_resources.resource_exists(resource_package, resource_path) and \
                    pkg_resources.resource_exists(resource_package, resource_path2) and \
                    pkg_resources.resource_exists(resource_package, resource_path3):
                with open(pkg_resources.resource_filename(resource_package, resource_path), 'rb') as f:
                    self.nmf = pickle.load(f)

                with open(pkg_resources.resource_filename(resource_package, resource_path2), 'rb') as f:
                    self.tfidf = pickle.load(f)

                with open(pkg_resources.resource_filename(resource_package, resource_path3), 'rb') as f:
                    self.tfidf_vectorizer = pickle.load(f)

        if self.topics_top_terms is None:
            self.topics_top_terms = generate_top_terms_dictionary(self.nmf, self.tfidf_vectorizer, nterms)

        return self.topics_top_terms

    # Returns a list of dictionaries with shape {text: #hashtag, count: 12}
    def get_hashtags_terms_count(self):
        if self._user.tweets is None:
            return "error, user tweets have not been searched yet."

        if self._user.hashtags_terms is None:
            self._user.hashtags_terms = generate_occurences_dictionay([l for l in self._user.tweets['hashtags'] if l])
        return self._user.hashtags_terms

    # Returns a list of dictionaries with shape {text: term, count: 12}
    def get_tweets_terms_count(self):
        if self._user.tweets is None:
            return "error, user tweets have not been searched yet."

        if self._user.tweets_terms is None:
            self._user.tweets_terms = generate_occurences_dictionay([l for l in self._user.tweets['preprocessed_tokens'] if l])
        return self._user.tweets_terms


