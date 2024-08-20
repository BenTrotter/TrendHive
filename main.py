
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import openai
from datetime import datetime, timedelta
import time
import sys
import re
import os

openai.my_api_key = os.getenv("CHAT_GPT_API_KEY")

def initiate_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def open_page(driver, option):
    url = get_url(option)
    driver.get(url)

def login(driver):
    return

def enter_text(driver, xpath, text):
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    input_element.clear()
    input_element.send_keys(text)

def get_url(option):
    urls = {
        "ChatGPT": "https://chatgpt.com",
        "InVideo": "https://invideo.io/make/youtube-video-editor/",
        "Trends": "https://trends.google.com/trends/explore?date=now%207-d&gprop=youtube&hl=en"
    }
    url = urls.get(option)
    return url

def wait_click(driver, xpath):
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    button.click()

def main():
    driver = None
    try:
        driver = initiate_driver()
        open_page(driver, "ChatGPT")

        time.sleep(20)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()
