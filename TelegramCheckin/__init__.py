import asyncio, selectors
import os
import datetime
import logging
from telethon.sync import TelegramClient, Conversation
from telethon.sessions import StringSession
import azure.functions as func

async def worker(loop):
    api_id      = os.environ['TLGM_API_ID']
    api_hash    = os.environ['TLGM_API_HASH']
    api_session = os.environ['TLGM_SESSION']
    entity      = os.environ['TLGM_ENTITY']
    message     = os.environ['TLGM_MESSAGE']
    client = TelegramClient(StringSession(api_session), api_id, api_hash, loop=loop)
    await client.connect()
    async with client.conversation(entity=entity) as conv:
        await conv.send_message(message)
        response = await conv.get_response()
        logging.info(response.text)
        await conv.mark_read()

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    if mytimer.past_due:
        logging.info('The timer is past due!')
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)  
    try:
        loop.run_until_complete(worker(loop))
    finally:
        loop.close()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
