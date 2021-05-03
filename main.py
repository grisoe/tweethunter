import twint
import json
from datetime import date

DATE = str(date.today())
CONF_FILE = 'conf.json'


def search_in_twitter(queries):
    tweets = []

    for query in queries:
        c = twint.Config()
        c.Hide_output = True
        c.Store_object = True
        c.Since = '2020-01-01'
        c.Search = query

        twint.run.Search(c)

        if len(twint.output.tweets_list) != 0:
            tweets.append(twint.output.tweets_list)

    return tweets


def print_tweets(tweets):
    for re in range(0, len(tweets)):
        for query_result in tweets:
            print(f'\n\n{query_result[re].tweet}\n\n')


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


def create_search_queries(in_twitter, in_tweets):
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
    queries = create_search_queries(in_twitter, in_tweets)
    tweets = search_in_twitter(queries)
    print_tweets(tweets)
