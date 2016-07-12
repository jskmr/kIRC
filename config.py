import json

SAVE_PATH = 'data/config.json'

class Config(object):
	def __init__(self, path):
		self.DEFAULT_CONFIG = {}
		self.path = path
		self.data = {}

		try:
			with open(self.path, 'r') as cf:
				data = json.loads(cf.readlines())
		except (FileNotFoundError, IOError):
			with open(self.path, 'w') as cf:
				cf.write(json.dumps({'4': 5, '6': 7}, sort_keys=False,
									 indent=4, separators=(',', ': ')))
				data = self.DEFAULT_CONFIG 