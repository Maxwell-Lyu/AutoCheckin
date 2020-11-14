from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import json

# prompt for data
api_id = input(
    'Your telegram api_id, achieved from https://core.telegram.org/api/obtaining_api_id:\n')
api_hash = input(
    'Your telegram api_hash, achieved from https://core.telegram.org/api/obtaining_api_id:\n')
entity = input('The username send message to, look like \"@username\":\n')
message = input('The check in message to send:\n')

# start client and send message
client = TelegramClient(StringSession(), api_id, api_hash)
client.start()
client.send_message(entity, message)
print('\nI\'ve already checked in for you, check out your telegram to see if it works.')

# save and show session
api_session = client.session.save()
print('\nOK, this is your session, if you need it for anything else:\n ========\n' +
      api_session + '\n=========')

# dump json for local dev
local = {
    "Values": {
        "TG_API_ID": api_id,
        "TG_API_HASH": api_hash,
        "TG_SESSION": api_session,
        "TG_ENTITY": entity,
        "TG_MESSAGE": message
    }
}
with open('local.settings.json', 'w+') as file:
    json.dump(local, file, indent=2)
print('+ local.settings.json: generated for local.settings.json, mix into local.settings.json')

# dump json for remote deploy
remote = [
    {
        "name": "TG_API_ID",
        "value": api_id,
        "slotSetting": False
    },
    {
        "name": "TG_API_HASH",
        "value": api_hash,
        "slotSetting": False
    },
    {
        "name": "TG_SESSION",
        "value": api_session,
        "slotSetting": False
    },
    {
        "name": "TG_ENTITY",
        "value": entity,
        "slotSetting": False
    },
    {
        "name": "TG_MESSAGE",
        "value": message,
        "slotSetting": False
    }
]
with open('remote.settings.json', 'w+') as file:
    json.dump(remote, file, indent=2)
print('+ remote.settings.json: generated for azure function configuration, mix into \"Advanced edit\"')
