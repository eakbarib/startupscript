import json
import tweepy

# defines the class TwitterAccount
# which is a wrapper for a Twitter Developer Account using the V2 API
# https://developer.twitter.com/en/docs/twitter-api

class TwitterAccount:

    max_tweet_length = 280

    # constructor for TwitterAccount class
    # params: filename - the filename of the json file containing the credentials
    # Example:
    # account = TwitterAccount(filename="credentials.json")
    # account = TwitterAccount(bearer_token,consumer_token,consumer_secret,access_token,access_token_secret)
    # params: bearer_token - the bearer token for the Twitter Developer Account
    #         consumer_token - the consumer token for the Twitter Developer Account
    #         consumer_secret - the consumer secret for the Twitter Developer Account
    #         access_token - the access token for the Twitter Developer Account
    #         access_token_secret - the access token secret for the Twitter Developer Account

    def __init__(self, *args, **kwargs):
        if(kwargs.get("filename") != None):
            filename = kwargs.get("filename")
            self.loadcredentials_from_file(filename)
            self.init_client()
            return
        elif(kwargs.get("bearer_token") != None and kwargs.get("consumer_token") != None and kwargs.get("consumer_secret") != None and kwargs.get("access_token") != None and kwargs.get("access_token_secret") != None):
            self.bearer_token = kwargs.get("bearer_token")
            self.consumer_token = kwargs.get("consumer_token")
            self.consumer_secret = kwargs.get("consumer_secret")
            self.access_token = kwargs.get("access_token")
            self.access_token_secret = kwargs.get("access_token_secret")
            self.init_client()
            return

        if(len(args) == 1):
            filename = args[0]
            self.loadcredentials_from_file(filename)
            self.init_client()
            return
        elif(len(args) == 5):
            self.bearer_token = args[0]
            self.consumer_token = args[1]
            self.consumer_secret = args[2]
            self.access_token = args[3]
            self.access_token_secret = args[4]
            self.init_client()
            return
        else:
            raise Exception("Invalid Arguments")

    # loads the credentials from a json file and initializes the TwitterAccount
    # params: filename - the filename of the json file containing the credentials

    def loadcredentials_from_file(self, filename):
        with open(filename,"r") as f:
            data = json.load(f)
            self.bearer_token = data["bearer_token"]
            self.consumer_token = data["consumer_token"]
            self.consumer_secret = data["consumer_secret"]
            self.access_token = data["access_token"]
            self.access_token_secret = data["access_token_secret"]
            self.init_client()

    def init_client(self):
        self.client = tweepy.Client(bearer_token=self.bearer_token, consumer_key=self.consumer_token, consumer_secret=self.consumer_secret, access_token=self.access_token, access_token_secret=self.access_token_secret,wait_on_rate_limit=True)


    # deletes all the tweets from the account
    # Example:
    # account.delete_all_tweets()
            
    def delete_all_tweets(self):
        last_ten_tweets = self.client.get_users_tweets(self.client.get_me().data["id"]).data
        while last_ten_tweets != None:
            for tweet in last_ten_tweets:
                self.client.delete_tweet(tweet["id"])
            last_ten_tweets = self.client.get_users_tweets(self.client.get_me().data["id"]).data
