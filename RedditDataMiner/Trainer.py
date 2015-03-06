#For assignment 2, the trainer used pairs with (features[dictionary], subreddit) 
#The post should be fed in through its url or some form
#subreddit_dict is an array of words paired with their subreddit (word, subreddit)
def trainer(url, subreddit_dict):
    #Post bank should be an array of words
    post_bank = post_scraper(url)
    
    #Classifier
    classifier = nltk.NaiveBayesClassifier.train(train_set)