""""
Question Discover Program

Tutorial program for PRAW:
See https://github.com/praw-dev/praw/wiki/Writing-A-Bot/
"""

import time
import praw
import json
#import csv

#r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
#				'Url: https://praw.readthedocs.org/en/latest/'
#				'pages/writing_a_bot.html')

r = praw.Reddit('PRAW Bot GVSU Comments with http link')

#r.login()
already_done = []
comments_found = []
csvout = []

with open('test2.csv','wb') as fp:
	#a = writer(fp, delimiter=',')
    #data = ['Me', 'You','293', '219','54', '13']
    #for x in data:
    #    a.writerows(x)

	lookWords = ['GVSU']
	subreddit = r.get_subreddit('GVSU')
	for submission in subreddit.get_new(limit=100):
		#op_text = submission.selftext.lower()
		op_text = submission.selftext
		has_lookWords = any(string in op_text for string in lookWords)
		# Test if it contains a PRAW-related question
		if submission.id not in already_done and has_lookWords:
			msg = '[Related thread](%s)' % submission.short_link
			#r.send_message('spoelee11', 'PRAW Thread', msg)
			already_done.append(submission.id)
			print "Found a message with lookWord"
			print submission.short_link
			#csvpageheader = []
			#csvpageheader.append(str(submission.title))
			#csvpageheader.append(str(submission.short_link))
			#csvpageheader.append(str(submission.selftext).encode('utf-16'))
			#csvpageheader.append(str(""))
			#a.writerow(csvpageheader)
			#csvpageheader = []
			fp.write(submission.title)
			fp.write(submission.short_link)
			fp.write(submission.selftext)
			fp.write(str(""))
			
			
			#time.sleep(1800)
			i = 0
			#forest_comments = submission.comments
			flat_comments = praw.helpers.flatten_tree(submission.comments)
			for comment in flat_comments:
				i = i + 1
				print i
				try:
					# sometimes there will be no text in the comment body
					# so we need to catch the error/warning that happens
					if str("http") in comment.body:
						#reply_world(comment)
						print i + "th one had a hyperlink!"
						if comment.body not in comments_found:
							print str(comment.body)
							comments_found.append(comment)
							#csvout = []
							#csvout.append(i + "th comment:")
							#csvout.append(comment)
							#csvout.append(" ")
							#a.writerow(csvout)
							fp.write(i + "th comment:")
							fp.write(comment)
							fp.write(" ")
							
				except:
					print "No body for comment"
				
