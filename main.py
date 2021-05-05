import twint
import json
import os
from datetime import date

DATE = str(date.today())
CONF_FILE = 'conf.json'

TWITTER_OUTPUT_FILE = 'output.json'
TWEETS_OUTPUT_FILE = 'output2.json'


def twint_conf(output_file):
    c = twint.Config()
    c.Hide_output = True
    c.Store_object = True
    c.Store_json = True
    c.Custom["tweet"] = ["created_at", "link", "username", "tweet"]
    c.Output = output_file
    # c.Since = '2018-03-01'
    # c.Until = '2019-01-01'
    return c


def search_twitter(queries):
    c = twint_conf(TWITTER_OUTPUT_FILE)

    for query in queries:
        c.Search = query
        twint.run.Search(c)

    tweets = twint.output.tweets_list
    twint.output.clean_lists()

    return tweets


def search_users_prof(users_clean, queries):
    c = twint_conf(TWEETS_OUTPUT_FILE)
    c.Profile_full = True

    for user in users_clean:
        for query in queries:
            c.Username = user
            c.Search = query
            twint.run.Search(c)

    tweets = twint.output.tweets_list
    twint.output.clean_lists()

    return tweets


def print_tweets(tweets):
    for index, tweet in enumerate(tweets):
        print(f'{index}: {tweet.username}, {tweet.tweet}, {tweet.link}\n')


def get_conf():
    with open(CONF_FILE) as conf:
        terms = json.load(conf)
        in_twitter = []
        in_tweets = []
        to_skip = []

        for term in terms['inTwitter']:
            in_twitter.append(term)
        for term in terms['inTweets']:
            in_tweets.append(term)
        for term in terms['remove']:
            to_skip.append(term)

    return in_twitter, in_tweets, to_skip


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
        users.append(tweet.username)
    return list(dict.fromkeys(users))


def clean_users(users, to_skip):
    to_skip = [x.lower() for x in to_skip]
    return list(set(users) - set(to_skip))


def remove_tweets_from_users(to_skip):
    lines = []
    to_skip = [ts.lower() for ts in to_skip]

    with open(TWITTER_OUTPUT_FILE, 'r') as f:
        for line in f:
            lines.append(line)

    with open('final.json', 'w') as f2:
        for line in lines:
            tweet_un = json.loads(line)['username'].lower()
            if tweet_un not in to_skip:
                f2.write(line)

    if os.path.exists(TWITTER_OUTPUT_FILE):
        os.remove(TWITTER_OUTPUT_FILE)


def main():
    in_twitter, in_tweets, to_skip = get_conf()
    queries = create_search_queries(in_twitter, in_tweets)

    tweets = search_twitter(queries)
    # print_tweets(tweets)
    # print(f'Tweets length: {len(tweets)}')

    users = get_users(tweets)
    # print(f'Users: {users}')
    # print(f'Users length: {len(users)}')

    users_clean = clean_users(users, to_skip)
    # print(f'Users clean: {users_clean}')
    # print(f'Users clean length: {len(users_clean)}')

    remove_tweets_from_users(to_skip)

    # tweets_prof = search_users_prof(users_clean, queries)
    # print(f'Tweets Prof length: {len(tweets_prof)}')
    # print_tweets(tweets_prof)


if __name__ == '__main__':
    main()
