""""
Question Discover Program

Tutorial program for PRAW:
See https://github.com/praw-dev/praw/wiki/Writing-A-Bot/
"""

import time
import praw
import csv

#r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
#				'Url: https://praw.readthedocs.org/en/latest/'
#				'pages/writing_a_bot.html')

r = praw.Reddit('PRAW Bot GVSU Comments with http link')

#r.login()
already_done = []
csvout = []

with open('test2.csv','wb') as fp:
	a = csv.writer(fp, delimiter=',')
    #data = ['Me', 'You','293', '219','54', '13']
    #for x in data:
    #    a.writerows(x)

	prawWords = ['Hillcrest']
	subreddit = r.get_subreddit('GVSU')
	for submission in subreddit.get_new(limit=100):
		op_text = submission.selftext.lower()
		has_praw = any(string in op_text for string in prawWords)
		# Test if it contains a PRAW-related question
		if submission.id not in already_done:
			msg = '[PRAW related thread](%s)' % submission.short_link
			#r.send_message('spoelee11', 'PRAW Thread', msg)
			already_done.append(submission.id)
			print "Sent a message"
		#time.sleep(1800)
		i = 0
		forest_comments = submission.comments
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:
			i = i + 1
			print i
			if str("http") in comment.body:
				#reply_world(comment)
				#print i
				print str(comment)
				csvout.append(comment)
				a.writerow(csvout)
