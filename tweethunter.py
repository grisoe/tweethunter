import argparse
import json
import os
import sys
import time
from datetime import date, timedelta

import twint
from selenium import webdriver

SINCE_DATE = str((date.today() - timedelta(days=7)).strftime('%Y-%m-%d'))
UNTIL_DATE = str(date.today())

CONF_FILE = 'conf.json'
TEMP_OUTPUT_FILE = 'temp.json'
FINAL_OUTPUT_FILE = 'tweets.json'

ALL_COLUMNS = False


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--since', dest="since_date", help="Search since this date.")
    parser.add_argument('-u', '--until', dest="until_date", help="Search until this date.")
    parser.add_argument('-c', '--conf', dest="conf_file", help="Configuration file.")
    parser.add_argument('-a', '--all-columns', action="store_true", help="Get all columns from tweets.")

    options = parser.parse_args()

    return options


def set_globals(options):
    global SINCE_DATE
    global UNTIL_DATE
    global CONF_FILE
    global ALL_COLUMNS

    if options.since_date:
        SINCE_DATE = options.since_date
    if options.until_date:
        UNTIL_DATE = options.until_date
    if options.conf_file:
        CONF_FILE = options.conf_file
    if options.all_columns:
        ALL_COLUMNS = True


def twint_conf(output_file):
    c = twint.Config()
    c.Hide_output = True
    c.Store_object = True
    c.Store_json = True
    c.Output = output_file
    c.Since = SINCE_DATE
    c.Until = UNTIL_DATE

    if not ALL_COLUMNS:
        c.Custom["tweet"] = ["created_at", "link", "username", "tweet"]

    return c


def search_twitter(queries):
    c = twint_conf(TEMP_OUTPUT_FILE)

    for query in queries:
        c.Search = query
        twint.run.Search(c)

    tweets = twint.output.tweets_list
    twint.output.clean_lists()

    return tweets


def get_conf():
    in_twitter = []
    in_tweets = []
    to_skip = []

    with open(CONF_FILE) as conf:
        terms = json.load(conf)

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


def remove_tweets_from_users(to_skip):
    to_skip = [ts.lower() for ts in to_skip]
    lines = file_to_list()

    with open(FINAL_OUTPUT_FILE, 'w+') as f:
        for line in lines:
            tweet_un = json.loads(line)['username'].lower()
            if tweet_un not in to_skip:
                f.write(line)

    remove_temp_file()


def file_to_list():
    lines = []
    with open(TEMP_OUTPUT_FILE, 'r+') as f:
        for line in f:
            lines.append(line)
    return lines


def remove_temp_file():
    os.remove(TEMP_OUTPUT_FILE)


def links_from_file():
    links = []
    with open(FINAL_OUTPUT_FILE, 'r+') as f:
        for line in f:
            links.append(json.loads(line)['link'])
    return links


def tweets_to_png():
    links = links_from_file()

    browser = webdriver.Firefox()
    browser.get('https://twitter.com/premierleague/status/1390797107389468679')

    time.sleep(10)

    browser.save_screenshot('screenshot.png')
    browser.close()


def main():
    options = get_arguments()
    set_globals(options)

    in_twitter, in_tweets, to_skip = get_conf()
    queries = create_search_queries(in_twitter, in_tweets)

    try:
        search_twitter(queries)
    except KeyboardInterrupt:
        print('\n[-] CTRL-C detected. Exiting...')
        remove_temp_file()
        sys.exit(0)

    if os.path.exists(TEMP_OUTPUT_FILE):
        remove_tweets_from_users(to_skip)

        # Move... Or leave...
        tweets_to_png()


if __name__ == '__main__':
    main()
