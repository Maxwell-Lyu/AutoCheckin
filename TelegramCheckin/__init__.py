import asyncio, selectors
import os
import datetime
import logging
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import azure.functions as func

async def worker(loop):
    api_id      = os.environ['TG_API_ID']
    api_hash    = os.environ['TG_API_HASH']
    api_session = os.environ['TG_SESSION']
    entity      = os.environ['TG_ENTITY']
    message     = os.environ['TG_MESSAGE']
    async with TelegramClient(StringSession(api_session), api_id, api_hash, loop=loop) as client:
        await client.send_message(entity, message)

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
