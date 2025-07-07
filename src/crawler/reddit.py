import praw
from dotenv import load_dotenv
import os
from transformers import pipeline
import time


# put your client id and secret in the code pls!!!!

loops = input('[+] Enter loop: ')
smth = input('[+] Enter query: ')
fst = 0

analyzer = pipeline("sentiment-analysis")

def to_temperature(label, score):
    return score if label == "POSITIVE" else 1 - score

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="realfeel"
)

def crawl(query):
    count = 0
    titemp = 0
    textemp = 0
    
    results = reddit.subreddit("all").search(query, limit=75, sort="relevance")


    for post in results:
        if post.selftext.strip():
            reself = analyzer(post.selftext[:500])
            text_temperature = to_temperature(reself[0]["label"], reself[0]["score"])
            restitle = analyzer(post.title[:500])
            title_temperature = to_temperature(restitle[0]["label"], restitle[0]["score"])
            count += 1
            titemp += title_temperature
            textemp += text_temperature
            atext = textemp / count
            atite = titemp / count
            orall = atext + atite
            return(orall / 2)
    

for i in range(int(loops)):
    f = crawl(smth)
    fst += f

print(f'temperature: {fst / int(loops)}')
