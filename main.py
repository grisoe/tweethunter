import twint
from datetime import date

if __name__ == '__main__':
    today = date.today()

    c = twint.Config()
    c.Search = "bigtoken bot"
    # Temp: for faster tests.
    # c.Limit = 3
    # For objects to be stored in twint.output.tweets_list
    c.Store_object = True
    # c.Since = str(today)

    twint.run.Search(c)

    tweets = twint.output.tweets_list
    # print('\n\n', tweets[-4].username)

# c = twint.Config()
# c.Username = "srmhdz"
# # c.Store_object = True
# c.User_full = True
# c.Profile_full = True
# c.Custom["tweet"] = ["id", "username", "link"]
# c.Retweets = True
# c.Hide_output = True
# c.Lowercase = True
# c.Store_json = True
# c.Output = "none.json"
#
# # twint.run.Search(c)
# # Returns more tweets.
# twint.run.Profile(c)
#
# tweets = twint.output.tweets_list
# for i in tweets:
#     print(i.hashtags)
