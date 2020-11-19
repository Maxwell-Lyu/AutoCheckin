import datetime
import logging
import requests
import re
import os
from common.ResultParser import TSDMResultParser as parser

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    # achieve secrets
    auth =  os.environ['TS_AUTH']
    saltkey =  os.environ['TS_SALTKEY']
    # build request parameters
    labor_url = 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work'
    cookies = {
        's_gkr8_f779_auth': auth,
        's_gkr8_f779_saltkey': saltkey
    }
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    num_adv = len(re.findall('class="npadv"', requests.get(url=labor_url, headers=headers, cookies=cookies).text))
    # send requests: num * [click] and 1 * [getcre]
    for _ in range(num_adv):
        response = requests.post(url=labor_url, headers=headers, cookies=cookies, data={'act': 'clickad'})
    response = requests.post(url=labor_url, headers=headers, cookies=cookies, data={'act': 'getcre'})
    # analyze result
    result = parser().feed(response.text.replace('<br />', ''))
    if result.find('恭喜') >= 0:
        logging.info(result)
    else:
        logging.error(result)

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
