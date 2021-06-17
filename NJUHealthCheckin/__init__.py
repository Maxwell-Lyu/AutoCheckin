import datetime
import logging
import os
import requests
import js2py
from bs4 import BeautifulSoup

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # const 
    username = os.environ['NJUA_USER']
    password = os.environ['NJUA_PASS']
    url_encrypt = r'https://authserver.nju.edu.cn/authserver/custom/js/encrypt.js'
    url_login = r'https://authserver.nju.edu.cn/authserver/login'
    url_list = r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
    url_apply = r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'
    session = requests.Session()

    # encryption
    response = session.get(url_encrypt)
    context = js2py.EvalJs()
    context.execute(response.text)

    if response.status_code == 200:
        logging.info('Load encryption: %d, %s' % (response.status_code, response.reason))
    else:
        logging.error('Load encryption: %d, %s' % (response.status_code, response.reason))
        return

    # login
    response = session.get(url_login)

    if response.status_code == 200:
        logging.info('Open login page: %d, %s' % (response.status_code, response.reason))
    else:
        logging.error('Open login page: %d, %s' % (response.status_code, response.reason))
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    data_login = {
        'username':     username, 
        'password':     context.encryptAES(password, soup.select_one("#casLoginForm #pwdDefaultEncryptSalt").attrs['value']),
        'lt' :          soup.select_one('#casLoginForm [name="lt"]').attrs['value'], 
        'dllt' :        soup.select_one('#casLoginForm [name="dllt"]').attrs['value'], 
        'execution' :   soup.select_one('#casLoginForm [name="execution"]').attrs['value'], 
        '_eventId' :    soup.select_one('#casLoginForm [name="_eventId"]').attrs['value'], 
        'rmShown' :     soup.select_one('#casLoginForm [name="rmShown"]').attrs['value'], 
    }

    response = session.post(url_login, data_login)

    if response.status_code == 200:
        logging.info('Login for %s: %d, %s' % (username, response.status_code, response.reason))
    else:
        logging.error('Login for %s: %d, %s' % (username, response.status_code, response.reason))
        return

    # list
    response = session.get(url_list)

    try:
        content = response.json()
    except ValueError:
        content = {}
    if response.status_code == 200 and content.get('code') == '0':
        logging.info('List: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
    else:
        logging.error('List: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
        return

    # apply
    data = next(x for x in content['data'] if x.get('TJSJ') != '')
    data_apply = {
        'WID':              content['data'][0]['WID'], 
        'CURR_LOCATION':    data['CURR_LOCATION'], 
        'IS_TWZC':          data['IS_TWZC'], 
        'IS_HAS_JKQK':      data['IS_HAS_JKQK'], 
        'JRSKMYS':          data['JRSKMYS'], 
        'JZRJRSKMYS':       data['JZRJRSKMYS']
    }

    response = session.get(url_apply, params=data_apply)

    try:
        content = response.json()
    except ValueError:
        content = {}
    if response.status_code == 200 and content.get('code') == '0':
        logging.info('Apply: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
    else:
        logging.error('Apply: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
        return
    pass

