import datetime
import logging
import os
import re
import requests
from bs4 import BeautifulSoup


import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # const
    session = os.environ['QNXX_SESSION']
    url_report = r'https://service.jiangsugqt.org/youth/report'
    url_confirm = r'https://service.jiangsugqt.org/youth/lesson/confirm'

    # load report
    response = requests.get(url_report, cookies={'laravel_session': session})
    if response.status_code == 200:
        logging.info('Load report: %d, %s' %
                     (response.status_code, response.reason))
    else:
        logging.error('Load report: %d, %s' %
                      (response.status_code, response.reason))
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = [[col.get_text().strip() for col in row.select('td')]
            for row in soup.select('tbody tr')]
    id = len(rows)
    event = rows[0][0]
    if rows[0][1] == '已学习':
        logging.warning('Event %d:\'%s\' is already checked' % (id, event))
        return

    # load token
    response = requests.get(url_confirm, cookies={'laravel_session': session})
    if response.status_code == 200:
        logging.info('Load token: %d, %s' %
                     (response.status_code, response.reason))
    else:
        logging.error('Load token: %d, %s' %
                      (response.status_code, response.reason))
        return
    token = re.search(r'var token = "(.*?)";$', response.text, re.MULTILINE | re.DOTALL).group(0)

    # check in
    response = requests.post(
        url_confirm,
        data={'_token': token, 'lesson_id': id},
        cookies={'laravel_session': session}
    )
    try:
        content = response.json()
    except ValueError:
        content = {}
    if response.status_code == 200 and content.get('status') == 1:
        logging.info('Check in success, Event %d:\'%s\', %d, %s, %s' %
                     (id, event, response.status_code, response.reason, content.get('message') or 'No messgage available'))
    else:
        logging.error('Check in failed, Event %d:\'%s\', %d, %s, %s' %
                      (id, event, response.status_code, response.reason, content.get('message') or 'No messgage available'))
        return
