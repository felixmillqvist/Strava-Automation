import sys
import selenium
import csv 
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.keys import Keys
import time


website = 'https://www.strava.com/upload/manual'
filePath = str(sys.argv[1])
email = input('Google E-Mail:  ') 
password = getpass('Google Password:  ')

#Login and Navigate to manual upload
driver = webdriver.Chrome('C:\Program Files\Chromedriver.exe')
driver.get(website)
link = driver.find_element_by_link_text('Log in using Google')
link.click()


emailElem = driver.find_element_by_id('identifierId')
emailElem.send_keys(email)
nextButton = driver.find_element_by_id('identifierNext')
nextButton.click()
time.sleep(1)
passwordElem = driver.find_element_by_name('password')
passwordElem.send_keys(password)
signinButton = driver.find_element_by_id('passwordNext')
signinButton.click()
time.sleep(2)

with open(filePath, 'r') as csv_f:
    csv_dict = csv.DictReader(csv_f)

    for row in csv_dict:
        
        act_type = row['Type']
        dist = row['Distance (km)']
        set_date = row['Date']
        duration = row['Duration']

        duration = duration.split(':')
        if len(duration) == 1:
            dur_sec = duration[0]
            dur_min = 0
            dur_hour = 0
        elif len(duration) == 2:
            dur_sec = duration[1]
            dur_min = duration[0] 
            dur_hour = 0
        elif len(duration) == 3:
            dur_sec = duration[2]
            dur_min = duration[1] 
            dur_hour = duration[0]
            
        set_date = set_date.split()
        act_time = set_date[1]

        set_date = set_date[0].split('-')
        date_str = f"{set_date[1]}/{set_date[2]}/{set_date[0]}"

        dist_elem = driver.find_element_by_id('activity_distance')
        dist_elem.clear()
        dist_elem.send_keys(dist)

        dur_hour_elem = driver.find_element_by_id('activity_elapsed_time_hours')
        dur_hour_elem.clear()
        dur_hour_elem.send_keys(dur_hour)

        dur_min_elem = driver.find_element_by_id('activity_elapsed_time_minutes')
        dur_min_elem.clear()
        dur_min_elem.send_keys(dur_min)

        dur_sec_elem = driver.find_element_by_id('activity_elapsed_time_seconds')
        dur_sec_elem.clear()
        dur_sec_elem.send_keys(dur_sec)


        time_elem = driver.find_element_by_id('activity_start_time_of_day')
        time_elem.clear()
        time_elem.send_keys(act_time)


        type_elem = driver.find_element_by_id('activity-type-dd')
        type_elem.click()
        if act_type == 'Running':
            type_elem = driver.find_element_by_xpath('//*[@id="activity-type-dd"]/ul/li[2]')
        else:    
            type_elem = driver.find_element_by_xpath('//*[@id="activity-type-dd"]/ul/li[17]')
        
        type_elem.click()

        date_elem = driver.find_element_by_id('activity_start_date')
        date_elem.clear()
        date_elem.send_keys(date_str)
        
        sub_elem = driver.find_element_by_xpath('//*[@id="new_activity"]/div[6]/div/input')
        sub_elem.click()
        time.sleep(1)
        driver.get(website)
#driver.close()    
