
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
from datetime import datetime, timedelta
import time
import sys
import re
import os

MY_API_KEY = os.getenv("CHAT_GPT_API_KEY")

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

def callChatGpt():
    client = OpenAI(api_key = MY_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Tell me a 6 word joke"
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def get_url():
    return "https://chatgpt.com"

def get_url(option):
    urls = {
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
    callChatGpt()
    driver = None
    try:
        driver = initiate_driver()
        open_page(driver, "Trends")

        time.sleep(20)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()
