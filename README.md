# Catwigopy

[![Python Version](https://img.shields.io/pypi/pyversions/catwigopy.svg)](https://pypi.org/project/catwigopy/)
[![PyPi Version](https://img.shields.io/pypi/v/catwigopy.svg)](https://pypi.org/project/catwigopy/)

## Introduction

**Catwigopy** is a tool which provides an easy way to generate a preferences profile of a given Twitter user.
## Installation

To install the latest version of [**catwigopy**](https://pypi.org/project/catwigopy/) from PyPi use:

``pip install catwigopy``

All the dependencies are already listed on the setup file of the package, but to sum them up, you will need the following requirements:

* [**pandas 0.24.2**](https://pypi.org/project/pandas/)
* [**tweepy 3.7.0**](https://pypi.org/project/tweepy/)
* [**numpy 1.16.2**](https://pypi.org/project/numpy/)


**IMPORTANT**

To use Catwigopy you need to create a [Twitter application](https://developer.twitter.com/en/docs/basics/apps/overview), in order to  get the [acces tokens](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html) and connect with the Twitter API service.

## How to use it
First of all, import the module

``from catwigopy import Catwigopy``

This next line, creates an instance of Catwigopy for the specified user **username**.

``new_user = Catwigopy('Tesla', consumer_key, consumer_secret, access_token, access_token_secret)``

Now you can display the user's name, username, image and description.

``new_user.get_user_name()``

``new_user.get_user_username()``

``new_user.get_user_image()``

``new_user.get_user_description()``

To retrive the user timeline:

`new_user.search_user_timeline(number_of_tweets)`

By default, number_of_tweets is 1200. You can decrease the value to get better execution times, but the prediction 
accuracy will be penalized.

Now, train the model and classify the tweets:

``new_user.classify_tweets_nmf()``

And get the results in a dictionary:

``new_user.get_analysis_results()``

## Disclaimer

Please, bear in mind that Catwigopy has been developed only for research purpose. Make sure that you don't store
the results obtained with Catwigopy and, in any case, don't use this results with comercial purposes.

Catwigopy efficiency and accuracy have been tested with enterprise accounts like Nintendo or Tesla, and also with public figures accounts, like Theresa May or Pontifex.
If you want to analyse personal accounts, even if them are public, make sure you have the explicit consent.