#!/usr/bin/env python
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import sys
#%matplotlib inline
class TwitterClient(object): 
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        consumer_key = 'q5KDm8mFYGuX5ofde3hGhbk13'
        consumer_secret = 'cpES4YMGDhX1n1qLfjbqtjL4iYvdbzQYLm5nJWFzbgSJJ4JUgQ'
        access_token = '4690057452-8oNgkeUKaIHOZPdwSK9jNPEdSVTkbEMSNHaHJhg'
        access_token_secret = 'mQtDVFE7vX8suAywV6cFQPAJOvSVeoLJ8cRqiaXRvP3nF'
        
        # attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
            
    def get_user_timeline(self,username):
        tweets=[]
        try:

            fetched_tweets=self.api.user_timeline(screen_name=username,count=25)
            # print(type(fetched_tweets))
            # print(fetched_tweets[0].created_at)
            # print("hjjfvfe")
            count=0
            for tweet in fetched_tweets:
                parsed_tweet = {}
                count=count+1
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            # print(count)
            
            # print(type(tweets))
            # print(len(tweets))
            return tweets
        
        except tweepy.TweepError as e:
            print("Error : " + str(e))

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    #tweets = api.get_tweets(query = 'Donald Trump', count = 20)
    tweets = api.get_user_timeline(sys.argv[1])

    #for tweet in tweets:
        #print(tweet)
    
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # print("Neutral tweets percentage: {}  %".format((100* (len(tweets)- len(ntweets) -len(ptweets))/len(tweets))))
    
    # printing first 5 positive tweets
    stor=[]
    for tweet in tweets:
        if tweet['sentiment'] == 'positive':
            stor.append(1)
        elif tweet['sentiment']=='negative':
            stor.append(-1)
        else:
            stor.append(0)
    # print(stor)       
    plt.plot(stor)
    plt.savefig('user_plot.png')
    plt.close()
    # print("\n\nPositive tweets:")
    # # for tweet in ptweets[:10]:
    # #       print(tweet['text'])
        
    # # printing first 5 negative tweets
    # print("\n\nNegative tweets:")
    # for tweet in ntweets[:10]:
    #       print(tweet['text']) 


if __name__ == "__main__":
    # calling main function
    main()
