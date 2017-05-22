import time
import urllib
import json
import re

from app.controller import verify
from app.models import Task
from twitter import error
from flask import request, render_template, jsonify, redirect, url_for

from crawler.basicinfo_crawler import BasicinfoCrawler
from crawler.relation_crawler import RelationCrawler
from crawler.tweets_crawler import TweetsCrawler

basicinfo_crawler = BasicinfoCrawler()
relation_crawler = RelationCrawler()
tweets_crawler = TweetsCrawler()


@verify
def user_search():
	return render_template('user_search.html')

@verify
def get_user_tweets():
	screen_name = request.form['screen_name']
	max_id = request.form['max_id']
	count = 30

	if max_id == '0':
		max_id = 1

	max_id = long(max_id) - 1
	tweets = tweets_crawler.get_user_timeline(screen_name = screen_name, max_id = max_id, count = count)

	res = []
	for tweet in tweets:
		res.append({
			'id': tweet.id,
			'text':len(tweet.text) > 48 and tweet.text[0 : 48] + " ..." or tweet.text,
			'created_at':time.strftime('%Y-%m-%d', time.strptime(tweet.created_at.replace('+0000 ',''))),
			'favorite_count':tweet.favorite_count,
			'retweet_count':tweet.retweet_count,
			'lang':tweet.lang,
			'source':re.sub(r'^<a href.+?>','',tweet.source)[0 : -4]
		})
		
	return jsonify(res)

@verify
def user_profile(screen_name):
	user = basicinfo_crawler.get_user(screen_name = screen_name)
	friends = []
	followers = []
	try:
		friends = relation_crawler.get_friends(screen_name = screen_name, count = 30)
		for friend in friends:
			friend.created_at = time.strftime('%Y-%m-%d', time.strptime(friend.created_at.replace('+0000 ','')))
			if len(friend.description) > 28:
				friend.description = friend.description[0:28]
				friend.description += ' ...'

	except error.TwitterError as te:
		pass

	try:
		followers = relation_crawler.get_followers(screen_name = screen_name, count = 30)
		for follower in followers:
			follower.created_at = time.strftime('%Y-%m-%d', time.strptime(follower.created_at.replace('+0000 ','')))
			if len(follower.description) > 8:
				follower.description = follower.description[0:18]
				follower.description += ' ...'

	except error.TwitterError as te:
		pass

	try:
		tweets = tweets_crawler.get_user_timeline(screen_name = screen_name, count = 30)

		res = []
		for tweet in tweets:
			res.append({
				'id': tweet.id,
				'text':len(tweet.text) > 48 and tweet.text[0 : 48] + " ..." or tweet.text,
				'created_at':time.strftime('%Y-%m-%d', time.strptime(tweet.created_at.replace('+0000 ',''))),
				'favorite_count':tweet.favorite_count,
				'retweet_count':tweet.retweet_count,
				'lang':tweet.lang,
				'source':re.sub(r'^<a href.+?>','',tweet.source)[0 : -4]
			})

	except error.TwitterError as te:
		pass

	user.created_at = time.strftime('%Y-%m-%d', time.strptime(user.created_at.replace('+0000 ','')))

	get_image(user.profile_image_url, screen_name)

	return render_template('user_profile.html', user = user, followers = followers, friends = friends, tweets = res)

def get_image(url, screen_name):
	urllib.urlretrieve(url.replace('normal.','bigger.'), 'app/static/profile/%s.jpg' % screen_name)

@verify
def user_search_detail():
	data = json.loads(request.form['aoData'])

	for item in data:
		if item['name'] == 'sSearch':
			s_search = item['value']
			break

		if item['name'] == 'iDisplayLength':
			data_length = item['value']

	if s_search == '':
		return jsonify({'aaData': []})

	data_length  = int(data_length)
	if data_length > 100:
		data_length = 100

	page = 1
	flag = True
	count = data_length / 20
	user_list = []

	while count > 0:
		user_temp = basicinfo_crawler.get_user_search(term = s_search, count = 20, page = page)
		user_list.extend(user_temp)
		page += 1

		if len(user_temp) < 20:
			flag = False
			break

		count -= 1

	if data_length % 20 != 0 and flag:	
		user_list.extend(basicinfo_crawler.get_user_search(term = s_search, page = page, count = data_length % 20))

	res = []
	for user in user_list:
		if user.description != '':
			description = len(user.description) < 28 and user.description or user.description[0 : 28] + " ..."
		else :
			description = ''

		res.append({
			'screen_name': user.screen_name,
			'name': user.name,
			'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user.created_at.replace('+0000 ',''))),
			'description': description,
			'followers_count': user.followers_count,
			'friends_count': user.friends_count,
			'statuses_count': user.statuses_count,
			'lang': user.lang
		})

	return jsonify({'aaData': res})

@verify
def relation_search():
	return render_template('relation_search.html')

@verify
def task_list():
	tasks = Task.query.filter().all()

	for task in tasks:
		if len(task.remark) > 8:
			task.remark = task.remark[0:8]
			task.remark += ' ...'

	return render_template('task_list.html', tasks = tasks)

@verify
def tweets_search():
	return render_template('tweets_search.html')