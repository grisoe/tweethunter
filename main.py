import twint
from datetime import date


def search_in_twitter():
    today = date.today()

    c = twint.Config()
    c.Search = "bigtoken"
    c.Hide_output = True
    c.Store_object = True
    c.Since = str(today)

    twint.run.Search(c)

    return twint.output.tweets_list


def print_from_twitter(tweets):
    for tweet in tweets:
        print(tweet.username)


if __name__ == '__main__':
    print_from_twitter(search_in_twitter())
