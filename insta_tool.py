from selenium import webdriver
from selenium.webdriver.chrome import service as cs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

user_id = "yakamashi1092"
password = "?7gSk!$!jZB!4!_"
message = "フォローありがとうございます"
start = True


#ログイン
chrome_service = cs.Service(executable_path = 'chromedriver.exe')
driver = webdriver.Chrome(service = chrome_service)

driver.get('https://www.instagram.com/accounts/login/')

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))
username_bar = driver.find_element_by_name("username")
#ユーザーの名前またはメールアドレスを入力
username_bar.send_keys(user_id)
password_bar = driver.find_element_by_name("password")
#ユーザーの名前またはメールアドレスを入力
password_bar.send_keys(password)

password_bar.submit()
sleep(3)

#初期設定
driver.get('https://www.instagram.com/' + user_id)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')))
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()

before_follower_list = []
try:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/ul/div/li/div/div[2]/div/div/div/span/a/span')))
    for follower_user in driver.find_elements_by_xpath('/html/body/div[6]/div/div/div/div[2]/ul/div/li/div/div[2]/div/div/div/span/a/span'):
        before_follower_list.append(follower_user.text)
except:
    pass
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[1]/div/div[2]/button')))
driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[1]/div/div[2]/button').click()

def page_click(xpath):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    driver.find_element_by_xpath(xpath).click()

def main():
    global message
    global start
    #新規フォロワーリストの取得
    #ポップアップを開く
    page_click('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    global before_follower_list
    current_follower_list = []
    new_follower_list = []
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/ul/div/li/div/div[2]/div/div/div/span/a/span')))
        for follower_user in driver.find_elements_by_xpath('/html/body/div[6]/div/div/div/div[2]/ul/div/li/div/div[2]/div/div/div/span/a/span'):
            current_follower_list.append(follower_user.text)

        for user in current_follower_list:
            if not user in before_follower_list:
                new_follower_list.append(user)
    except:
        pass
    print(before_follower_list)
    print(current_follower_list)
    print(new_follower_list)
    before_follower_list = current_follower_list

    #ポップアップを閉じる
    page_click('/html/body/div[6]/div/div/div/div[1]/div/div[2]/button')
    if len(current_follower_list) == 0:
        return

    page_click('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/a')
    if start:
        sleep(3)
        page_click('/html/body/div[6]/div/div/div/div[3]/button[2]')
        start = False

    #新規フォロワーへメッセージの送信
    for user in new_follower_list:
        #メッセージを開く
        page_click('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input')))
        search_bar = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input')
        search_bar.send_keys(user)
        search_bar.send_keys(Keys.TAB)
        sleep(1)
        page_click('/html/body/div[6]/div/div/div[2]/div[2]/div/div')
        page_click('/html/body/div[6]/div/div/div[1]/div/div[2]/div/button')

        #メッセージを送信        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        message_bar = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        message_bar.send_keys(message)
        page_click('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')

        #再度メッセージを開く
        page_click('//*[@id="react-root"]/section/div/div[1]/div/div[3]/div/div[2]/a')

    #プロフィール欄に戻る
    driver.get('https://www.instagram.com/' + user_id)

#リロード
while True:
    driver.refresh()
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span')))
        if len(before_follower_list) != int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').text):
            main()
    except:
        pass
    sleep(random.randrange(1800, 3600, 60))