from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
from transformers import pipeline
import time
import requests


loops = input('[+] Enter loop: ')
smth = input('[+] Enter query: ')
fst = 0
# ye still put your client id and secret

analyzer = pipeline("sentiment-analysis")

def to_temperature(label, score):
    return score if label == "POSITIVE" else 1 - score

gproxy = requests.get('https://crimson-term-ce6d.kingcrtis1.workers.dev/')
proxy = gproxy.text
print(proxy)


def crawl(query, api_key):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    youtube = build("youtube", "v3", developerKey=api_key)
    count = 0
    titemp = 0
    textemp = 0
    
    request = youtube.search().list(
        part="snippet",
        q=query,  
        maxResults=5,
        type="video"
    )
    response = request.execute()


    for item in response["items"]:
        video_id = item["id"]["videoId"]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
        for entry in transcript:
            print(f"{entry['start']:.2f}s: {entry['text']}")
            reself = analyzer(transcript[:500])
            text_temperature = to_temperature(reself[0]["label"], reself[0]["score"])
            count += 1
            textemp += text_temperature
            atext = textemp / count
            return(textemp)
    

for i in range(int(loops)):
    f = crawl(smth, "")
    fst += f

print(f'temperature: {fst / int(loops)}')
