from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import requests
import urllib.request as ul
import pandas as pd
import time
import getpass

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.flipkart.com/account/orders?link=home_orders")

usr=input('Enter Mobile Number: ')
while len(usr) != 10:
    usr=input('Enter Correct Mobile Number: ')

driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[1]/input').send_keys(usr)
choice = input('Enter 1 for password or Enter 2 for OTP: ')
if choice == '1':
    pwd = getpass.getpass()
    driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[2]/input').send_keys(pwd)
    driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[3]/button').click()
else:
    driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[4]/button').click()
    otp = input('Enter OTP: ')
    for o in otp:
        driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div[2]/div/div/form/div/div[1]/input').send_keys(otp)
    driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div[2]/div/div/form/button').click()


SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

data = driver.page_source
soup = bs(data)

orders = soup.find_all('a', class_='_2WFi0x')
titles = list()
prices = list()
status = list()
category = list()
links = list()
date=list()
for order in orders:
    if (order.find('span', class_='_7BRRQk').text) not in ['Returned','Cancelled','Order Not Placed']:
        title = order.find('span', class_='row _13y4_y _1iu0PI').text
        titles.append(title)
        price = order.find('div', class_='col-2-12 JL36Xz').text
        prices.append(price)
        sts = order.find('span', class_='_7BRRQk').text
        status.append(sts)
        links.append('https://www.flipkart.com'+ order.get('href'))

for link in links:
    driver.get(link)
    time.sleep(6)
    date.append(bs(driver.page_source).find('div', class_='_3wS5ZT').span.text)
    new_url = 'https://www.flipkart.com' + bs(driver.page_source).find('a', class_='_2AkmmA row NPoy5u').get('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(new_url)
    try:
        category.append(bs(driver.page_source).findAll('a', class_='_1KHd47')[1].text)
    except:
        category.append("")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()

data = {'Purchase Date': date, 'Titles': titles, 'Category': category, 'Status': status, 'Prices': prices}
df = pd.DataFrame(data)
df
