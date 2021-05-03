import twint
import json
from datetime import date

DATE = str(date.today())
CONF_FILE = 'conf.json'


def search_in_twitter(in_twitter, in_tweets):
    # TODO: Create the strings to search for. Find out if logical operations are supported in Search.
    c = twint.Config()
    c.Search = 'bigtoken vpn OR termux OR hack'
    c.Hide_output = False
    c.Store_object = True
    # c.Since = DATE

    twint.run.Search(c)

    return twint.output.tweets_list


def print_from_twitter(tweets):
    for tweet in tweets:
        print(tweet.username)


def get_conf_terms():
    with open(CONF_FILE) as conf:
        terms = json.load(conf)
        terms_twitter = []
        terms_tweets = []
        for term in terms['inTwitter']:
            terms_twitter.append(term)
        for term in terms['inTweets']:
            terms_tweets.append(term)
    return terms_twitter, terms_tweets


def create_search_query(in_twitter, in_tweets):
    queries = []

    for termi in range(0, len(in_twitter)):
        query = ''
        for term in in_tweets:
            query = query + f' {term} OR'

        query = query[0:-3]
        query = in_twitter[termi] + query
        queries.append(query)

    return queries


if __name__ == '__main__':
    in_twitter, in_tweets = get_conf_terms()
    # search_in_twitter(in_twitter, in_tweets)
    create_search_query(in_twitter, in_tweets)
