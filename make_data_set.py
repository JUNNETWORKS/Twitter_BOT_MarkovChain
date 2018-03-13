# -*- coding: utf-8 -*-

import tweepy
import time

# Tweepyの設定
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
"""
# 最新の自分のツイート(RTを除く)１０件を取得しリスト化
tw_list = []
for i in range(10):
    tw = api.user_timeline()[i].text    # ツイート内容を取得
    if "RT" in str(tw):
        pass
    else:
        print(tw)
        tw = tw.replace("\n","")    # ツイート内の改行を削除
        tw_list.append(tw)          # ツイートをリストに追加

# 現在txtファイル内にある文章を改行で分けてリスト化
txt = []
for i in open("Tweet_data.txt","r"):
    i = i.replace("\n","")  # 改行記号を消す
    txt.append(i)           # リストに追加

with open("Tweet_data.txt", "a") as tf:
    for i in range(len(tw_list)):   # 取得したツイート数の分だけ繰り返す
        if str(tw_list[i]) in txt:  # 既にtxt内に同じ文章がある場合は追加しない
            pass
        else:
            if "https" in tw_list[i]:   # 画像つきやURL付きは書き込まない(後に単語を切り出す際にややこしいから)
                pass
            else:
                tf.write(tw_list[i]+"\n")   # txtファイルに書き込み
"""
#上記の改良版
def tweet_get(tw_num):  # tw_num: 取得したいツイート数
    i = 1
    with open("Tweet_data.txt", "a+") as tf:
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                #tf.write(str(status.text))
                status = str(status.text).replace("\n","")    # ツイート内の改行を削除
                if "RT" in status:  # RTは書き込まない
                    pass
                elif "https" in status: # 画像つきやURL付きツイートを書き込まない
                    pass
                elif "@" in status: # リプの場合はIDを取り除いて書き込む
                    status = status[status.find(" ")+1:] # "@"から" "インデックスを取得してそれ以降の部分のみ取得
                    tf.write(status+"\n")
                    print("Step%d: %s"%(i, status))   # txtファイルに書き込まれたツイートを表示
                    i += 1
                elif i == tw_num+1:   # 指定回数までツイートを取得したら終了する
                    break
                else:
                    tf.write(status+"\n")
                    print("Step%d: %s"%(i, status))   # txtファイルに書き込まれたツイートを表示
                    i += 1
            except UnicodeEncodeError:  # 実行していると突然UnicodeEncodeErrorが出るが続ける
                pass

if __name__ == "__main__":  # コマンドプロンプトから呼び出された場合のみ実行
    tw_num = int(input("取得したいツイート数を入力してください: "))
    tweet_get(tw_num)
