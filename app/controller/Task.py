import time
import threading

from app import app
from app.controller import verify
from app.database import db
from app.models import Task
from flask import request, render_template, jsonify, session, url_for, redirect

from crawler.basicinfo_crawler import BasicinfoCrawler
from crawler.relation_crawler import RelationCrawler
from crawler.tweets_crawler import TweetsCrawler

basicinfo_crawler = BasicinfoCrawler()
relation_crawler = RelationCrawler()
tweets_crawler = TweetsCrawler()

@verify
def task_list():
	tasks = Task.query.filter().all()

	for task in tasks:
		if len(task.remark) > 8:
			task.remark = task.remark[0:8]
			task.remark += ' ...'

	return render_template('task_list.html', tasks = tasks)

@verify
def task_delete():
	id = request.form['id']
	res = Task.query.filter(Task.id == id).delete()

	if res != None:
		return jsonify({'status': 1})
	else:
		return jsonify({'status': 0})

@verify
def task_add():
	return render_template('task_add.html')

def tweet_process(args):
	user_list = []
	tweets_crawler.get_user_all_timeline(screen_name = args['screen_name'])

	thread_num = args['thread_num']
	threads_pool = []

	while i < thread_num:
		threads_pool.append(threading.Thread(target = tweets_crawler.get_user_all_timeline, 
										args = (user_list, include_rts, exclude_replies)))
		i = i + 1

	for thread in threads_pool:
		thread.join()


	with app.app_context():
		Task.query.filter(Task.id == task_id).update({'finished_at': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})

def basicinfo_process(args):
	basicinfo_crawler.get_all_users([screen_name])
	with app.app_context():
		Task.query.filter(Task.id == task_id).update({'finished_at': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})

def friends_process(args):
	tweets_crawler.get_user_all_timeline(screen_name = screen_name)
	with app.app_context():
		Task.query.filter(Task.id == task_id).update({'finished_at': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})

def followers_process(args):
	basicinfo_crawler.get_all_users([screen_name])
	with app.app_context():
		Task.query.filter(Task.id == task_id).update({'finished_at': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))})

@verify
def task_add_submit():
	screen_name = request.form['search_name']
	search_type = request.form.getlist('type')

	thread_num = int(request.form['thread'])
	deepth = int(request.form['deepth'])
	style = int(request.form['style'])
	extension = request.form['extension']

	if thread_num < 1 or thread_num > 6:
		return redirect(url_for('task_add'))

	if deepth < 1 or deepth > 6:
		return redirect(url_for('task_add'))

	st = ""
	tweet_num = None
	friends_num = None
	followers_num = None
	basicinfo_num = None

	if '1' in search_type:
		tweet_num = request.form['tweet_num']
		st += '1'

	if '2' in search_type:
		friends_num = request.form['friends_num']
		st += '2'

	if '3' in search_type:
		followers_num = request.form['followers_num']
		st += '3'

	if '4' in search_type:
		basicinfo_num = request.form['basicinfo_num']
		st += '4'

		
	task = Task(task_name = request.form['task_name'], userid = session['userid'], search_name = request.form['search_name'], 
		thread_num = thread_num, deepth = deepth, style = style, extension = extension,
		tweet_num = tweet_num, friends_num = friends_num, followers_num = followers_num, basicinfo_num = basicinfo_num,
		remark = request.form['remark'], created_at = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
		search_type = st)

	db.session.add(task)
	db.session.commit()

	args = []
	args['screen_name'] = screen_name
	args['id'] = task.id
	args['thread_num'] = thread_num
	args['deepth'] = deepth
	args['style'] = style
	args['extension'] = extension

	args['tweet_num'] = tweet_num
	if search_type.find('1') != -1:
		t = threading.Thread(target = tweet_process, args = args)
		t.start()
	
	# args['friends_num'] = friends_num
	# if search_type.find('2') != -1:
	# 	t = threading.Thread(target = friends_process, args = args)
	# 	t.start()
	
	# args['followers_num'] = followers_num
	# if search_type.find('3') != -1:
	# 	t = threading.Thread(target = followers_process, args = args)
	# 	t.start()

	# args['basicinfo_num'] = basicinfo_num
	# if search_type.find('4') != -1:
	# 	t = threading.Thread(target = basicinfo_process, args = args)
	# 	t.start()

	return render_template('task_add.html', status = 1)