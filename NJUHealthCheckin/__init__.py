import datetime
import logging
import os
import requests
import random
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util import Padding
from bs4 import BeautifulSoup

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # encrypt func
    def encryptAES(_p0: str, _p1: str) -> str:
        _chars = list('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678')
        def _rds(len: int) -> str: 
            return ''.join(random.choices(_chars, k=len))
        def _gas(data: str, key0: str, iv0: str) -> bytes:
            encrypt = AES.new(key0.strip().encode('utf-8'), AES.MODE_CBC, iv0.encode('utf-8'))
            return base64.b64encode(encrypt.encrypt(Padding.pad(data.encode('utf-8'), 16)))
        return _gas(_rds(64) + _p0, _p1, _rds(16)).decode('utf-8')

    # const 
    username = os.environ['NU_USER']
    password = os.environ['NU_PASS']
    url_login = r'https://authserver.nju.edu.cn/authserver/login'
    url_list = r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
    url_apply = r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'
    session = requests.Session()

    # login
    response = session.get(url_login)
    if response.status_code == 200:
        logging.info('Open login page success for ' + username)
    else:
        logging.error('Open login page fail for ' + username)
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.select_one("#pwdDefaultEncryptSalt").attrs['value']
    data_login = {
        'username': username, 
        'password': encryptAES(password, soup.select_one("#pwdDefaultEncryptSalt").attrs['value']),
        'lt' : soup.select_one('[name="lt"]').attrs['value'], 
        'dllt' : soup.select_one('[name="dllt"]').attrs['value'], 
        'execution' : soup.select_one('[name="execution"]').attrs['value'], 
        '_eventId' : soup.select_one('[name="_eventId"]').attrs['value'], 
        'rmShown' : soup.select_one('[name="rmShown"]').attrs['value'], 
    }
    response = session.post(url_login, data_login)
    if response.status_code == 200:
        logging.info('Login success for ' + username)
    else:
        logging.error('Login fail for ' + username)
        return

    # list
    response = session.get(url_list)
    content = response.json()
    if response.status_code == 200 and content['code'] == '0':
        logging.info('List success for ' + username)
    else:
        logging.error('List fail for ' + username)
        return

    # apply
    data = next(x for x in content['data'] if x.get('TJSJ') != '')
    data['WID'] = content['data'][0]['WID']
    fields = [
        'WID', 
        'CURR_LOCATION', 
        'IS_TWZC', 
        'IS_HAS_JKQK', 
        'JRSKMYS', 
        'JZRJRSKMYS'
    ]
    response = session.get('http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do?' + '&'.join([key + '=' + data[key] for key in fields]))
    content = response.json()
    if response.status_code == 200 and content['code'] == '0':
        logging.info('Apply success for ' + username)
    else:
        logging.error('Apply fail for ' + username)
        return
    pass
