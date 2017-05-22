from twitter import Api
from app import app

APP_INFO = app.config['APP_INFO']
ApiList = []
ApiCount = len(APP_INFO)

for i in range(ApiCount):
	ApiList.append(Api(consumer_key = APP_INFO[i]['consumer_key'],
                      consumer_secret = APP_INFO[i]['consumer_secret'],
                      access_token_key = APP_INFO[i]['access_token_key'],
                      access_token_secret = APP_INFO[i]['access_token_secret']))

