import argparse
import json
import math
import os
import sys
import time
from datetime import date, timedelta, datetime
from io import BytesIO

import twint
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

CURRENT_TIME = datetime.now().strftime("%H:%M:%S")

SINCE_DATE = str((date.today() - timedelta(days=7)).strftime('%Y-%m-%d'))
UNTIL_DATE = str(date.today())

CONF_FOLDER = 'conf'
JSON_OUTPUT_FOLDER = 'output'
IMAGES_OUTPUT_FOLDER = 'images'
OUT_FOLDER = date.today().strftime('%Y-%m-%d')

CONF_FILE = f'{CONF_FOLDER}/conf.json'
TEMP_OUTPUT_FILE = f'{JSON_OUTPUT_FOLDER}/temp.json'
FINAL_OUTPUT_FILE = f'{JSON_OUTPUT_FOLDER}/{OUT_FOLDER}/{CURRENT_TIME}.json'

ALL_COLUMNS = False
SCREENSHOTS = False

# Real one is (sometimes) 48,
# 47 secondary, plus 1 main.
SEARCH_TERMS_LIMIT = 30


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--since', dest="since_date", help="Search since this date.")
    parser.add_argument('-u', '--until', dest="until_date", help="Search until this date.")
    parser.add_argument('-c', '--conf', dest="conf_file", help="Configuration file.")
    parser.add_argument('-a', '--all-columns', action="store_true", help="Get all columns from tweets.")
    parser.add_argument('-i', '--screenshots', action="store_true", help="Take screenshots of tweets.")

    options = parser.parse_args()

    return options


def set_globals(options):
    global SINCE_DATE
    global UNTIL_DATE
    global CONF_FILE
    global ALL_COLUMNS
    global SCREENSHOTS

    if options.since_date:
        SINCE_DATE = options.since_date
    if options.until_date:
        UNTIL_DATE = options.until_date
    if options.conf_file:
        CONF_FILE = options.conf_file
    if options.all_columns:
        ALL_COLUMNS = True
    if options.screenshots:
        SCREENSHOTS = True


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
    terms_ranges = math.ceil(len(in_tweets) / SEARCH_TERMS_LIMIT)
    queries = []
    c_queries = []

    for i in range(0, terms_ranges):
        query = ''
        start = SEARCH_TERMS_LIMIT * i
        end = start + SEARCH_TERMS_LIMIT

        for j in range(start, end):
            if j < len(in_tweets):
                query = query + f' {in_tweets[j]} OR'
        queries.append(query)

    for term in in_twitter:
        for query in queries:
            n_query = f'{term}{query}'[0:-3]
            c_queries.append(n_query)

    return c_queries


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
    if os.path.exists(TEMP_OUTPUT_FILE):
        os.remove(TEMP_OUTPUT_FILE)


def links_from_file():
    links = []
    if os.path.exists(FINAL_OUTPUT_FILE):
        with open(FINAL_OUTPUT_FILE, 'r+') as f:
            for line in f:
                links.append(json.loads(line)['link'])
    return links


def tweets_to_png_cropped():
    links = links_from_file()

    if links:
        ff_options = webdriver.FirefoxOptions()
        ff_options.headless = True
        browser = webdriver.Firefox(options=ff_options, service_log_path=os.devnull)

        xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/' \
                'div[2]/div/section/div/div/div[1]/div/div/article/div'

        for i, link in enumerate(links):
            browser.get(link)
            browser.maximize_window()
            time.sleep(10)

            element = browser.find_element_by_xpath(xpath)
            location = element.location
            size = element.size

            png = browser.get_screenshot_as_png()
            im = Image.open(BytesIO(png))

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            im = im.crop((left, top, right, bottom))
            im.save(f'{IMAGES_OUTPUT_FOLDER}/{OUT_FOLDER}/{CURRENT_TIME}/{i + 1}.png')

        browser.close()


def tweets_to_png_full():
    links = links_from_file()

    if links:
        browser = webdriver.Firefox(service_log_path=os.devnull)

        for i, link in enumerate(links):
            browser.get(link)
            time.sleep(10)
            browser.save_screenshot(f'{IMAGES_OUTPUT_FOLDER}/{OUT_FOLDER}/{CURRENT_TIME}/{i + 1}.png')
        browser.close()


def create_output_folders():
    if not os.path.exists(JSON_OUTPUT_FOLDER):
        os.makedirs(JSON_OUTPUT_FOLDER)
    if not os.path.exists(CONF_FOLDER):
        os.makedirs(CONF_FOLDER)

    if not os.path.exists(f'{JSON_OUTPUT_FOLDER}/{OUT_FOLDER}'):
        os.makedirs(f'{JSON_OUTPUT_FOLDER}/{OUT_FOLDER}')

    if SCREENSHOTS:
        if not os.path.exists(IMAGES_OUTPUT_FOLDER):
            os.makedirs(IMAGES_OUTPUT_FOLDER)
        if not os.path.exists(f'{IMAGES_OUTPUT_FOLDER}/{OUT_FOLDER}'):
            os.makedirs(f'{IMAGES_OUTPUT_FOLDER}/{OUT_FOLDER}')
        if not os.path.exists(f'{IMAGES_OUTPUT_FOLDER}/{OUT_FOLDER}/{CURRENT_TIME}'):
            os.makedirs(f'{IMAGES_OUTPUT_FOLDER}/{OUT_FOLDER}/{CURRENT_TIME}')


def main():
    options = get_arguments()
    set_globals(options)
    create_output_folders()

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
    if SCREENSHOTS:
        tweets_to_png_cropped()


if __name__ == '__main__':
    main()
