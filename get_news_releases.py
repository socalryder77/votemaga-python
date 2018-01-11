# -*- coding: utf-8 -*-
from news_releases.spider_runner import SpiderRunner
import logging
import praw
import sys

spider_runner = SpiderRunner()
previous_data = spider_runner.get_data()
spider_runner.run_spiders()
new_data = spider_runner.get_data()

data_to_post = []
for spider in spider_runner.get_spider_list():
    for post in new_data[spider.name]:
        post_it = True
        for prev_post in previous_data[spider.name]:
            if post['link'] == prev_post['link']:
                post_it = False
        if(post_it):
            data_to_post.append(post)



should_post_data = True
if len(sys.argv) > 1:
    should_post_data = sys.argv[1].lower() == 'true'

if should_post_data and len(data_to_post) > 0:
    reddit = praw.Reddit(client_id='RHPMCaot0ItkNw',
                           client_secret='dOTc0gaTTmzgjLnfzFD7u0e60R0',
                           password='HGT@9iwgkuY#T*7ay28IHTpya;w3y93*Y%&T#',
                           user_agent='News Release Bot',
                           username='News_Release_Bot') #reddit data in theses parentheses
    previous_submissions = reddit.redditor('News_Release_Bot').submissions.new(limit=500)
    previous_links = []
    for sub in previous_submissions:
        previous_links.append(sub.url)
    for link in data_to_post:
        if(link['link'] not in previous_links):
            #This will flair TrumpTV posts
            if('**TRUMP TV**' in link['title']):
                submission = reddit.subreddit("trump").submit(link["title"][12:], url=link["link"])
                submission.mod.flair(text='TRUMP TV', css_class='live-flair')
            else:
                reddit.subreddit("trump").submit(link["title"], url=link["link"])

                
