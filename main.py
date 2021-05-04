import twint
import json
from datetime import date

DATE = str(date.today())
CONF_FILE = 'conf.json'
OUTPUT_FILE = 'output.json'


def search_in_twitter(queries):
    c = twint.Config()
    c.Hide_output = True
    c.Store_object = True
    c.Store_json = True
    c.Custom["tweet"] = ["created_at", "link", "username", "tweet"]
    c.Output = OUTPUT_FILE
    c.Since = '2018-05-01'
    # c.Until = '2019-01-01'

    for query in queries:
        c.Search = query
        twint.run.Search(c)

    _tweets = twint.output.tweets_list
    twint.output.clean_lists()

    return _tweets


def search_users_profiles(users, queries):
    tweets = []
    print(f'BIG LIST: {twint.output.tweets_list}')

    c = twint.Config()
    c.Hide_output = True
    c.Store_object = True
    # c.Store_json = True
    c.Profile_full = True
    # c.Custom["tweet"] = ["created_at", "link", "username", "tweet"]
    # c.Output = 'JEJEJEJE.json'
    # c.Since = '2018-05-01'
    # c.Until = '2019-01-01'

    for user in users:
        for query in queries:
            c.Username = user
            c.Search = query

    if twint.output.tweets_list:
        tweets.append(twint.output.tweets_list)
    print(tweets)
    return tweets


# Is this function really needed?
def print_tweets(tweets):
    for index, tweet in enumerate(tweets):
        print(f'{index}: {tweet.username}, {tweet.tweet}, {tweet.link}\n')


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


def get_users(tweets):
    users = []
    for tweet in tweets:
        for info in tweet:
            users.append(info.username)
    return list(dict.fromkeys(users))


if __name__ == '__main__':
    in_twitter, in_tweets = get_conf_terms()
    queries = create_search_queries(in_twitter, in_tweets)
    tweets = search_in_twitter(queries)
    # users = get_users(tweets)
    # tweets2 = search_users_profiles(users, queries)
    print_tweets(tweets)
