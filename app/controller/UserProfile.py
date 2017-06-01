import urllib
from app import app
from app.controller import verify
from app.database import db
from app.models import StandardUsers as stusers
from flask import request, render_template, jsonify, session, url_for, redirect
from crawler.basicinfo_crawler import BasicinfoCrawler
from app.controller.ProfileConstruct import TweetsClassify
from app.controller.ProfileConstruct import config
from app.controller.ProfileConstruct import GenerateXML

basicinfo_crawler = BasicinfoCrawler()

months = config.months
@verify
def user_profile_list():
	users = stusers.query.filter().all()

	return render_template('user_profile_list.html',users=users)

@verify
def add_standard_users():
	return render_template('add_standard_users.html')

@verify
def user_profile(screen_name):
	user = (stusers.query.filter(stusers.screen_name == screen_name).all())[0]
	if(len(user.created_at.split(" ")) > 5):
		user.created_at = converttime(user.created_at)
	# get_image(user.profile_image_url, screen_name)

	# get psychology
	
	return render_template('standardUsers_profile.html',user=user)

# convert no-formattime to format time
def converttime(noformattime):
	time_period = noformattime.split(" ")
	month = months[time_period[1]]
	day = time_period[2]
	year = time_period[5]
	time = time_period[3]
	last_time = year + "/" + month + "/" + day + " " + time
	# print last_time
	return last_time

# get target user's image
def get_image(url, screen_name):
	urllib.urlretrieve(url.replace('normal.','bigger.'), 'app/static/profile/%s.jpg' % screen_name)

# get target user's tweets
def get_user_tweet(screen_name):
	pass

@verify
def user_add_submit():
	screen_name = request.form['screen_name']
	category = request.form['category']
	user = basicinfo_crawler.get_user(screen_name = screen_name)
	# insert new standard user into database
	newuser = stusers(screen_name=user.screen_name,name=user.name,category=user.category)
	
	# db.session.add(newuser)
	db.session.commit()
	# return the list
	user_profile_list()

@verify
def insert_standard_users():
	return render_template('search_users_profile.html')

@verify
def user_profiles(screen_name,type):
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

	return render_template('UserDetails.html', user = user, followers = followers, friends = friends, tweets = res,type=type)

@verify
def search_user(type):
	return render_template('search_users_profile.html',type=type)

def apiUserProfile(screen_name,data):
	user = (stusers.query.filter(stusers.screen_name == screen_name).all())[0]
	if(len(user.created_at.split(" ")) > 5):
		user.created_at = converttime(user.created_at)
	return jsonify({"userid":user.userid,"name":user.name})

@verify
def user_add_submit(screen_name):
	pass
	return render_template('standardUsers_profile.html',user=user)

# @verify
def OutPut2XML(screen_name):
	user = (stusers.query.filter(stusers.screen_name == screen_name).all())[0]
	GenerateXML.GenerateUserXml(user)
	return
