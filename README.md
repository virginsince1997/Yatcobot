# Yatcobot
Will poll for Retweet Contests and retweet them. Inspired by http://www.hscott.net/twitter-contest-winning-as-a-service/

A more acceptable use of this kind of app may involve using to search for philanthropic causes requesting retweets, and retweet less often so as not to seem spammy.

[![Build Status](https://travis-ci.org/buluba89/Yatcobot.svg)](https://travis-ci.org/buluba89/Yatcbot)
[![codecov.io](http://codecov.io/github/buluba89/Yatcobot/coverage.svg?branch=master)](http://codecov.io/github/buluba89/Yatcobot?branch=master)


Disclaimer!
------------

This bot is written purely for educational purposes. I hold no liability for what you do with this bot or what happens to you by using this bot. Abusing this bot *can* get you banned from Twitter, so make sure to read up on [proper usage](https://support.twitter.com/articles/76915-automation-rules-and-best-practices) of the Twitter API.

License
------------

This program is released under GPL v2

Prerequisites
------------

  * TwitterAPI
  * Python 3.4
  
Configuration
------------

Open up `config.json` and make the values correspond to your Twitter API credentials.

Installation
------------
From the command line:

	pip3 install -r requirements.txt 
	
Then run:

	python3 yatcobot.py


## Usage with Docker

To run container use like below

    $ docker run -v /path/to/config.json:/yatcobot/config.json buluba89/Yatcobot

where /path/to/config.json is the path of your config.json



Credits
-----------
>Forked from [ModusVivendi/twitter-contest](https://github.com/ModusVivendi/twitter-contest)


>Original project [kurozael/twitter-contest-bot](https://github.com/kurozael/twitter-contest-bot)

