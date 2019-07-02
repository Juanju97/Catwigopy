import catwigopy.twitter_manager as tm
from catwigopy.User import User
from catwigopy.auxiliar import *
from catwigopy.analysis import *
import pandas as pd
import pickle
import pkg_resources

name = "catwigopy"


class Catwigopy:

    """
    The main class of the package. It offers methods to manage all the functionality

    :param user_name: User's Twitter name (@name).
    :param consumer_key: consumer key generated by creating Twitter application.
    :param consumer_secret: consumer secret key generated by creating Twitter application.
    :param access_token: access token key generated by creating Twitter application.
    :param access_token_secret: access token secret key generated by creating Twitter application.
    :param number_of_tweets: Number of tweets to retrieve
    """

    # Class attribute configured via class method.
    api = None
    name = None
    user_name = None
    image = None
    description = None
    tweets = None
    analysis_results = None
    tweets_terms = None
    hashtags_terms = None
    topics_top_terms = None
    nmf = None
    tfidf = None
    tfidf_vectorizer = None

    def __init__(self, user_name, consumer_key, consumer_secret, access_token, access_token_secret, number_of_tweets=1200):
        self.api = tm.do_authentication(consumer_key, consumer_secret, access_token, access_token_secret)
        result = tm.search_user_tweets(self.api, user_name, number_of_tweets)
        self.user_name = user_name
        self.image = result[1]
        self.name = result[2]
        self.description = result[3]
        self.tweets = pd.DataFrame(result[0])
        self.analysis_results = {'nmf': None, 'kmeans': None}

    # Classify using NMF with the best hyperparameter configuration acquired in training phase.
    def get_user_classification(self):

        """
        This function launch the classification. First of all, it gets the model variables.

        :return: analysis dictionary.
        """

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

        if self.analysis_results['nmf'] is None:
            doc = " ".join(self.tweets['preprocessed_tweet'])
            self.analysis_results['nmf'] = apply_nmf(self.nmf, self.tfidf, self.tfidf_vectorizer, doc)

        return self.analysis_results['nmf']

    def get_user_name(self):

        """
        This function returns user name.

        :return: name of the user.
        """
        return self.name

    def get_user_username(self):

        """
        This function returns user username.

        :return: username of the user.
        """
        return self.user_name

    def get_user_description(self):

        """
        This function returns user description.

        :return: user description.
        """
        return self.description

    def get_user_image(self):

        """
        This function returns user image path.

        :return: user image path.
        """
        return self.image

    # Returns a dict with shape {name_of_category: [{text: term_i, count: 21}, {text: term_j, count: 15} ...], ...}
    def get_topics_top_terms(self, nterms=30):

        """
        This function gets model variables and launch the construction of topics top terms.

        :param nterms: Number of top terms per topic.
        :return: dict containing top terms per topic.
        """
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

        """
        This function launch the construction of a term count array for hashtags terms.

        :return: list containing hashtags terms and its occurrences values.
        """

        if self.tweets is None:
            return "error, user tweets have not been searched yet."

        if self.hashtags_terms is None:
            self.hashtags_terms = generate_occurences_dictionay([l for l in self.tweets['hashtags'] if l])
        return self.hashtags_terms

    # Returns a list of dictionaries with shape {text: term, count: 12}
    def get_tweets_terms_count(self):

        """
        This function launch the construction of a term count array for tweets terms.

        :return: list containing tweets terms and its occurrences values.
        """
        if self.tweets is None:
            return "error, user tweets have not been searched yet."

        if self.tweets_terms is None:
            self.tweets_terms = generate_occurences_dictionay([l for l in self.tweets['preprocessed_tokens'] if l])
        return self.tweets_terms


