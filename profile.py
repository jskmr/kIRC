import json
import os
import os.path as path

PROFILES_PATH = 'data/profiles/'

PROFILE_NAME_PATTERN = '^[a-z_][a-z\d_.,!]*$'

class Network(object):
    def __init__(self, name, address, port, login_command=None):
        self.name = name
        self.address = address
        self.port = port
        self.login_command = login_command

    def __repr__(self):
        return self.name

class Profile(object):
    def __init__(self, name, description, nicks, networks, image_specified = False):
        self.name = name
        self._original_name = self.name
        self.description = description
        self.nicks = nicks
        self.networks = networks
        self.image_specified = image_specified

    def __repr__(self):
        return self.name

class ProfileHandler(object):
    def __init__(self, save_path=PROFILES_PATH):
        self.save_path = save_path
        self.profiles = []

        for item in os.listdir(self.save_path):
            profile_name = item
            profile_path = path.join(self.save_path, item)
            if path.isdir(profile_path):
                with open(path.join(profile_path, 'profile.json')) as raw_profile_data:
                    data = json.loads(raw_profile_data.read())

                    self.new(profile_name, data['description'], data['nicks'], [Network(
                        net, *data['networks'][net]) for net in data['networks'].keys()],
                        True if path.isfile(path.join(profile_path, 'img.png')) else False)

    def save(self, *profiles):
        for profile in (profiles if profiles else self.all()):
            profile_data = {
                'description' : profile.description,
                'networks' : {},
                'nicks' : profile.nicks
            }

            for net in profile.networks:
                profile_data['networks'][net.name] = [
                net.address, net.port, net.login_command]

            if profile.name != profile._original_name:
                base = self.save_path
                os.rename(path.join(base, profile._original_name), path.join(base, profile.name))

            profile_save_path = path.join(self.save_path, profile.name, 'profile.json')

            with open(profile_save_path, 'w') as profile_file:
                profile_json = json.dumps(profile_data, indent=4)
                profile_file.write(profile_json)

    def new(self, name, description, nicks, networks, image_specified):
        self.profiles.append(Profile(name, description, nicks, networks, image_specified))

    def get(self, name):
        for profile in self.profiles:
            if profile.name.lower() == name.lower():
                return profile
        return None

    def all(self):
        return self.profiles

profiles = ProfileHandler()
current = profiles.get('shabby')
current.name = 'Shiburizu'
profiles.save(current)