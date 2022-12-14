from http.client import OK
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import random
import imaplib
from bs4 import BeautifulSoup
import string
import re
import requests

options = webdriver.ChromeOptions()

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def register(mail, password):

    with open('names.txt') as file:
        lines = file.read().splitlines()
    name = random.choice(lines).title()

    with open('surnames.txt') as file:
        lines = file.read().splitlines()
    surname = random.choice(lines).title()

    print('Регистрация аккаунта...')

    url = "https://www.rev.ai/auth/signup"

    driver.get(url=url)

    firstname = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "signup-firstname")))
    firstname.send_keys(name)

    lastname = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "signup-lastname")))
    lastname.send_keys(surname)

    email_register = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "signup-email")))
    email_register.send_keys(mail)

    password_register = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "signup-password")))
    password_register.send_keys(password)

    password_confirm = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "signup-confirm-password")))
    password_confirm.send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "signup-submit-button"))).click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "resend-verification-email-btn")))
    except:
        pass



def check_exists_by_path(path):
    try:
        driver.find_element(By.ID, path)
    except NoSuchElementException:
        return False
    return True

def login(mail, mailPassword, password):

    print("Аккаунт зарегистрирован")

    url = "https://www.rev.ai/auth/login"

    driver.get(url=url)

    print("Подтверждение почты...")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "login-email")))

    email_login = driver.find_element(By.ID, "login-email")
    email_login = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "login-email")))
    email_login.send_keys(mail)

    password_login = driver.find_element(By.ID, "login-password")
    password_login.send_keys(password)

    email = mail
    password = mailPassword

    try:
        time.sleep(1)
        mail = imaplib.IMAP4_SSL('imap.rambler.ru')
        mail.login(email, password)
        mail.list()
        mail.select("inbox")

        result, data = mail.search(None, "ALL")

        ids = data[0]
        id_list = ids.split()

        latest_email_id = id_list[-1]

        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')

        bs = BeautifulSoup(raw_email_string,features="html.parser")
        reInitial = str(bs)[str(bs).find('https://www.rev.ai/auth/verifyaccount?'):]
        reInitial2 = str(reInitial)[:str(reInitial).find(' target=3D"_blank')]
        result = re.sub("^\s+|\n|\r", '', reInitial2)
        s1 = result[:len(result)//2].replace("3D", "")
        s2 = result[len(result)//2:]
        s3 = s2[:len(s2)//2].replace("=", "")
        s4 = s2[len(s2)//2:].replace("3D", "")[:-1]
        url = s1 + s3 + s4

        requests.get(url)

        print("Почта подтверждена")

    except:

        print("Ошибка на стороне почты")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit-button"))).click()

    print("Выполнен вход")

    time.sleep(2)
        
    driver.get(url="https://www.rev.ai/access-token")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "access-token-generate-btn"))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "account-generate-token-btn"))).click()
        
    token = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html[@class='h-100']/body[@id='access-token-page']/div[@id='site-content']/div[@id='dashboard-content']/div[@class='pa4 mt3-ns w-100 mw7 f6']/div[@id='developer-settings']/div/div[2]/div[@class='regenerated-access-token']/div[@class='flex flex-column flex-row-l pt3']/div[@class='fs-exclude flex flex-column flex-row-l w-100 tl tr-l']/div[@class='access-token displayed w-100 ph2 pb2 br2 pointer']"))).text

    print("Токен получен")

    user_info = email + ':' + password + ":" + token

    file = open("result.txt", "a")
    file.write(user_info + "\n")
    file.close()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[@class='h-100']/body[@id='access-token-page']/div[@id='site-content']/div[@id='dashboard-sidebar']/div[2]/div[@id='dashboard-sidebar-logout']/span[@class='dark-gray text-link pl2']"))).click()

    print("Выход с аккаунта")

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "signup-firstname")))
    except:
        pass

def start():
    with open('data.txt') as file:
        lines = file.read().splitlines()

    for line in lines:
        pas = ''
        for x in range(14):
            pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        mail,password = line.split(':')
        register(mail, pas)

        if check_exists_by_path("resend-verification-email-btn"):
            login(mail, password, pas)
            continue
        else:
            print("Требуется капча. Установлена задержка")
            time.sleep(1800)
            register(mail, pas)

if __name__ == "__main__":
    start()