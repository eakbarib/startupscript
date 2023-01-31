import openai
import os
import time
from twitter_account import TwitterAccount
from twitter_bot import TwitterBot

# add your own keys and tokens here
# you can get them from https://developer.twitter.com/en/apps
# and https://openai.com/docs/developer-quickstart/api-keys
# my twitter account is @startupscript


# the interval between tweets in seconds
TWEET_INTERVAL = 0.002*3600

openai.api_key = os.getenv("OPENAI_API_KEY")

my_twitter_account = TwitterAccount(filename="Innovate_Oasis.json")
startup_twitter_bot = TwitterBot(my_twitter_account.client)

# my_twitter_account.delete_all_tweets()


# get a startup script from openai
def get_startup_script(temperature=0.9, max_tokens=3800):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Write a startup idea with steps. In the first line write the name of the startup. In the second line write the problem it solves. In the third line write the solution. In the fourth line write the market. In the fifth line write the business model. In the sixth line write the revenue model. In the seventh line write the competitive advantage. In the eighth line write the team. In the ninth line write the funding. In the tenth line write the exit strategy. In the eleventh line write the first step. In the twelfth line write the second step. In the thirteenth line write the third step. In the fourteenth line write the fourth step. In the fifteenth line write the fifth step. In the sixteenth line write the sixth step. In the seventeenth line write the seventh step. In the eighteenth line write the eighth step. In the nineteenth line write the ninth step. In the twentieth line write the tenth step. Use emojis to make the startup idea more interesting.",
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response

# slice the startup script into tweets
# returns a list of strings
# each string is a tweet
# params: script - the script to slice
# returns: a list of strings
# each string is a tweet
# Example:
# script = get_startup_script().choices[0].text
# tweets = slice_script(script)
# for tweet in tweets:
#     print(tweet)
#     print("\n")
# output:
# Write a startup idea with steps. In the first line write the name of the startup. In the second line write the problem it solves. In the third line write the solution. In the fourth line write the market. In the fifth line write the business model. In the sixth line write the revenue model. In the seventh line write the competitive advantage. In the eighth line write the team. In the ninth line write the funding. In the tenth line write the exit strategy. In the eleventh line write the first step. In the twelfth line write the second step. In the thirteenth line write the third step. In the fourteenth line write the fourth step. In the fifteenth line write the fifth step. In the sixteenth line write the sixth step. In the seventeenth line write the seventh step. In the eighteenth line write the eighth step. In the nineteenth line write the ninth step. In the twentieth line write the tenth step. Use emojis to make the startup idea more interesting.

def neat_startup_script(script):
    # script = get_startup_script().choices[0].text
    result=[]
    script_splitted = script.split("\n")
    for str in script_splitted:
        if(str=="\n" or str == ""):
            script_splitted.remove(str)

    # a while loop to slice the script into tweets
    # each tweet is at most 280 characters
    # each tweet is at least 1 line of the script
    i = 0
    while i < len(script_splitted):
        temp = ""
        while((len(temp) + len(script_splitted[i]))< TwitterAccount.max_tweet_length-1):
            temp += script_splitted[i] + "\n"
            i += 1
            if(i > len(script_splitted)-1):
                break
        result.append(temp)

    return result

# tweet the startup script
def tweet_startup_script(twitter_bot):
    script = get_startup_script().choices[0].text
    tweets = neat_startup_script(script)
    print(script)
    print(tweets)
    twitter_bot.post_tweet_thread(tweets)
    return 




if __name__ == "__main__":
    # Setting the bot to tweet every 12 hours
    current_time = time.time()
    tweet_startup_script(startup_twitter_bot)
    while True:
        if(time.time() - current_time > TWEET_INTERVAL):
            print("Tweeting")
            tweet_startup_script(startup_twitter_bot)
            current_time = time.time()
        time.sleep(TWEET_INTERVAL-10)