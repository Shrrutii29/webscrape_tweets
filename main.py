# import dependencies

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from dotenv import load_dotenv
import csv

driver = webdriver.Chrome()
driver.get("http://www.x.com/login")
driver.maximize_window()

# setup for log in
sleep(30)
username = driver.find_element(By.XPATH, "//input[@name='text']")
username.send_keys("Shrutiinavale")
next_button=driver.find_element(By.XPATH,"//span[contains(text(), 'Next')]")
next_button.click()

sleep(30)
password = driver.find_element(By.XPATH, "//input[@name='password']")
load_dotenv()
twitter_password = os.getenv("password")
password.send_keys(twitter_password)
login_button=driver.find_element(By.XPATH,"//span[contains(text(), 'Log in')]")
login_button.click()

# search item and fetch it
sleep(30)
search_button = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search_button.send_keys("Elon musk")
search_button.send_keys(Keys.ENTER)

sleep(30)
people = driver.find_element(By.XPATH,"//span[contains(text(), 'People')]")
people.click()

sleep(30)
profile=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div/div[1]/div/div[1]/a/div/div[1]/span/span[1]')
profile.click()

sleep(30)
'''userTag=driver.find_element(By.XPATH,'//div[@data-testid="User-Name"]').text
timeStamp=driver.find_element(By.XPATH,'//time').get_attribute('datetime')
Tweet=driver.find_element(By.XPATH,"//div[@data-testid='tweetText']").text
reply=driver.find_element(By.XPATH,"//div[@data-testid='reply']")
reTweet=driver.find_element(By.XPATH,"//div[@data-testid='retweet']")
like=driver.find_element(By.XPATH,"//div[@data-testid='like']")
'''
# automate process
userTags=[]
timeStamps=[]
Tweets=[]
Replys=[]
reTweets=[]
Likes=[]

sleep(30)

while True:
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    
    for article in articles:
        try:
            userTag=article.find_element(By.XPATH,'.//div[@data-testid="User-Name"]').text.strip().replace("\n"," ")
            userTags.append(userTag)
            
            timeStamp=article.find_element(By.XPATH,'.//time').get_attribute('datetime')
            timeStamps.append(timeStamp)
            
            Tweet=article.find_element(By.XPATH,".//div[@data-testid='tweetText']").text.strip().replace("\n"," ")
            Tweets.append(Tweet)
            
            reply=article.find_element(By.XPATH,".//div/button[@data-testid='reply']").text
            Replys.append(reply if reply else "0")
            
            reTweet=article.find_element(By.XPATH,".//div/button[@data-testid='retweet']").text
            reTweets.append(reTweet if reTweet else "0")
            
            like=article.find_element(By.XPATH,".//div/button[@data-testid='like']").text
            Likes.append(like if like else "0")
        
        except Exception as e:
            print(f"Error extracting tweet data: {e}")
            break       
    Tweets = list(set(Tweets))
    if len(Tweets) > 5:
        break
    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    sleep(30)
    
driver.quit()
# export
import pandas as pd
df = pd.DataFrame(zip(userTags, timeStamps, Tweets, Replys, reTweets, Likes), columns=['userTags', 'timeStamps', 'Tweets', 'Replys', 'reTweets', 'Likes'])
df.to_csv(r"/home/shruti29/Desktop/Project/web scraping-twitter tweets/elonmusk_tweets.csv",index=False, quoting=csv.QUOTE_ALL)

print("Data saved successfully!")
