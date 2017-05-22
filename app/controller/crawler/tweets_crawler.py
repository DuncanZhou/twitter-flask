import time
import threading

# from app.config import THREAD_NUM
from twitter import error
from app.api import ApiList, ApiCount
from pymongo import MongoClient

class TweetsCrawler:
	def __init__(self):
		self.api_index = 0
		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		self.db = client[db_name]
		
	def get_user_timeline(self,
						  user_id = None,
						  screen_name = None, 
						  since_id = None, 
						  max_id = None, 
						  count = None, 
						  include_rts = True, 
						  trim_user = True, 
						  exclude_replies = False):

		if user_id == None and screen_name == None:
			return []

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		tweets = api.GetUserTimeline(user_id = user_id,	screen_name = screen_name, 
									 since_id = since_id, max_id = max_id, count = count,
									 include_rts = include_rts, trim_user = trim_user,
									 exclude_replies = exclude_replies)

		return tweets

	def get_user_all_timeline(self, user_id = None,
						  	  screen_name = None, 
						  	  include_rts = True, 
						  	  exclude_replies = False):

		if user_id == None and screen_name == None:
			return

		flag = True
		tweets = [0]
		sleep_count = 0
		api_index = self.api_index

		collect = self.db['tweet_task']

		while len(tweets) > 0:
			api_index = (api_index + 1) % ApiCount
			api = ApiList[api_index]
			try:
				if flag:
					tweets = api.GetUserTimeline(user_id = user_id, screen_name = screen_name, 
												include_rts = include_rts, exclude_replies = exclude_replies,
						  	  					trim_user = True, count = 200)
					flag = False

				else:
					tweets = api.GetUserTimeline(user_id = user_id, screen_name = screen_name,
												include_rts = include_rts, exclude_replies = exclude_replies,
						 						trim_user = True, count = 200, max_id = tweets[-1].id - 1)

			except error.TwitterError as te:
				print te
				if te.message['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					break
			except Exception as e:
				print e
				break

			for tt in tweets:
				tweet = {
					'coordinates': tt.coordinates,  # Coordinates
					'created_at': tt.created_at, # String
					'favorite_count': tt.favorite_count, # int
					'filter_level': tt.filter_level if hasattr(tt, 'filter_level') else '', # String
					'hashtags': map(lambda x: x.text, tt.hashtags), # {'0': ,'1':}
					'_id': tt.id_str, # String
					'in_reply_to_status_id': tt.in_reply_to_status_id,
					'in_reply_to_user_id': tt.in_reply_to_user_id,
					'lang': tt.lang, # String
					'place': tt.place, # Place
					'possibly_sensitive': tt.possibly_sensitive, # Boolean
					'retweet_count': tt.retweet_count, # int
					'source': tt.source, # String
					'text': tt.text, # String
					'user_id': tt.user.id, # int
					'user_mentions': map(lambda x: x.id, tt.user_mentions), # []
					'withheld_copyright': tt.withheld_copyright, # Boolean
					'withheld_in_countries': tt.withheld_in_countries, # Array of String
					'withheld_scope': tt.withheld_scope, #String
				}
				try:
					collect.insert_one(tweet)
				except Exception as e:
					continue
		

	def get_all_users_timeline(user_list = None, 
							   include_rts = True, 
							   exclude_replies = False):		

		if len(user_list) == 0:
			return

		i = 0
		thread_pool = []
		self.lock = threading.Lock()


		while i < 6:
			threads_pool.append(threading.Thread(target = get_users_timeline_thread, 
											args = (user_list, include_rts, exclude_replies)))
			i = i + 1

		for thread in thread_pool:
			thread.join()

	def get_users_timeline_thread(user_list = None, include_rts = True, exclude_replies = False):
		lock = self.lock
		while len(user_list) > 0:
			if lock.acquire():
				user_id = user_list.pop(0)
				lock.release()

			get_user_all_timeline(user_id = user_id,
						  	  include_rts = include_rts, 
						  	  exclude_replies = exclude_replies)
