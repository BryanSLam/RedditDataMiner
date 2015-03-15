#For assignment 2, the trainer used pairs with (features[dictionary], subreddit) 
#The post should be fed in through its url or some form
#subreddits is a list of subreddits (strings) you want to build the trainer off of
import DataScraper
import nltk
from operator import itemgetter
from collections import OrderedDict

def trainer(url, subreddits):
    #Post word bank should be an array of words that comes from the post we're testing
    post_word_bank = DataScraper.post_scraper("http://www.reddit.com/r/science/comments/2y0k2l/science_ama_series_we_are_susannah_burrows_and/")
    
    
    #So heres my current strategy to analyze posts ONLY using the frequency
    #We can do another one using the nltk classifier if time given, but feel free
    #to modify the frequencey one
    
    #Side note: I decided to split the two algorithims because the classifier looks much
    #more effective if we have some way to classify each subreddit as a dictionary of
    #its properties, in assignment 2 each entry to the training_set was something like
    #({first_letter: a, last_letter: b.. etc}, male) to do this for a reddit post itd be something
    #like ({word_in_post: 'cook', domain: 'welovescience', type:'link', etc}, science) there 
    #isn't much variety and I don't know if itd be possible to have a bunch training_set 
    #entries where the dictionary looked like ({word_from_text:science, word_from_text: 
    #physics,word_from_text: star}, science) it's hard to tell how to split up the post
    #because our strength lies in knowing what words are in the post
    
    #FREQUENCY ALGORITHIM
    #From what I can tell, it looks like words with a frequency of 3 (maybe try 2) or more are
    #words that are very subject centric (I ran the scraper on cooking and words with
    #frequency 3 are stuff like 'toast' 'bowl' 'sour') so in light of this I want to
    #assign a scoring system where we use the words with frequencey 3 or more
    #and loop through the post's word bank and for every word that matches up is one point
    #then divide that score over the total number of words in the post's word bank to get
    #a percentage
    
    #PROBLEMS: If the post we feed in has too little words, like a short title and a small
    #question then there's a chance no words will match up, in that case it'd be ideal
    #that we have another way to classify posts
    
    #Also we need to decide if maybe we should give more points if the word
    #had a higher frequency in the subreddit, for now just 1 point each
    
    #FREQUENCY ALGORITHIM CODE:
    #Loop through the list of subreddits and for each one assign a score
    subreddit_scores = {}
    for subreddit in subreddits:
        current_score = 0
        dictionary = DataScraper.scrape_subreddit(subreddit, 25)
        subreddit_bank = []
        for key in dictionary:
            if(dictionary[key] >= 2):
                #Subreddit word bankerino
                subreddit_bank.append(key)
        for word in post_word_bank:
            #If the word is in the bank add a point
            if(word in subreddit_bank):
                current_score = current_score + 1
        
        #Calculate as a percentage
        current_score = (current_score/len(post_word_bank)) * 100
        subreddit_scores[subreddit] = current_score
        
    sorted_subreddit_scores = OrderedDict(sorted(subreddit_scores.items(), key = itemgetter(1),reverse = True))
    return sorted_subreddit_scores

    #Classifier save for you guys tomorrow to think of a way you want to do this, 
    #or we can do it as a group
    #classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        
print(trainer("", ["science","cooking","politics", "worldnews", "truegamers", 
                   "history", "religon","economics","programming"]))