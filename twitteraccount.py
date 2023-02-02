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


    # utility method to initialize the client member variable
    # initializes the client for the TwitterAccount using the credentials
    # params: bearer_token - the bearer token for the Twitter Developer Account
    #         consumer_token - the consumer token for the Twitter Developer Account
    #         consumer_secret - the consumer secret for the Twitter Developer Account
    #         access_token - the access token for the Twitter Developer Account
    #         access_token_secret - the access token secret for the Twitter Developer Account

    def init_client(self):
        self.client = tweepy.Client(bearer_token=self.bearer_token, consumer_key=self.consumer_token, consumer_secret=self.consumer_secret, access_token=self.access_token, access_token_secret=self.access_token_secret,wait_on_rate_limit=True)




    
    # post a tweet to twitter account
    # returns the response from twitter
    # if the response has errors, the tweet was not successful
    # if the response has no errors, the tweet was successful
    # params: tweet - the tweet to post
    # returns: the response from twitter
    # Example:
    # bot = TwitterBot(twitter_account,openai_key)
    # response = bot.post_tweet("Hello World!")
    # if response.errors == None:
    #     print("Tweet was successful")
    # else:
    #     print("Tweet was not successful")

    def post_tweet(self, tweet, reply_tweet_id=None):
        return self.client.create_tweet(text=tweet, in_reply_to_tweet_id=reply_tweet_id)



       # posts a list of tweets to twitter account
    # params: tweet_series - a list of tweets to post (strings)
    # Example:
    # bot = TwitterBot(twitter_account,openai_key)
    # bot.post_tweet_series(["Hello","World!","This is a tweet series","Goodbye!"])
    # tweets:
    # Hello
    # World!
    # This is a tweet series
    # Goodbye!

    def post_tweet_thread(self, tweet_series):
        # stores the id of the last tweet posted so we can reply to it
        reply_tweet_id = None
        for tweet in tweet_series:
            # if the tweet is not empty post it otherwise skip it
            if(tweet != ""):
                reply_tweet_id = self.post_tweet(tweet, reply_tweet_id).data['id']



    # deletes all the tweets from the account
    # Example:
    # account.delete_all_tweets()
            
    def delete_all_tweets(self):
        last_ten_tweets = self.client.get_users_tweets(self.client.get_me().data["id"]).data
        while last_ten_tweets != None:
            for tweet in last_ten_tweets:
                self.client.delete_tweet(tweet["id"])
            last_ten_tweets = self.client.get_users_tweets(self.client.get_me().data["id"]).data
