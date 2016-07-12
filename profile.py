import pickle

SAVE_PATH = 'data/profiles.pkl'

def _generate_profile(description, nicks, network_data):
	return {'description' : description, 'nicks' : nicks, 'networks' : [*network_data]}

class ProfileHandler(object):
	def __init__(self, path=SAVE_PATH):
		self.profiles = {}
		self.path = path

	def load(self):
		try:
			with open(self.path, 'rb') as pf:
				self.profiles = pickle.load(pf)
		except (FileNotFoundError, IOError):
			pass #TODO: Common error handling

	def save(self):
		with open(self.path, 'wb') as pf:
			pickle.dump(self.profiles, pf)

	def new(self, name, description, nicks, network_data):
		if name not in self.profiles.keys():
			self.profiles[name] = _generate_profile(description, nicks, network_data)
		else:
			#TODO: more error handling
			pass

	def get(self, name, field=None):
		if field is None:
			return self.profiles[name]
		else:
			return self.profiles[name][field]

	def edit(self, name, changed_data):
		if name in self.profiles.keys():
			keys = self.profiles[name].keys()
			for key in changed_data.keys():
				if key == 'name':
					self.profiles[changed_data[key]] = self.profiles.pop(name)
					name = changed_data[key]
				else:
					if key in keys:
						self.profiles[name][key] = changed_data[key]
		else:
			#TODO
			pass


profiles = ProfileHandler()
profiles.new('Kevin', 'Friendly programmer ;)', ['Kebin', 'Kebby', 'Snibby'], [['Anonymous IRC', '192.168.1', '80', ['main', 'secret']]])
print(profiles.get('Kevin', 'description'))
profiles.edit('Kevin', {'name' : 'Kevum', 'description' : 'wanted by the FBI'})
print(profiles.get('Kevum'))
profiles.save()