#For assignment 2, the trainer used pairs with (features[dictionary], subreddit) 
#The post should be fed in through its url or some form
#subreddits is a list of subreddits (strings) you want to build the trainer off of
import DataScraper
import nltk
from operator import itemgetter
from collections import OrderedDict

#urls = array of pairs (subreddit,url)
#subreddits = array of subreddits
def trainer(urls, subreddits):
    #Post word bank should be an array of pairs where the first part is the subreddit
    #and the second part is the word_bank
    all_scores = []
    post_word_bank =[]    
    for s in urls:
        all_scores.append([])
        url_word_bank = DataScraper.post_scraper(s[1])
        post_word_bank.append((s[0], url_word_bank))
    
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
    for subreddit in subreddits:
        index = 0
        current_score = 0
        dictionary = DataScraper.scrape_subreddit(subreddit, 25)
        subreddit_bank = []
        for key in dictionary:
            if(dictionary[key] >= 2):
                #Subreddit word bankerino
                subreddit_bank.append(key)
        #For each post's word bank, compute the score for that subreddit
        for bank in post_word_bank:
            current_score=0
            for word in bank[1]:
                #If the word is in the bank add a point
                if(word in subreddit_bank):
                    current_score = current_score + 1
        
                #Calculate as a percentage
            current_score = (current_score/len(bank[1])) * 100
            subreddit_score = (subreddit, current_score)                
            all_scores[index].append(subreddit_score)
            index = index+1
    scores = {}
    for i in range(0, len(urls)):
        scores[urls[i][0].upper()] = all_scores[i]
        
    return scores

    #Classifier save for you guys tomorrow to think of a way you want to do this, 
    #or we can do it as a group
    #classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        
print(trainer([("science","http://www.reddit.com/r/science/comments/2y0k2l/science_ama_series_we_are_susannah_burrows_and"),
               ("cooking","http://www.reddit.com/r/Cooking/comments/2z19u0/shrimp_steam_vs_boil_shell_on_vs_off/")], 
              ["science","cooking","politics", "worldnews"]))