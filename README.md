# RedditDataMiner
To run the script you must have the following libraries installed for Python 3.4
  PRAW
  BeautifulSoup
  
To get a return from our classifer run the trainer.py in the src folder.
trainer.py is set to use the datascraper to create a training set, based on the current posts on reddit.
It will then run a static test set, comprised of reddit posts that will not have further changes.
The output of the trainer.py will be an array tuples like the following:
  [('science',[('cooking',X),('science',Y)])]

The main function of the trainer.py is train(urls, subreddit).
urls is an array of tuples (subreddit post is found, url to reddit post), and subreddit is an array of subreddit to build a frequency wordbank for.
the postscraper of the datascraper.py will take the urls and find the words for post, which will be ran against the wordbanks.
This is to determine their scores.
To change the test set, change the array of urls to contain the chosen posts.
To change the number of class change the subreddit array to contain the classes you would wish to label.

To get a sorted data and the number of correct matches for the run follow instructions.
In post_bar_grapher.py change data to the output of trainer.py. run post_bar_grapher.py
its out will be the number of correct matches and the sorted data showing the frequencies for subreddit ih highest to lowest order.
