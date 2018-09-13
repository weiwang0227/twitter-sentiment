import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    keys = loadkeys(twitter_auth_filename)
    consumer_key = keys[0]
    consumer_secret = keys[1]
    access_token = keys[2]
    access_token_secret = keys[3]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """

    ret_user_info = dict()
    tweets = []
    user = api.get_user(name)
    ret_user_info['user'] = user.screen_name
    ret_user_info['count'] = user.statuses_count
    analyzer = SentimentIntensityAnalyzer()
    raw_tweets = api.user_timeline(screen_name = name,count=100)
    for raw_tweet in raw_tweets:
        tweet = dict()
        tweet['id'] = raw_tweet.id_str
        tweet['created'] = raw_tweet.created_at.date()
        tweet['retweeted'] = raw_tweet.retweet_count
        tweet['text'] = raw_tweet.text
        tweet['hashtags'] = [ raw_tweet.entities[u'hashtags'][i][u'text'] for i in range(len(raw_tweet.entities[u'hashtags'])) ]
        tweet['urls']     = [ raw_tweet.entities[u'urls'][i][u'expanded_url'] for i in range(len(raw_tweet.entities[u'urls'])) ]
        tweet['mentions'] = [ raw_tweet.entities[u'user_mentions'][i][u'screen_name'] for i in range(len(raw_tweet.entities[u'user_mentions'])) ]
        tweet['score']    = analyzer.polarity_scores(raw_tweet.text)['compound']
        tweets.append(tweet)
    ret_user_info['tweets'] = tweets

    return ret_user_info


def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    friend_info_list = []

    for friend in tweepy.Cursor(api.friends, screen_name=name).items():
        friend_dict = {}
        friend_dict['name'] = friend.name
        friend_dict['screen_name'] = friend.screen_name
        friend_dict['followers'] = friend.followers_count
        friend_dict['created'] = friend.created_at.date()
        friend_dict['image'] = friend.profile_image_url_https
        friend_info_list.append(friend_dict)

    return friend_info_list

if __name__ == '__main__':
    api = authenticate('twitter.csv')
    user = api.get_user('the_antlr_guy')

    friends = fetch_following(api, 'the_antlr_guy')
    for key in friends:
        print key, friends[key][0], friends[key][1], friends[key][2], friends[key][3], friends[key][4]
