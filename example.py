import voodooconfig
import getpass

# Let's imagine you have a config defined as:


class MyAwesomeConfig(voodooconfig.VoodooConfig):

    options = {'username': lambda: getpass.getuser(),
               'api_key': None,
               'server': 'server.example',
               'protocol': 'https',
               'api_version': 'v1'
               }

# You can then instatiate the config with:

config = MyAwesomeConfig()

# And your user should be set, since VoodooConfig checks for callables:

print("Username is: '{0}'".format(config.username))

# However it is not yet complete, since the api_key is missing:

try:
    config.is_complete()
except voodooconfig.MissingConfigValues:
    print('config is incomplete')

# You would have to update the api-key, for example using a dictionary:

config.update({'api_key': 'APIKEY'})

# Check that it was set, (you could also update it like this):

print("'api_key' is: '{0}'".format(config.api_key))

# Then, note that VoodooConfig would complain, if you spellt it wrong.

try:
    config.update({'apikey': 'APIKEY'})
except voodooconfig.UnexpectedConfigValues:
    print('Yes, we misspellt it')

# Lastly, note, that it is roboust to - and _ changes:

config.update({'api-key': 'NEWAPIKEY'})
print("'api_key' is: '{0}'".format(config.api_key))
