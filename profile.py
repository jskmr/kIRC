import pickle

SAVE_PATH = 'data/profiles.pkl'

def _generate_profile(description):
	return {'description' : description}

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

	def new(self, name, description):
		if name not in self.profiles.keys():
			self.profiles[name] = _generate_profile(description)
		else:
			#TODO: more error handling
			pass

	def get(self, name, field=None):
		if field is None:
			return self.profiles[name]
		else:
			return self.profiles[name][field]

	def edit(self, name, field, new):
		if name in self.profiles.keys():
			if field is 'name':
				if new not in self.profiles.keys():
					self.profiles[new] = self.profiles.pop(name)
				else:
					#TODO
					pass
			else:
				self.profiles[name][field] = new
		else:
			#TODO
			pass

if __name__ is '__main__':
	profiles = ProfileHandler()
	profiles.new('Kevin', 'Friendly programmer ;)')
	print(profiles.get('Kevin', 'description'))
	profiles.edit('Kevin', 'name', 'Kevum')
	print(profiles.get('Kevum', 'description'))
	profiles.save()