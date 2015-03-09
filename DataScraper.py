# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 14:40:57 2015

@author: bryanlam
"""

#Probably need beautifulsoup for articles on sites other than reddit, praw
#can do all the scraping for reddit

#import bs4
#import urllib
import praw
import re
import sys
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
def is_self_post(domain):
    if(domain[:5] == "self."):
        return True
    else:
        return False
def visible(element):
    if element.parent.name in ['style','script','[document]','head','title']:
        return False
    elif re.match('<!--.*-->',str(element)):
        return False
    return True
#Given a post url, grab relevant words and store in a word bank
def post_scraper(url):
    word_bank = []
    word_count = {}
    bad_char = '[(){}<>*?&,.!=+-;:%"]'
    return_keys = '\n'
    interesting_char = '–'
    stopWords = stopwords.words('english')    
    
    r = praw.Reddit(user_agent='Post_Parser')
    word_bank = []
    submission = r.get_submission(url)
    
    #Parse
    for s in submission.title.split(" "):
        s = re.sub(bad_char,"",s)
        s = re.sub(interesting_char,"",s)
        s = s.lower()
        if s not in stopWords and s != '':
            word_bank.append(s)
                
            #if it's a self post
    if(is_self_post(submission.domain)):
        for s in submission.selftext.split(" "):
            s = re.sub(bad_char,"",s)
            s = re.sub(return_keys,"",s)
            s = re.sub(interesting_char,"",s)
            s = s.lower()
            if s not in stopWords and s != '':
                word_bank.append(s)
                #Its a link, grab the domain keyword then continue to scrape the site  
    else:
        d = submission.domain.split('.')
        #Grab everything except the last part of the url
        for i in range(0,len(d)-1):
            word_bank.append(d[i])
        url = submission.url
        req = requests.get(url)
        soup = BeautifulSoup(req.content)
        texts = soup.find_all(text=True)
        visible_texts=filter(visible,texts)
        for item in visible_texts:
            for s in item.split(' '):
                s = re.sub(bad_char,"",s)
                s = re.sub(return_keys,"",s)
                s = re.sub(interesting_char,"",s)
                s = s.lower()
                if s not in stopWords and s != '':
                    word_bank.append(s)
        req.connection.close()
    return word_bank
#Given a subreddit, grab relevant words and store in a word bank
def scrape_subreddit(subreddit, num_posts):
    word_bank = []
    word_count = {}
    bad_char = '[(){}<>*?&,.!=+-;:%"]'
    return_keys = '\n'
    interesting_char = '–'
    stopWords = stopwords.words('english')
    r = praw.Reddit(user_agent='Wordsszzz')
    sr = r.get_subreddit(subreddit)
    
    submission_list = []
    #Grab submissions from the 3 tabs might be too slow, maybe there's faster
    #way to grab stuff
    for sub in sr.get_hot(limit=num_posts):
        if((sub in submission_list) is False):
            submission_list.append(sub)
    for sub in sr.get_new(limit=num_posts):
        if((sub in submission_list) is False):
            submission_list.append(sub)
    for sub in sr.get_rising(limit=num_posts):
        if((sub in submission_list) is False):
            submission_list.append(sub)

    for submission in submission_list:
        for s in submission.title.split(" "):
            s = re.sub(bad_char,"",s)
            s = re.sub(interesting_char,"",s)
            s = s.lower()
            if s not in stopWords and s != '':
                word_bank.append(s)
                
        #if it's a self post
        if(is_self_post(submission.domain)):
            for s in submission.selftext.split(" "):
                s = re.sub(bad_char,"",s)
                s = re.sub(return_keys,"",s)
                s = re.sub(interesting_char,"",s)
                s = s.lower()
                if s not in stopWords and s != '':
                    word_bank.append(s)
        #Its a link, grab the domain keyword then continue to scrape the site  
        else:
            d = submission.domain.split('.')
            #Grab everything except the last part of the url
            for i in range(0,len(d)-1):
                word_bank.append(d[i])  
            url = submission.url
            req = requests.get(url)
            soup = BeautifulSoup(req.content)
            req.connection.close()
            texts = soup.find_all(text=True)
            visible_texts=filter(visible,texts)
            for item in visible_texts:
                for s in item.split(' '):
                    s = re.sub(bad_char,"",s)
                    s = re.sub(return_keys,"",s)
                    s = re.sub(interesting_char,"",s)
                    s = s.lower()
                    if s not in stopWords and s != '':
                        word_bank.append(s)
            
    #
    for word in word_bank:
        if word in word_count.keys():
            word_count[word] += 1
        else:
            word_count[word] = 1
        
#    subreddit_file = open(subreddit,'w')
#   for word in word_bank:
#        subreddit_file.write('%s\n' % word)
        
            #TODO: Get the text from the website here
    return word_count, word_bank
    
#def subreddit_score(word_bank, sub_top_words):
    
print (post_scraper("http://www.reddit.com/r/science/comments/2x868m/science_ama_series_im_elizabeth_iorns_breast/"))
    

