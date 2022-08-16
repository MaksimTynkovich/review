from http.client import OK
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
import random
import imaplib
from bs4 import BeautifulSoup
import string
import re
import requests

options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.page_load_strategy = 'eager'
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    firstname = driver.find_element(By.ID, "signup-firstname")
    firstname.send_keys(name)
    
    lastname = driver.find_element(By.ID, "signup-lastname")
    lastname.send_keys(surname)

    email_register = driver.find_element(By.ID, "signup-email")
    email_register.send_keys(mail)

    password_register = driver.find_element(By.ID, "signup-password")
    password_register.send_keys(password)

    password_confirm = driver.find_element(By.ID, "signup-confirm-password")
    password_confirm.send_keys(password)

    time.sleep(1)

    driver.find_element(By.ID, "signup-submit-button").click()

    print("Аккаунт зарегистрирован")

    time.sleep(1)

def login(mail, password):

    url = "https://www.rev.ai/auth/login"

    driver.get(url=url)

    email_login = driver.find_element(By.ID, "login-email")
    email_login.send_keys(mail)

    password_login = driver.find_element(By.ID, "login-password")
    password_login.send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit-button"))).click()

    print("Попытка входа...")

    time.sleep(5)

    if driver.current_url != 'https://www.rev.ai/auth/login':

        print("Успешный вход")

        time.sleep(1)
        
        driver.get(url="https://www.rev.ai/access-token")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "access-token-generate-btn"))).click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "account-generate-token-btn"))).click()

        time.sleep(1)

        token = driver.find_element(By.CLASS_NAME, "access-token").text
            
        print("Токен получен")

        data = mail + ':' + password + ":" + token

        file = open("result.txt", "a")
        file.write(data + "\n")
        file.close()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[@class='h-100']/body[@id='access-token-page']/div[@id='site-content']/div[@id='dashboard-sidebar']/div[2]/div[@id='dashboard-sidebar-logout']/span[@class='dark-gray text-link pl2']"))).click()
        time.sleep(1)

        print("Выход с аккаунта")
    else:
        print("Неверные данные")

def mail_confirm(email, password):
    
    print("Подтверждение почты...")

    time.sleep(5)

    email = email
    password = password

    try:
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


def start():
    with open('data.txt') as file:
        lines = file.read().splitlines()

    for line in lines:
        pas = ''
        for x in range(14):
            pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        mail,password = line.split(':')
        register(mail, pas)
        mail_confirm(mail,password)
        login(mail,pas)

if __name__ == "__main__":
    start()