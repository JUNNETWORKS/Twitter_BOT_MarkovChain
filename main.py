import sys
sys.path.append("TextGenerator/")
from PrepareChain import PrepareChain
from GenerateText import GenerateText
import MeCab
import tweepy
import time
import datetime
from make_data_set import my_tweet, tl_tweet

# ツイートデータを一つの文章にまとめる
def read_tweet():
    with open("Tweet_data.txt","r") as tf:
        line = tf.read()
        line = line.replace("\n", "。")
    return line

# マルコフ連鎖-準備
def markov_set(line):
    text = line
    chain = PrepareChain(text)
    triplet_freqs = chain.make_triplet_freqs()
    chain.save(triplet_freqs, True)
line = read_tweet()
markov_set(line)

# マルコフ連鎖-実行
def markov():
    generator = GenerateText()
    return generator.generate()


# Tweepyの設定
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

day = datetime.date.today()
while True:
    Tweet = markov()
    Tweet = Tweet.replace("。","")
    if len(Tweet) < 140:
        api.update_status(status=Tweet)
        print(Tweet)
    else:
        continue
    if datetime.date.today() == day + datetime.timedelta(days=1):
        day+=datetime.timedelta(days=1)
        tl_tweet(50)
        tw = read_tweet()
        markov_set(tw)
    else:
        pass
    time.sleep(3600)

#if __name__ == "__main__":
#    print(markov())
