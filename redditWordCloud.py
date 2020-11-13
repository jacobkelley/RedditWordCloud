#!/usr/bin/python

### --------------------------------->>> Imports <<<---------------------------------   ###
import praw
import os
import pdb
import re
import sys, getopt
# Imports for wordcloud
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt

### --------------------------------->>> Functions <<<---------------------------------   ###


def checkArgs():
    def printAndExit():
        print("Usage: test.py -s <subreddit>  -t <posttypes> -n <numberofposts>")
        print("       posttypes are new, hot, top, or rising")
        print("       numberofposts must be above 0 and below 101")
        sys.exit()

    ## Ensure that the first argument is not blank
    if len(sys.argv) < 2:
        printAndExit()

    ## Check to ensure each argument is in the correct order
    try:
        if sys.argv[1] == "-s" and sys.argv[3] == "-t" and sys.argv[5] == "-n":
            pass
        else:
            printAndExit()
    except:
        printAndExit()

    ## Make sure they supplied the subreddit name.  If so, set variable called subreddit
    try:
        global subreddit
        if sys.argv[1] == "-s":
            if sys.argv[2]:
                subreddit = sys.argv[2]
            else:
                subreddit = input("Please enter the subreddit name.")
        else:
            printAndExit()
    except:
        printAndExit()

    ## Make sure they supplied type of subreddit. If so, set variable called sorttype
    try:
        global sorttype
        if sys.argv[3] == "-t":
            if sys.argv[4] == "new" or sys.argv[4] == "hot" or sys.argv[4] == "top" or sys.argv[4] == "rising" or sys.argv[4] == "New" or sys.argv[4] == "Hot" or sys.argv[4] == "Top" or sys.argv[4] == "Rising":
                sorttype = sys.argv[4]
            else:
                sorttype = input("What type of sort do you want (hot, new, top, or rising):\n")
        else:
            printAndExit()
    except:
        printAndExit()

    ## Make sure they supplied number of posts to look at
    try:
        global sortlimit
        if sys.argv[5] == "-n":
            if int(sys.argv[6]) > 0 and int(sys.argv[6]) < 101:
                sortlimit = int(sys.argv[6])
            else:
                sortlimit = input("Please enter the proper number of posts to check.  This must be more than 0 and less than 100.")
        else:
            printAndExit()
    except:
        printAndExit()

    ## Make sure there are exactly 7 arguments (not too many...)
    try:
        if len(sys.argv) == 7:
            pass
        else:
            printAndExit()
    except:
        printAndExit()

### --------------------------------->>> Main Loop <<<---------------------------------   ###

def main():
    ### --------------------------------->>> Gather data <<<---------------------------------   ###
    commonwords = "the","be","to","of","and","a","in","that","have","I","it","for","not","on","with","he","as","you","do","at","this","but","his","by","from","they","we","say","her","she","or","an","will","my","one","all","would","there","their","what","so","up","out","if","about","who","get","which","go","me","when","make","can","like","time","no","just","him","know","take","people","into","year","your","good","some","could","them","see","other","than","then","now","look","only","come","its","over","think","also","back","after","use","two","how","our","work","first","well","way","even","new","want","because","any","these","give","day","most","us"

    ### --> Setting bot and subreddit info
    reddit = praw.Reddit(user_agent='WordCloudBot v0.1',
                        client_id='blah', client_secret='abc123',
                        username='need_to_update_this', password='aaaaaaaa')

    words = []

    ### --> Get submissions from subreddit hot to parse for wordcloud
    if sorttype == "Hot" or sorttype == "hot":
        for submission in reddit.subreddit(subreddit).hot(limit=sortlimit):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                commentwords = re.findall(r'\s|,|[^,\s]+', comment.body) 
                for word in commentwords:
                    words.append(word)

    ### --> Get submissions from subreddit new to parse for wordcloud
    elif sorttype == "New" or sorttype == "new":
        for submission in reddit.subreddit(subreddit).new(limit=sortlimit):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                commentwords = re.findall(r'\s|,|[^,\s]+', comment.body)
                for word in commentwords:
                    words.append(word)

    ### --> Get submissions from subreddit top to parse for wordcloud
    elif sorttype == "Top" or sorttype == "top":
        for submission in reddit.subreddit(subreddit).top(limit=sortlimit):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                commentwords = re.findall(r'\s|,|[^,\s]+', comment.body) 
                for word in commentwords:
                    words.append(word)

    ### --> Get submissions from subreddit rising to parse for wordcloud
    elif sorttype == "Rising" or sorttype == "rising":
        for submission in reddit.subreddit(subreddit).rising(limit=sortlimit):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                commentwords = re.findall(r'\s|,|[^,\s]+', comment.body)
                for word in commentwords:
                    words.append(word)

    else:
        print("Something went wrong... exiting")
        sys.exit()

    ### --------------------------------->>> Calculate frequency <<<---------------------------------   ###

    ### ---> Tally up number of times a word appears
    wordcloud = {}

    ### ---> Strip out undesirable data from words
    words2 = []
    for word in words:
        if word != " ":
            w = word.strip("\"")
            w = w.strip("\n")
            w = w.strip(",")

            if w.lower() not in commonwords:
                if w not in commonwords:
                    words2.append(w)
    words = words2

    for w in words:
        wordcloud[w] = wordcloud.get(w, 0) + 1

    #Sort the dict by most occurrances first
    sortedwordcloud = sorted(wordcloud.items(), key=lambda x: (x[1],x[0]), reverse=True)


    ### --------------------------------->>> Generate command-line visualization <<<---------------------------------   ###
    index = ['Frequency']
    index2 = [1]
    df = pd.DataFrame(wordcloud, index=index)
    df2 = pd.DataFrame(sortedwordcloud, columns=['Word','frequency'])

    #Display the data
    print(df)
    print(df2)

    ### --------------------------------->>> Generate image visualization <<<---------------------------------   ###

    wordnums = [lis[1] for lis in sortedwordcloud]
    wordnames = [lis[0] for lis in sortedwordcloud]
    wordscloud = []

    #expand stocks into a cloud list
    for idx, num in enumerate(wordnums):
       for i in range(0,int(num)):
          wordscloud.append(wordnames[idx])

    listToStr = ' '.join([str(elem) for elem in wordscloud]) 

    # read stock list and define wordcloud
    df = pd.DataFrame(words)
    stopwords = set(STOPWORDS)
    wordcloud2 = WordCloud(collocations=False, width = 1200, height = 1200, background_color ='white', stopwords = stopwords, min_font_size = 10).generate(listToStr)

    # plot the WordCloud image                        
    fig = plt.figure(figsize = (8, 8), facecolor = None)
    fig.canvas.set_window_title("Looking at Reddit " + subreddit + " posts of type: " + sorttype + " sort, with " + str(sortlimit) + " post(s)")
    plt.imshow(wordcloud2)
    plt.axis("off") 
    plt.tight_layout(pad = 0)

    plt.show()

if __name__ == "__main__":
    ### --> Make sure user supplied proper arguments
    checkArgs()
    main()
