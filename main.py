
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

def get_prompt():
    topic = input("Please enter your topic: ")
    prompt = (
        f"I want you to act as a YouTube content creator, creating videos on a broad range of "
        f"topics relating to science and technology. I will send you a keyword that will be a "
        f"recently searched trend on YouTube. I want you to find out why this is trending on the "
        f"web (so that your information is up to date) and then find out about the trend. Use what "
        f"you find about the trend to write a script for a 2-minute video. The video should be "
        f"informative, entertaining, and catch people's attention by spiking curiosity. Please start "
        f"with a clickbait title for this video, and then provide the script. Your output should "
        f"be a title introduced with 'Title: (YOUR TITLE)', and the script only, no sources. Your topic today is: {topic}"
    )
    print(prompt)
    return prompt
    

def call_chat_gpt(prompt):
    client = OpenAI(api_key = MY_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are youtube content creator"},
            {
                "role": "user",
                "content": prompt
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
        "Trends": "https://trends.google.com/trends/explore?cat=174&date=now%207-d&gprop=youtube&hl=en"
    }
    url = urls.get(option)
    return url

def wait_click(driver, xpath):
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    button.click()

def scrape_trends(driver):
    # for element in elements
    #     get text
    #     append text to list
    return 0

def main():
    print("Main")
    # prompt = get_prompt()
    # call_chat_gpt(prompt)
    # call_chat_gpt()
    # driver = None
    # try:
    #     driver = initiate_driver()
    #     open_page(driver, "Trends")
    # callChatGpt()
    # driver = None
    # try:
    #     driver = initiate_driver()
    #     open_page(driver, "Trends")
        # scrape_trends(driver)

    #     time.sleep(20)
    # except Exception as error:
    #     print(error)

if __name__ == "__main__":
    main()
