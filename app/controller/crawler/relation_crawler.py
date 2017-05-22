import time
# import threading

# from config import THREAD_NUM
from twitter import error
from app.api import ApiList, ApiCount
# from database import Mysql

class RelationCrawler:
	def __init__(self):
		self.api_index = 0
		
	def get_friendids(self,
                      user_id = None,
                      screen_name = None,
                      cursor = None,
                      count = None,
                      total_count = None,
                      skip_status = False,
                      include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriendIDs(user_id = user_id,
			                      screen_name = screen_name,
			                      cursor = cursor,
			                      count = count,
			                      total_count = total_count,
			                      skip_status = skip_status,
			                      include_user_entities = include_user_entities)

		return friends

	def get_friendids_paged(self,
	                        user_id = None,
	                        screen_name = None,
	                        cursor = -1,
	                        stringify_ids = False,
	                        count = 5000):
		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriendIDsPaged(user_id = user_id,
					                    screen_name = screen_name,
					                    cursor = cursor,
					                    count = count,
					                    stringify_ids = stringify_ids)

		return friends

	def get_friends(self,
                    user_id = None,
                    screen_name = None,
                    count = None,
                    include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = self.get_friends_paged(user_id = user_id, 
										 screen_name = screen_name, 
										 count = count, 
										 include_user_entities = include_user_entities)
	
		return friends[2]

	def get_friends_paged(self,
                   		  user_id = None,
                          screen_name = None,
                          cursor = -1,
                          count = 200,
                          skip_status = True,
                          include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriendsPaged(user_id = user_id,
				                      screen_name = screen_name,
				                      cursor = cursor,
				                      count = count,
				                      skip_status = skip_status,
				                      include_user_entities = include_user_entities)

		
		return friends

	def get_all_friendids(user_id = None,
	                      screen_name = None,
	                      skip_status = False,
	                      include_user_entities = True):

		cursor = -1
		api_index = 0
		sleep_count = 0

		while cursor != 0:
			api = ApiList[api_index]
			api_index = (api_index + 1) / ApiCount

			try:
				out = api.GetFriendIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2] 
			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					continue
			except Exception as e:
				continue


	def get_followersids(self,
	                     user_id = None,
	                     screen_name = None,
	                     cursor = None,
	                     count = None,
	                     total_count = None,
	                     skip_status = False,
	                     include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followers = api.GetFollowersIDs(user_id = user_id,
					                     screen_name = screen_name,
					                     cursor = cursor,
					                     count = count,
					                     total_count = total_count,
					                     skip_status = skip_status,
					                     include_user_entities = include_user_entities)

		return followers

	def get_followersids_paged(self,
		                       user_id = None,
		                       screen_name = None,
		                       cursor = -1,
		                       stringify_ids = False,
		                       count = 5000):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followers = api.GetFollowersIDsPaged(user_id = user_id,
						                 	 screen_name = screen_name,
						                 	 cursor = cursor,
						                 	 count = count,
						                 	 stringify_ids = stringify_ids)

		return followers

	def get_followers(self,
	                  user_id = None,
	                  screen_name = None,
	                  count = None,
	                  include_user_entities = True):

		if user_id == None and screen_name == None:
			return []

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followers = self.get_followers_paged(user_id = user_id, 
											 screen_name = screen_name, 
											 count = count, 
											 include_user_entities = include_user_entities)

		return followers[2]

	def get_followers_paged(self,
	                   		 user_id = None,
	                         screen_name = None,
	                         cursor = -1,
	                         count = 200,
	                         skip_status = True,
	                         include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followers = api.GetFollowersPaged(user_id = user_id,
					                        screen_name = screen_name,
					                        cursor = cursor,
					                        count = count,
					                        skip_status = skip_status,
					                        include_user_entities = include_user_entities)

		return followers

	def get_all_followersids(user_id = None,
		                     screen_name = None,
		                     skip_status = False,
		                     include_user_entities = True):

		cursor = -1
		api_index = 0
		sleep_count = 0

		while cursor != 0:
			api = ApiList[api_index]
			api_index = (api_index + 1) / ApiCount

			try:
				out = api.GetFollowersIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]

			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					continue
			except Exception as e:
				continue