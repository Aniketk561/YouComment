import os
class Config(object):
	BOT_TOKEN = os.environ.get('BOT_TOKEN')
	USERNAME = os.environ.get('EMAIL')
	PASSWORD = os.environ.get('PASSWORD')
	MESSAGE = os.environ.get('MESSAGE')