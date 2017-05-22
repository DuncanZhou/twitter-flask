import urllib
from app import app
from app.controller import verify
from app.database import db
from app.models import StandardUsers as stusers
from flask import request, render_template, jsonify, session, url_for, redirect
from crawler.basicinfo_crawler import BasicinfoCrawler

basicinfo_crawler = BasicinfoCrawler()

months = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
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
	return render_template('standardUsers_profile.html',user=user)

# convert no-formattime to format time
def converttime(noformattime):
	time_period = noformattime.split(" ")
	month = months[time_period[1]]
	day = time_period[2]
	year = time_period[5]
	time = time_period[3]
	last_time = year + "/" + month + "/" + day + " " + time
	print last_time
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
