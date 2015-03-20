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
import pylab as pl
import numpy as np
from collections import OrderedDict
from operator import itemgetter
#from nltk.corpus import stopwords
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
    #create the data containers and delimiters
    #With self-text posts, the return key is often used multiple times for formatting
    #So we had to remove any instances of '\n' that our scrapper might grab
    #To simplify the words in the word bank, we chose to remove all hyphend words and take each word seperately.
    word_bank = []
    word_count = {}
    bad_char = '[(){}<>*?&,.!=+-;:%"]'
    return_keys = '\n'
    interesting_char = '–'
    
    #stopWords = stopwords.words('english')    
    stopWords = []
#using a larger set of english stop words 
    f = open('english_stop_words.txt')
    for word in f.read().split():
        stopWords.append(word)
    f.close()
    #print(stopWords)
    r = praw.Reddit(user_agent='Post_Parser')
    word_bank = []
    submission = r.get_submission(url)
    
    #Parse
    #For submission titles and self-text, we need to first split all words seperated by a space into individual tokens
    #following this, we need to filter certain characters, such as the bad characters and the hyphen, and replace them with an empty string
    #then change all the texts into lower case
    #Next we check if the word is in the list of stop words and isn't an empty string, where if it isn't we add it to the list for total words
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
#        texts = soup.find_all(text=True)
#        visible_texts=filter(visible,texts)
#        for item in visible_texts:
#            for s in item.split(' '):
#                s = re.sub(bad_char,"",s)
#                s = re.sub(return_keys,"",s)
#                s = re.sub(interesting_char,"",s)
#                s = s.lower()
#                if s not in stopWords and s != '':
#                    word_bank.append(s)
        paragraphTag = soup.find_all('p')
        for item in paragraphTag:
            for word in item.find_all(text=True):
                for s in word.split():
                    s = re.sub(bad_char,"",s)
                    s = re.sub(return_keys,"",s)
                    s = re.sub(interesting_char,"",s)
                    s = s.lower()
                    if s not in stopWords and s != '':
                        word_bank.append(s)
        req.connection.close()
    return word_bank

def scrape_subreddit(subreddit, num_posts):
    #With self-text posts, the return key is often used multiple times for formatting
    #So we had to remove any instances of '\n' that our scrapper might grab
    #To simplify the words in the word bank, we chose to remove all hyphend words and take each word seperately.
    word_bank = []
    word_count = {}
    bad_char = '[(){}<>*?&,.!=+-;$:%"]'
    return_keys = '\n'
    interesting_char = '–'
    stopWords=[]
    r = praw.Reddit(user_agent='Wordsszzz')
    sr = r.get_subreddit(subreddit)
    f = open('english_stop_words.txt')
    for word in f.read().split():
        stopWords.append(word)
    f.close
    #print(stopWords)
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
        
        #For submission titles and self-text, we need to first split all words seperated by a space into individual tokens
        #following this, we need to filter certain characters, such as the bad characters and the hyphen, and replace them with an empty string
        #then change all the texts into lower case
        #Next we check if the word is in the list of stop words and isn't an empty string, where if it isn't we add it to the list for total words        
        
        #Get the title of the submission        
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
#            texts = soup.find_all(text=True)
#            visible_texts=filter(visible,texts)
#            for item in visible_texts:
#                for s in item.split(' '):
#                    s = re.sub(bad_char,"",s)
#                    s = re.sub(return_keys,"",s)
#                    s = re.sub(interesting_char,"",s)
#                    s = s.lower()
#                    if s not in stopWords and s != '':
#                        word_bank.append(s)
            paragraphTag = soup.find_all('p')
            for item in paragraphTag:
                for word in item.find_all(text=True):
                    for s in word.split():
                        s = re.sub(bad_char,"",s)
                        s = re.sub(return_keys,"",s)
                        s = re.sub(interesting_char,"",s)
                        s = s.lower()
                        if s not in stopWords and s != '':
                            word_bank.append(s)
            req.connection.close()
            
    #Here is the the first iteration of the data set, a simple dictionary that uses the value as the frequency of the word
    #if it sees the word in the dictionary, it increments the frequency, otherwise it will create a new entry with a value of 1
    for word in word_bank:
        if word in word_count.keys():
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    #This is the final version of the data set, where it sorts the previous data set by the highest frequency        
    sorted_word_dict = OrderedDict(sorted(word_count.items(), key = itemgetter(1),reverse = True))
        
#    subreddit_file = open(subreddit,'w')
#    subreddit_file.write(str(sorted_word_dict))
    
#    X = np.arange(len(sorted_word_dict))
#    pl.bar(X,sorted_word_dict.values(),align='center',width=0.5)
#    pl.xticks(X,sorted_word_dict.keys())
#    ymax = max(sorted_word_dict.values())+1
#    pl.ylim(0,ymax)
#    pl.show()

        
    #TODO: Get the text from the website here
    return sorted_word_dict
#print(scrape_subreddit("programming", 25))
#print(scrape_subreddit("politics",25))   
#print(post_scraper('http://www.reddit.com/r/philosophy/comments/2xoet7/why_our_children_dont_think_there_are_moral_facts/'))
