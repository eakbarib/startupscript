class TwitterBot:

    # constructor for TwitterBot class
    # params: twitter_account - the twitter account to post tweets to
    #         openai_key - the openai key to use to get startup scripts
    # Example:
    # bot = TwitterBot(twitter_account,openai_key)
    
    def __init__(self,twitter_account):
        self.twitter_account = twitter_account

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
        return self.twitter_account.create_tweet(text=tweet, in_reply_to_tweet_id=reply_tweet_id)

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