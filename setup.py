import json
import os

#python -m disco.cli --config config.json to run the bot scripts

AUTH_TOKEN = os.environ["ARCHIVE_AUTH"]
with open('./config.json') as file:
    data = json.load(file)
data['token'] = AUTH_TOKEN
with open('./config.json', 'w') as file:
    json.dump(data, file)
print(AUTH_TOKEN)