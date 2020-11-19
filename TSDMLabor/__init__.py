import datetime
import logging
import requests
import re
import os
from html.parser import HTMLParser

import azure.functions as func

class ResultParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = None
        self.found = False

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'div' and ('id', 'messagetext') in attrs:
            self.found = True

    def handle_data(self, data: str) -> None:
        if self.found and self.lasttag == 'p':
            self.result, self.found = data, False
    
    def feed(self, feed: str) -> str:
        HTMLParser.feed(self, feed)
        return self.result

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
    result = ResultParser().feed(response.text.replace('<br />', ''))
    if result.find('恭喜') >= 0:
        logging.info(result)
    else:
        logging.error(result)

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
