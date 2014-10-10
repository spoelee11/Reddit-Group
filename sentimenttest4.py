""""
https://github.com/praw-dev/praw/wiki/Writing-A-Bot/

Tutorial for Textblob
http://textblob.readthedocs.org/en/dev/api_reference.html#api-classifiers
"""

import time
import praw
import json
#import csv

from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import random
from nltk.corpus import movie_reviews
#from nltk.corpus import wordnet
random.seed(1)

r = praw.Reddit('PRAW Bot GVSU Comments with http link')

#r.login()
already_done = set()
ad2 = set()
comments_found = []

train = [
     ('I love this sandwich.', 'pos'),
     ('This is an amazing place!', 'pos'),
     ('I feel very good about these beers.', 'pos'),
     ('I do not like this restaurant', 'neg'),
     ('I am tired of this stuff.', 'neg'),
     ("I can't deal with this", 'neg'),
     ("My boss is horrible.", "neg")
]

test = [
	('The beer was good.','pos'),
	('I do not enjoy my job','neg'),
	("I ain't feeling dandy tody.",'neg'),
	("I feel amazing!",'pos'),
	("Gary is a friend of mine",'pos'),
	("I can't believe I'm doing this.",'neg')
]

cl = NaiveBayesClassifier(train)

reviews = [(list(movie_reviews.words(fileid)),category)
		for category in movie_reviews.categories()
		for fileid in movie_reviews.fileids(category)]

random.shuffle(reviews)
new_train, new_test = reviews[0:100], reviews[101:200]

#print(new_train[0])

#print cl.classify("I feel amazing")

cl.update(new_train)

#print cl.classify("I feel amazing")

#accuracy = cl.accuracy(test + new_test)
#print("Accuracy: {0}".format(accuracy))

#cl.show_informative_features(10)

cl.update(reviews[201:500])


#first print
fp = open('Links_v1.txt', 'wb')

#second print
sp = open('SentimentOut_v1.txt','wb')

#lookWords = ['Obama']
subreddit = r.get_subreddit('Obama')
for submission in subreddit.get_hot(limit=5):
	#op_text = submission.selftext.lower()
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
		for comment in flat_comments:
			i = i +1
			#sometimes there will be no text in the comment body
			# so we need to catch the error/warning that happens
			if "Obama" in comment.body:
				print str(i) + "th one had a 'Obama' in the comment body!"
				#if comment.body not in comments_found:
					#print str(comment.body)
				blob = TextBlob(comment.body,classifier=cl)
				blob2 = TextBlob(comment.body)
				sp.write("Comment: "+str(blob)+'\n')
				sp.write("Comment Class: "+str(blob.classify()) + '\n')
				
				# You need to train a classifier before you can use this next line.
				#sp.write("Comment Class #2:"+str(blob2.classify()) + '\n')

				prob_dist = cl.prob_classify(blob)
				sp.write("Pos Prob: "+ str(prob_dist.prob("pos"))+'\n')
				sp.write("Neg Prob: "+ str(prob_dist.prob("neg"))+'\n')
				
				prob_dist2 = cl.prob_classify(blob2)
				sp.write("Pos Prob #2: "+ str(prob_dist2.prob("pos"))+'\n')
				sp.write("Neg Prob:#2 "+ str(prob_dist2.prob("neg"))+'\n')		
				for s in blob.sentences:
					#print s
					#print s.classify()
					#sp.write(str(s) + '\n')
					sp.write("Sentence: "+str(s)+'\n')
					sp.write("Polarity: "+str(s.sentiment.polarity)+'\n')
					sp.write("Subjectivity: "+str(s.sentiment.subjectivity)+'\n')
					sp.write("Sent Class: "+str(s.classify())+'\n')
				for s in blob2.sentences:
					sp.write("Sentence #2: "+str(s)+'\n')
					sp.write("Polarity #2: "+str(s.sentiment.polarity)+'\n')
					sp.write("Subjectivity #2: "+str(s.sentiment.subjectivity)+'\n')
					#sp.write("Sent Class #2: "+str(s.classify())+'\n')

				#sp.write("For the text above: \n")
				#sp.write("Pos Prob: "+ str(round(prob_dist.prob("pos"),2))+'\n')
				#sp.write("Neg Prob: "+ str(round(prob_dist.prob("neg"),2))+'\n')
				#prob_dist = cl.prob_classify(s)
				#sp.write(str(prob_dist.max()) + '\n'))
				#sp.write(str(round(prob_dist.prob("pos"),2))+'\n')
				#if (str(s.classify()) == 'neg'):
				#	print str(s.classify())
		
			else:
				print "No body for comment"
print "First Try"	
blob = TextBlob("The beer was terrible.",classifier=cl)
print(blob)
print(blob.classify())
for s in blob.sentences:
	print s
	print s.sentiment.polarity
	print s.sentiment.subjectivity

blob = TextBlob("The beer was great.",classifier=cl)
print(blob)
print(blob.classify())
for s in blob.sentences:
	print s
	print s.sentiment.polarity
	print s.sentiment.subjectivity

print "Second Try"
blob2 = TextBlob("The beer was terrible.")
print(blob2)

# Can't classify if you don't use a classifier in the TextBlob creation method
#print(blob2.classify())

for s in blob2.sentences:
	print s
	print s.sentiment.polarity
	print s.sentiment.subjectivity

blob2 = TextBlob("The beer was great.")
print(blob2)

# Can't classify if you don't use a classifier
#print(blob2.classify())
for s in blob2.sentences:
	print s
	print s.sentiment.polarity
	print s.sentiment.subjectivity

print "First Try"
blob = TextBlob("I'm on your side actually!  I agree that a lot has been done, and you stated some of his biggest achievements.  It's frustrating to think that if McCain and/or Romney had been elected, and the economy had rebounded to this degree, Republicans would be treating him like a god.  But the question was why Obama is a disappointment to many people, which I gave my best answer.  (And people are clearly disappointed. Justified or not, his approval ratings aren't exactly stellar.",classifier=cl)
print("I'm on your side actually!  I agree that a lot has been done, and you stated some of his biggest achievements.  It's frustrating to think that if McCain and/or Romney had been elected, and the economy had rebounded to this degree, Republicans would be treating him like a god.  But the question was why Obama is a disappointment to many people, which I gave my best answer.  (And people are clearly disappointed. Justified or not, his approval ratings aren't exactly stellar.")
print(blob.classify())
for s in blob.sentences:
	print s
	print s.sentiment.polarity
	print s.sentiment.subjectivity

print "Second Try"
blob2 = TextBlob("I'm on your side actually!  I agree that a lot has been done, and you stated some of his biggest achievements.  It's frustrating to think that if McCain and/or Romney had been elected, and the economy had rebounded to this degree, Republicans would be treating him like a god.  But the question was why Obama is a disappointment to many people, which I gave my best answer.  (And people are clearly disappointed. Justified or not, his approval ratings aren't exactly stellar.")
#print("I'm on your side actually!  I agree that a lot has been done, and you stated some of his biggest achievements.  It's frustrating to think that if McCain and/or Romney had been elected, and the economy had rebounded to this degree, Republicans would be treating him like a god.  But the question was why Obama is a disappointment to many people, which I gave my best answer.  (And people are clearly disappointed. Justified or not, his approval ratings aren't exactly stellar.")
#print(blob2.classify())
for s in blob2.sentences:
	print s
	print s.sentiment.polarity
	print s.sentiment.subjectivity


#print("Accuracy: {0}".format(cl.accuracy(reviews[501:700])))

#cl.show_informative_features(5)
