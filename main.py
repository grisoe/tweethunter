import argparse
import json
import os
from datetime import date, timedelta

import twint

SINCE_DATE = str((date.today() - timedelta(days=7)).strftime('%Y-%m-%d'))
UNTIL_DATE = str(date.today())
CONF_FILE = 'conf.json'

TEMP_OUTPUT_FILE = 'temp.json'
TWEETS_OUTPUT_FILE = 'temp2.json'
FINAL_OUTPUT_FILE = 'tweets.json'


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--since', dest="since_date", help="Search since this date.")
    parser.add_argument('-u', '--until', dest="until_date", help="Search until this date.")
    parser.add_argument('-c', '--conf', dest="conf_file", help="Configuration file.")

    options = parser.parse_args()

    return options


def set_globals(options):
    global SINCE_DATE
    global UNTIL_DATE
    global CONF_FILE

    if options.since_date:
        SINCE_DATE = options.since_date
    if options.until_date:
        UNTIL_DATE = options.until_date
    if options.conf_file:
        CONF_FILE = options.conf_file


def twint_conf(output_file):
    c = twint.Config()
    c.Hide_output = True
    c.Store_object = True
    c.Store_json = True
    c.Custom["tweet"] = ["created_at", "link", "username", "tweet"]
    c.Output = output_file
    c.Since = SINCE_DATE
    c.Until = UNTIL_DATE
    return c


def search_twitter(queries):
    c = twint_conf(TEMP_OUTPUT_FILE)

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
    to_skip = [ts.lower() for ts in to_skip]
    lines = file_to_list()

    with open(FINAL_OUTPUT_FILE, 'w') as f:
        for line in lines:
            tweet_un = json.loads(line)['username'].lower()
            if tweet_un not in to_skip:
                f.write(line)

    remove_temp_file()


def file_to_list():
    lines = []
    with open(TEMP_OUTPUT_FILE, 'r') as f:
        for line in f:
            lines.append(line)
    return lines


def remove_temp_file():
    if os.path.exists(TEMP_OUTPUT_FILE):
        os.remove(TEMP_OUTPUT_FILE)


def main():
    options = get_arguments()
    set_globals(options)

    in_twitter, in_tweets, to_skip = get_conf()
    queries = create_search_queries(in_twitter, in_tweets)

    search_twitter(queries)
    remove_tweets_from_users(to_skip)

    # tweets = search_twitter(queries)
    # print_tweets(tweets)
    # print(f'Tweets length: {len(tweets)}')

    # users = get_users(tweets)
    # print(f'Users: {users}')
    # print(f'Users length: {len(users)}')

    # users_clean = clean_users(users, to_skip)
    # print(f'Users clean: {users_clean}')
    # print(f'Users clean length: {len(users_clean)}')

    # tweets_prof = search_users_prof(users_clean, queries)
    # print(f'Tweets Prof length: {len(tweets_prof)}')
    # print_tweets(tweets_prof)


if __name__ == '__main__':
    main()
