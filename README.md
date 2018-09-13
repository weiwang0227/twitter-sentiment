# Overview

The goal of this project is to demonstrate how to pull twitter data, using the [tweepy](http://www.tweepy.org/) wrapper around the twitter API, and how to perform simple sentiment analysis using the [vaderSentiment](https://github.com/cjhutto/vaderSentiment) library.  The tweepy library hides all of the complexity necessary to handshake with Twitter's server for a secure connection.

It also produces a web server running at AWS to display the most recent 100 tweets from a given user and the list of users followed by a given user. For example, in response to URL `/realDonaldTrump`, the web server should respond with a tweet list color-coded by sentiment, using a red to green gradient:

<img src=images/trump-tweets.png width=750>
