#Imports datascraper module, nltk for stopwords, and ordered dicts to order
import DataScraper
import nltk
from operator import itemgetter
from collections import OrderedDict

#urls = array of pairs (subreddit,url) Allows us to output results telling us where each subreddit the links came from
#subreddits = array of subreddits //15 subreddits we use for testing
def trainer(urls, subreddits):
    #Post_word_bank is an array of pairs (subreddit link came from, array of words (word bank))
    #All_scores is an array of dictionaries for each url's scores for all of their subreddits
    all_scores = []
    post_word_bank =[]
    #Loop through each url, call the post_scraper to get a word bank, place that word bank into another array
    #Pairing it up 
    for s in urls:
        all_scores.append([])
        url_word_bank = DataScraper.post_scraper(s[1])
        post_word_bank.append((s[0], url_word_bank))
    
    #Loop through each subreddit and construct a frequency list using the datascraper for each one
    #From the frequency list, strip words with frequency 2 or less
    #After constructing the frequency list begin frequency testing
    for subreddit in subreddits:
        index = 0
        current_score = 0
        dictionary = DataScraper.scrape_subreddit(subreddit, 15)
        subreddit_bank = []
        for key in dictionary:
            if(dictionary[key] >= 3):
                #Subreddit word bankerino
                subreddit_bank.append(key)
        #For each post's word bank, compute the score for that subreddit
        #For each word in the post's word bank, check if it's on the subreddit's frequency list
        #If it is, then add a point to that subreddit and calculate the percentage of matching words
        #Then store that score into a dictionary that will contain all subreddit scores
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
    scores = []
    #Append the url's subreddit for better output formatting
    for i in range(0, len(urls)):
        scores.append((urls[i][0].upper(),all_scores[i]))
    print(len(post_word_bank))
    return scores

#Sample testcase, first pararameter is a array of pairs with the subreddit name and the url it came from
#Second parameter is the array of subreddits you want to check against
        
#print(trainer([("drugs","http://www.reddit.com/r/Drugs/comments/2wzg83/alaska_becomes_3rd_state_with_legal_marijuana/")],["cooking","drugs","economics","fitness","history","law","lgbt","philosophy","politics","programming","religion","science","technology","truegaming","worldnews"]))      
print(trainer([("science","http://www.reddit.com/r/science/comments/2y0k2l/science_ama_series_we_are_susannah_burrows_and"),
               ("science","http://www.reddit.com/r/science/comments/2w2gr7/a_hard_drive_made_from_dna_preserved_in_glass/"),
               ("cooking","http://www.reddit.com/r/Cooking/comments/2z19u0/shrimp_steam_vs_boil_shell_on_vs_off/"),
               ("cooking","http://www.reddit.com/r/Cooking/comments/2y8znr/what_to_do_with_duck_stock/"),
               ("drugs","http://www.reddit.com/r/Drugs/comments/2wzg83/alaska_becomes_3rd_state_with_legal_marijuana/"),
               ("drugs","http://www.reddit.com/r/Drugs/comments/2ylz75/i_have_some_shitty_news_some_of_you_might_care/"),
               ("economics","http://www.reddit.com/r/Economics/comments/2x8rye/the_simple_reason_walmart_tj_maxx_are_handing_out/"),
               ("economics","http://www.reddit.com/r/Economics/comments/2wfhn0/here_we_go_germany_stuns_markets_in_rejecting/"),
               ("fitness","http://www.reddit.com/r/Fitness/comments/2yn1qv/a_simple_diet_trick_ive_learned_from_trimming/"),
               ("fitness","http://www.reddit.com/r/Fitness/comments/2yx9el/lonely_fitness/"),
               ("history","http://www.reddit.com/r/history/comments/2yc0no/3_years_before_the_liberation_of_auschwitz_the/"),
               ("history","http://www.reddit.com/r/history/comments/2wcukp/magic_was_widely_acknowledged_in_the_old_world_is/"),
               ("law","http://www.reddit.com/r/law/comments/2w6n67/3_bank_ceos_were_summoned_by_france_for_a_trial/"),
               ("law","http://www.reddit.com/r/law/comments/2x3lqe/two_law_schools_said_this_month_that_they_would/"),
               ("lgbt","http://www.reddit.com/r/lgbt/comments/2w4427/bout_time_therapists_who_say_homosexuality_can_be/"),
               ("lgbt","http://www.reddit.com/r/lgbt/comments/2yclk8/happy_international_womens_day_to_all_women_cis/"),
               ("philosophy","http://www.reddit.com/r/philosophy/comments/2xoet7/why_our_children_dont_think_there_are_moral_facts/"),
               ("philosophy","http://www.reddit.com/r/philosophy/comments/2xwm0e/as_we_uncover_more_and_more_animals_that_possess/"),
               ("politics","http://www.reddit.com/r/politics/comments/2xnyt5/a_stunt_like_inhofe_tossing_a_snowball_on_the/"),
               ("politics","http://www.reddit.com/r/politics/comments/2ywjdo/the_new_republican_tax_plan_is_just_the_bush_tax/"),
               ("programming","http://www.reddit.com/r/programming/comments/2x5pn6/googles_atariplaying_algorithm_could_be_the/"),
               ("programming","http://www.reddit.com/r/programming/comments/2vsoql/how_a_lone_hacker_shredded_the_myth_of/"),
               ("religion","http://www.reddit.com/r/religion/comments/2y6en6/pope_denounces_throwaway_culture_that_views/"),
               ("religion","http://www.reddit.com/r/religion/comments/2yoawh/america_just_got_its_first_accredited_muslim/"),
               ("technology","http://www.reddit.com/r/technology/comments/2wpzbm/the_superfish_problem_is_microsofts_opportunity/"),
               ("technology","http://www.reddit.com/r/technology/comments/2wka4m/microsoft_has_updated_windows_defender_to_root/"),
               ("truegaming","http://www.reddit.com/r/truegaming/comments/2wfhyr/why_60/"),
               ("truegaming","http://www.reddit.com/r/truegaming/comments/2xdda0/i_played_quake_for_the_first_time_in_17_years_no/"),
               ("worldnews","http://www.reddit.com/r/worldnews/comments/2yqbqe/a_strike_at_a_chinese_factory_that_makes_shoes/"),
               ("worldnews","http://www.reddit.com/r/worldnews/comments/2xecq8/russian_opposition_politician_and_former_deputy/")
               ], 
              ["cooking","drugs","economics","fitness","history","law","lgbt","philosophy","politics","programming","religion",
              "science","technology","truegaming","worldnews"]))