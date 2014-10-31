import time
import praw
import json
import csv
import os

from textblob import TextBlob
#from textblob.classifiers import NaiveBayesClassifier
import random
#from nltk.corpus import movie_reviews
#from nltk.corpus import wordnet

random.seed(1)
r = praw.Reddit('PRAW Bot Obama Comments')
r.config.store_json_result = True
#r.login()
already_done = set()

#first print
os.remove("Links_v1.txt")
fp = open('Links_v1.txt', 'wb')

#second print
os.remove("SentimentOut_v1.txt")
sp = open('SentimentOut_v1.txt','wb')

#data print
os.remove("dataprint.txt")
dp = open('dataprint.txt','a')

#lookWords = ['Obama']
subreddit = r.get_subreddit('Obama')
for submission in subreddit.get_hot(limit=10):
	op_text = submission.selftext.lower()
	#op_text = submission.selftext
	#has_lookWords = any(string in op_text for string in lookWords)
	# Test if it contains a PRAW-related question
	if submission.id not in already_done: #and has_lookWords:
		already_done.add(submission.id)
		#print "Found a message with lookWord"
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
				#print type(comment.json_dict)
				#json.dump(comment.json_dict,jp)	
				#print type(comment.json_dict)
				#jp.write(comment.json_dict)
				out = comment.body.replace("\n","")
				out2 = out.replace("&gt;","")
				dp.write(out2)
				dp.write('\n')
				#prob_dist = cl.prob_classify(blob)
				#sp.write("Pos Prob: "+ str(prob_dist.prob("pos"))+'\n')
				#sp.write("Neg Prob: "+ str(prob_dist.prob("neg"))+'\n')
				for s in blob.sentences:
					sp.write("Sentence: "+str(s)+'\n')
					sp.write("Polarity: "+str(s.sentiment.polarity)+'\n')
					sp.write("Subjectivity: "+str(s.sentiment.subjectivity)+'\n')
					for w in s.words:
						blob2 = TextBlob(w)
						sp.write("Word: "+str(blob2)+'\n')
						sp.write("Polarity: "+str(blob2.sentiment.polarity)+'\n')
						sp.write("Subjectivity: "+str(blob2.sentiment.subjectivity)+'\n')
			else:
				print "No body for comment"

fp.close()
sp.close()
dp.close()

import re

os.remove("thirdprint.txt")
dp2 = open("dataprint.txt",'rb')
tp = open("thirdprint.txt",'a')
reader = csv.reader(dp2,delimiter="\t")
for row in reader:
	comment = str(row).replace('[','').replace(']','').replace('\'','')
	blob = TextBlob(comment)
	tp.write("Comment: "+str(blob)+'\n')
	#out = comment.body.replace("\n","")
	#out2 = out.replace("&gt;","")
	#dp.write(out2)
	#dp.write('\n')
	newString = ''		
	x = []
	y = ''
	for s in blob.sentences:
		# find all "word.word"
		splitsentence = s.split()
		print splitsentence
		newSentence = []
		for word in splitsentence:
			x = re.findall('\w\.\w',word)
			if len(x) > 0:
				y = x[0]
				print y
				word2 = word.split(".")
				#word2.insert(1,".")
				firstWord = word2[0]
				secondWord = word2[1]
				firstNew = str(firstWord) + '. '
				newString = firstNew + secondWord + ''
				newSentence.append(newString)
				print newString
			else:
				newSentence.append(word)
		newSent = ' '.join(newSentence)
		blobsentence = TextBlob(newSent)		
		tp.write("Sentence: "+str(blobsentence)+'\n')
		tp.write("Polarity: "+str(blobsentence.sentiment.polarity)+'\n')
		tp.write("Subjectivity: "+str(blobsentence.sentiment.subjectivity)+'\n')
		for w in blobsentence.words:
			blob2 = TextBlob(w)
			tp.write("Word: "+str(blob2)+'\n')
			tp.write("Polarity: "+str(blob2.sentiment.polarity)+'\n')
			tp.write("Subjectivity: "+str(blob2.sentiment.subjectivity)+'\n')
	

