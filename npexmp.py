import os
from gtts import gTTS

import feedparser as fp
import json
import codecs
import newspaper
from newspaper import Article

from time import mktime
from datetime import datetime

import playsound

#Set the limit for number of atricles to download
LIMIT = 5
c = 1

data = {}
data['newspapers'] = {}

#Loads the Json files with news sites 
companies = json.load(codecs.open('NewsPapers.json', 'r', 'utf-8-sig'))

count = 1

# Iterate through each news company
for company, value in companies.items():
    # If a RSS link is provided in the JSON file, this will be the first choice.
    # Reason for this is that, RSS feeds often give more consistent and correct data.
    # If you do not want to scrape from the RSS-feed, just leave the RSS attr empty in the JSON file.
    if 'rss' in value:
        d = fp.parse(value['rss'])
        #print("Downloading articles from ", company)
        newsPaper = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            # Check if publish date is provided, if no the article is skipped.
            # This is done to keep consistency in the data and to keep the script from crashing.
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                #print("Downloading articles from ", company)
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading
                    # the next article.
                    print("An error occured. continuing...")
                    continue
                # Seperating the news headlines and printing it
                article['title'] = content.title
                print(article['title'], "\n")

                # Seperating the complete news
                article['text'] = content.text

                #Converting the seperated news headlines to speech or audio
                mytext = article['title']
                tts = gTTS(text = mytext, lang = 'en', slow = False)
                fname1 = 'headline' + str(c) + '.mp3'
                tts.save(fname1)
                
                # Playing the converted news headlines to the user
                playsound.playsound(fname1, True)

                c = c + 1
                
                count = count + 1 
