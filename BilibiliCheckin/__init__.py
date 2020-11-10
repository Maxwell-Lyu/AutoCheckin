import datetime
import logging
import os
import json
import requests

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    sessdata = os.environ["BL_SESSDATA"]
    response = requests.get("https://api.live.bilibili.com/sign/doSign", cookies={"SESSDATA": sessdata})
    content = json.loads(response.text)
    if content["code"] == 0:
      logging.info(content["data"]["text"] + "," + content["data"]["specialText"])
    elif content["code"] < 0: 
      logging.error(content["message"])
    else:
      logging.warn(content["message"])

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
