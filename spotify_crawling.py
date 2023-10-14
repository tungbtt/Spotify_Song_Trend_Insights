# -*- coding: utf-8 -*-
"""

Spotify Crawling

"""

from datetime import date
from datetime import datetime
import pandas as pd
import numpy as np
import os
from selenium import webdriver
import time


def convert_to_desired_format(date_string):

    month, day = date_string.split(' ')
    month_number = datetime.strptime(month, '%B').month
    current_year = datetime.now().year
    
    input_date = datetime(current_year, month_number, int(day))
    if input_date < datetime.now():
        year = current_year
    else:
        year = current_year - 1
        
    formatted_date = f"{year}-{'{:02d}'.format(month_number)}-{day}"
    return formatted_date



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)
time.sleep(10)


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = 'https://accounts.spotify.com/vi/login?continue=https%3A%2F%2Fcharts.spotify.com/login'

username = 'tungbtt.2002@gmail.com'
password = '@cc_temp'

driver.get(url)
driver.implicitly_wait(5)
time.sleep(10)

driver.save_screenshot('_login.png')

driver.find_element(By.XPATH, '//*[@id="login-username"]').send_keys(username)
driver.implicitly_wait(2)
time.sleep(5)

driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(password)

driver.implicitly_wait(2)
time.sleep(5)
driver.save_screenshot('_id_pass.png')



driver.find_element(By.XPATH, '//*[@id="login-button"]/span[1]').click()
time.sleep(10)

driver.save_screenshot('_id_pass_ok.png')
'''
print("The Spotify Global Chart is being crawled...")

driver.get("https://charts.spotify.com/charts/view/regional-global-daily/latest")

driver.implicitly_wait(5)
time.sleep(10)

driver.save_screenshot('_global_chart.png')

date_picker_element = driver.find_element(By.XPATH, '//*[@id="date_picker"]')
date = convert_to_desired_format(date_picker_element.get_attribute('value'))
print("Date: ",date)

table = driver.find_element(By.CSS_SELECTOR, 'table').find_elements(By.TAG_NAME, 'tbody')[0]

rows = table.find_elements(By.TAG_NAME, 'tr')

song_data_list = []
for row in rows:

        link_element = row.find_element(By.XPATH, './td[3]/div/div[2]/a')
        link_href = link_element.get_attribute('href')

        elements = row.find_elements(By.TAG_NAME, 'td')

        song_data = {
            'date' : date,
            'position' : int(elements[1].text.split('\n')[0]),
            'id' : link_href.replace('https://open.spotify.com/track/',''),
            'track' : elements[2].text.split('\n')[0],
            'artist' : elements[2].text.split('\n')[1],
            'peak' : int(elements[3].text),
            'prev' : int(elements[4].text) if elements[4].text != '—' else -1,
            'streak' : int(elements[5].text),
            'streams': int(elements[6].text.replace(',', ''))
        }

        song_data_list.append(song_data)


global_chart = pd.DataFrame(song_data_list)

header = not os.path.exists(r'datasets/global_chart.csv') or os.stat(r'datasets/global_chart.csv').st_size == 0
global_chart.to_csv(r'datasets/global_chart.csv', mode='a', header=header, index=False)

print("Done!")

print("The Spotify Vietnam Chart is being crawled...")

driver.get("https://charts.spotify.com/charts/view/regional-vn-daily/latest")

driver.implicitly_wait(5)
time.sleep(10)
#driver.save_screenshot('_vn_chart.png')

date_picker_element = driver.find_element(By.XPATH, '//*[@id="date_picker"]')
date = convert_to_desired_format(date_picker_element.get_attribute('value'))
print("Date: ",date)

table = driver.find_element(By.CSS_SELECTOR, 'table').find_elements(By.TAG_NAME, 'tbody')[0]

rows = table.find_elements(By.TAG_NAME, 'tr')

song_data_list = []

for row in rows:

        link_element = row.find_element(By.XPATH, './td[3]/div/div[2]/a')
        link_href = link_element.get_attribute('href')

        elements = row.find_elements(By.TAG_NAME, 'td')

        song_data = {
            'date' : date,
            'position' : int(elements[1].text.split('\n')[0]),
            'id' : link_href.replace('https://open.spotify.com/track/',''),
            'track' : elements[2].text.split('\n')[0],
            'artist' : elements[2].text.split('\n')[1],
            'peak' : int(elements[3].text),
            'prev' : int(elements[4].text) if elements[4].text != '—' else -1,
            'streak' : int(elements[5].text),
            'streams': int(elements[6].text.replace(',', ''))
        }

        song_data_list.append(song_data)


vn_chart = pd.DataFrame(song_data_list)

driver.quit()

header = not os.path.exists(r'datasets/vn_chart.csv') or os.stat(r'datasets/vn_chart.csv').st_size == 0
vn_chart.to_csv(r'datasets/vn_chart.csv', mode='a', header=header, index=False)

print("Done!")

# Nên add file audio_features.csv vào trước để hạn chế request quá nhiều chết key api.

import requests

CLIENT_ID = '29942d75c20b46b9b01eb4cd31edff20'
CLIENT_SECRET = 'e8905b5241e54a6b8340e94282abb615'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'

check = not os.path.exists(r'datasets/audio_features.csv') or os.stat(r'datasets/audio_features.csv').st_size == 0

if check:
    exist_tracks = set()
else:
    exist_tracks = set(pd.read_csv(r'datasets/audio_features.csv')['id'])

vn_chart_ids = set(vn_chart['id'])
global_chart_ids = set(global_chart['id'])

not_exist_tracks = vn_chart_ids.union(global_chart_ids).difference(exist_tracks)

audio_features_data = []

print("The audio features are being crawled...")

for track_id in not_exist_tracks:
    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers).json()
    in4 = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers).json()

    r['explicit'] = in4['explicit']
    r['popularity'] = in4['popularity']
    r['release_date'] = in4['album']['release_date']
    r['album_id'] = in4['album']['id']
    r['album_name'] = in4['album']['name']
    r['track_number'] = in4['track_number']
    r['preview_url'] = in4['preview_url']

    audio_features_data.append(r)

audio_features = pd.DataFrame(audio_features_data)

if len(audio_features) != 0:
    audio_features = audio_features.set_index('id').reset_index().drop(columns=['type','uri','track_href','analysis_url'])
    audio_features.to_csv(r'datasets/audio_features.csv', mode='a', header=check, index=False)

print("Done!")

'''
