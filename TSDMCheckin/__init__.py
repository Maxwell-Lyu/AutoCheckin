import datetime
import logging
import os
import requests
from common.ResultParser import TSDMResultParser as parser

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    auth = os.environ['TSDM_AUTH']
    saltkey = os.environ['TSDM_SALTKEY']

    cookies = {
        's_gkr8_f779_auth': auth,
        's_gkr8_f779_saltkey': saltkey
        }

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }

    content = requests.get('https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&mobile=yes', cookies=cookies, headers=headers).text
    position = content.find('name=\"formhash\" value=\"')
    if position > 0:
        formhash = content[position + 23: position + 31]
        response = requests.post('https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&mobile=yes&operation=qiandao&infloat=0&inajax=0', 
            cookies=cookies, 
            headers=headers,
            data={'formhash': formhash,'qdxq': 'kx','qdmode': '3'})
        result = parser().feed(response.text) or '未知错误，请联系开发者'
        if result.find('恭喜你签到成功!') >= 0:
            logging.info(result)
        else:
            logging.error(result)
    else:
        if content.find('您今天已经签到过了或者签到时间还未开始') >= 0:
            logging.error('您今天已经签到过了或者签到时间还未开始')
        else:
            logging.error(parser().feed(content) or '未知错误，请联系开发者')

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
