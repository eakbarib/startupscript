# Description: Test the main.py file
import main
import unittest

class TestMain(unittest.TestCase):
    # Test to see the length of the script returned by OpenAI is greater than 0
    def test_get_startup_script(self):
        script = main.get_startup_script()
        self.assertGreater(len(script.choices[0].text), 0)

    # Test to see if the tweet is successful    
    def test_tweet_startup_script(self):
        tweet = main.tweet_startup_script(main.my_twitter_account)
        self.assertEqual(tweet.response.errors, None)

    def test_slice_script(self):
        script = main.get_startup_script().choices[0].text
        slices = main.slice_script(script)
        for str in slices:
            if (len(str)>279):
                self.fail("The slices tweets contain a tweet that is greater than 280 characters")
            if (len(str)==0):
                self.fail("The slices tweets contain empty string")


# Execute the tests
if __name__ == "__main__":
    unittest.main()