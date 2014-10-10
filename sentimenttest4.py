import time
import praw
import json

from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import random
from nltk.corpus import movie_reviews
#from nltk.corpus import wordnet

random.seed(1)
r = praw.Reddit('PRAW Bot Obama Comments')
#r.login()
already_done = set()

#first print
fp = open('Links_v1.txt', 'wb')

#second print
sp = open('SentimentOut_v1.txt','wb')

#lookWords = ['Obama']
subreddit = r.get_subreddit('Obama')
for submission in subreddit.get_hot(limit=5):
	op_text = submission.selftext.lower()
	#op_text = submission.selftext
	#has_lookWords = any(string in op_text for string in lookWords)
	# Test if it contains a PRAW-related question
	if submission.id not in already_done: #and has_lookWords:
		already_done.add(submission.id)
		print "Found a message with lookWord"
		#print submission.short_link
		fp.write('\n' + "Title of Page: " + submission.title.encode('utf-8') + '\n')
		fp.write("Link of Page: " + submission.short_link + '\n')
		selftxt = submission.selftext.encode('utf-8').strip()
		fp.write("Body of Page Below: " + '\n' + selftxt + '\n')
		fp.write("- End of Body - " + '\n')
		
		submission2 = r.get_submission(submission_id =submission.id)
		submission2.replace_more_comments(limit=16,threshold=10)
		flat_comments = praw.helpers.flatten_tree(submission2.comments)
		i = 0
		sp.write("Flat Tree Length: "+str(len(flat_comments))+'\n')
		print "Flat Tree Length: "+str(len(flat_comments))
		for comment in flat_comments:
			i = i +1
			#sometimes there will be no text in the comment body
			if "Obama" in comment.body:
				print str(i) + "th one had a 'Obama' in the comment body!"
				#if comment.body not in comments_found:
					#print str(comment.body)
				blob = TextBlob(comment.body)
				sp.write("Comment: "+str(blob)+'\n')	
				#prob_dist = cl.prob_classify(blob)
				#sp.write("Pos Prob: "+ str(prob_dist.prob("pos"))+'\n')
				#sp.write("Neg Prob: "+ str(prob_dist.prob("neg"))+'\n')
				for s in blob.sentences:
					sp.write("Sentence: "+str(s)+'\n')
					sp.write("Polarity: "+str(s.sentiment.polarity)+'\n')
					sp.write("Subjectivity: "+str(s.sentiment.subjectivity)+'\n')
			else:
				print "No body for comment"
