from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
import json


# login using webdriver
login_page = 'https://www.tsdm39.net/member.php?mod=logging&action=login&mobile=yes'
driver = Chrome('..\chromedriver.exe')
wait = WebDriverWait(driver, 300)
driver.get(login_page)
wait.until(lambda driver: driver.current_url != login_page)
cookies = {cookie['name']:cookie['value'] for cookie in driver.get_cookies()}
driver.close()

if cookies.get('s_gkr8_f779_auth') is None:
	print('Login failed, please try again!')
	exit()
	
# dump json for local dev
local = {
    "Values": {
        "TS_AUTH": cookies['s_gkr8_f779_auth'],
        "TS_SALTKEY": cookies['s_gkr8_f779_saltkey']
    }
}
with open('local.settings.partial.json', 'w+') as file:
    json.dump(local, file, indent=2)
print('+ local.settings.partial.json: generated for local.settings.json, mix into local.settings.json')

# dump json for remote deploy
remote = [
    {
        "name": "TS_AUTH",
        "value": cookies['s_gkr8_f779_auth'],
        "slotSetting": False
    },
    {
        "name": "TS_SALTKEY",
        "value": cookies['s_gkr8_f779_saltkey'],
        "slotSetting": False
    }
]
with open('remote.settings.partial.json', 'w+') as file:
    json.dump(remote, file, indent=2)
print('+ remote.settings.partial.json: generated for azure function configuration, mix into \"Advanced edit\"')

