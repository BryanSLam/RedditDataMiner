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
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


def is_self_post(domain):
    if(domain[:5] == "self."):
        return True
    else:
        return False

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
            
    #
    for word in word_bank:
        if word in word_count.keys():
            word_count[word] += 1
        else:
            word_count[word] = 1
            
    sorted_word_dict = OrderedDict(sorted(word_count.items(), key = itemgetter(1),reverse = True))
        
    subreddit_file = open(subreddit,'w')
    subreddit_file.write(str(sorted_word_dict))
    
    X = np.arange(len(sorted_word_dict))
    pl.bar(X,sorted_word_dict.values(),align='center',width=0.5)
    pl.xticks(X,sorted_word_dict.keys())
    ymax = max(sorted_word_dict.values())+1
    pl.ylim(0,ymax)
    pl.show()

        
            #TODO: Get the text from the website here
    return sorted_word_dict
print(scrape_subreddit("science", 100))
    

