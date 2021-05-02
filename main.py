import twint
import json
from datetime import date

CONF_FILE = 'conf.json'


def search_in_twitter():
    today = date.today()

    c = twint.Config()
    c.Search = ''
    c.Hide_output = True
    c.Store_object = True
    c.Since = str(today)

    twint.run.Search(c)

    return twint.output.tweets_list


def print_from_twitter(tweets):
    for tweet in tweets:
        print(tweet.username)


def get_conf_terms():
    with open(CONF_FILE) as conf:
        terms = json.load(conf)
        in_twitter = []
        in_tweets = []
        for term in terms['inTwitter']:
            in_twitter.append(term)
        for term in terms['inTweets']:
            in_tweets.append(term)
    return in_twitter, in_tweets


if __name__ == '__main__':
    # print_from_twitter(search_in_twitter())
    print(get_conf_terms()[0])
    print(get_conf_terms()[1])
