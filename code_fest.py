
# coding: utf-8

# In[6]:

import sys
import itertools
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
# get_ipython().magic('matplotlib inline')

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
        dic={}
        dic['text']=tweet
        dic['score']=analysis.sentiment.polarity 
        return analysis.sentiment.polarity  
        """
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        """    
        
    
            
    def get_user_timeline(self,username):
        tweets=[]
        try:

            fetched_tweets=self.api.user_timeline(screen_name=username,count=50)
            #print(type(fetched_tweets))
            #print(fetched_tweets[0].created_at)
            #print("hjjfvfe")
            count=0
            score_values=[]
            for tweet in fetched_tweets:
                parsed_tweet = {}
                count=count+1
                parsed_tweet['text'] = tweet.text
                
                w=self.get_tweet_sentiment(tweet.text)  
                score_values.append(w)
                if w > 0:
                     parsed_tweet['sentiment']='positive'                        
                elif w == 0:
                     parsed_tweet['sentiment']='neutral'
                else :
                     parsed_tweet['sentiment']='negative'               
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            #print(count)
            
            #print(type(tweets))
            #print(len(tweets))
            return  score_values , tweets
        
        except tweepy.TweepError as e:
            print("Error : " + str(e))
            
plot1=  [ ]           
scores1 = []
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    #tweets = api.get_tweets(query = 'Donald Trump', count = 20)
    # scores , tweets = api.get_user_timeline(sys.argv[1])
    scores , tweets = api.get_user_timeline('ChesterBe')
    #for tweet in tweets:
        #print(tweet)
    
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    print("Neutral tweets percentage: {}  %".format((100* (len(tweets)- len(ntweets) -len(ptweets))/len(tweets))))
    
    # printing first 5 positive tweets
    stor=[]
    #print("lentgth is " , len(tweets) , len(scores))
    for tweet , sco in zip(tweets, scores)   :
        plot1.append(sco)
        if tweet['sentiment'] == 'positive':
            #print("positive tweet score is " , sco )
            #print("tweet is " , tweet)
            stor.append(1)
            
        elif tweet['sentiment']=='negative':
            #print("negative tweet score is " , sco )
            #print("tweet is " , tweet)
            stor.append(-1)
        else:
            stor.append(0)
            #print("neutral tweet score is " , sco )
            #print("tweet is " , tweet)
    #print(stor)
    #plt.ylabel('some numbers')
    #plt.plot(stor)
    #plt.show()
    #plt.savefig('books_read.png')
    """
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
          print(tweet['text'])
        
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
          print(tweet['text']) 
    """
    
    poly_deg = 18

    plt.ylabel('Emotional condition')
    #plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
    
    
    y=plot1
    y=y[::-1]
    x = np.arange(0, 2*(np.pi), 0.1)[0:len(y)]
    y_knots = y
    x_knots=x
    coefs = np.polyfit(x_knots, y_knots, poly_deg)
    y_poly = np.polyval(coefs, x)
    
    #plt.plot(x_knots, y_knots, "o", label="data points")
    plt.plot(x, y_poly, label="polynomial fit")
    plt.fill_between(x_knots, 0, y_poly)
    plt.ylabel( 'Emotional Condition' )
    plt.xlabel('Time')
    plt.savefig('plotted_graph.png')
if __name__ == "__main__":
    # calling main function
    main()

