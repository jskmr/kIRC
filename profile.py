import json

SAVE_PATH = 'data/profiles.json'

class Network(object):
    def __init__(self, name, address, port, login_command=None):
        self.name = name
        self.address = address
        self.port = port
        self.login_command = login_command

    def __repr__(self):
        return self.name

class Profile(object):
    def __init__(self, name, description, nicks, networks):
        self.name = name
        self.description = description
        self.nicks = nicks
        self.networks = networks

    def __repr__(self):
        return self.name

class ProfileHandler(object):
    def __init__(self, save_path=SAVE_PATH):
        self.save_path = save_path
        self.profiles = []

        with open(self.save_path, 'r') as profiles_file:
            profiles_data = json.loads(profiles_file.read())

        for name in profiles_data.keys():
            data = profiles_data[name]
            self.new(name, data['description'], data['nicks'],
                [Network(net, *data['networks'][net]) for net in data['networks'].keys()])

    def save(self):
        profiles_dict = {}

        for profile in self.all():
            profiles_dict[profile.name] = {
                'description' : profile.description,
                'networks' : {},
                'nicks' : profile.nicks
            }

            for net in profile.networks:
                profiles_dict[profile.name]['networks'][net.name] = [
                net.address, net.port, net.login_command]

        with open(self.save_path, 'w') as profiles_file:
            profiles_json = json.dumps(profiles_dict, indent=4)
            profiles_file.write(profiles_json)            

    def new(self, name, description, nicks, networks):
        self.profiles.append(Profile(name, description, nicks, networks))

    def get(self, name):
        for profile in self.profiles:
            if profile.name == name:
                return profile
        return None

    def all(self):
        return self.profiles