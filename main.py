
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
INVIDEO_EMAIL = os.getenv("INVIDEO_EMAIL")
INVIDEO_PASSWORD = os.getenv("INVIDEO_PASSWORD")

def initiate_driver():
    print("Initiating driver")
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def open_page(driver, option):
    print("Accessing URL")
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
        f"be a title introduced with 'Title: (YOUR TITLE)', and the script only, no sources, no special characters. Your topic today is: {topic}"
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
    print("Getting trends")
    span_text_dict = {}
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item")))
    elements = driver.find_elements(By.CLASS_NAME, "item")
    for i in range(min(5, len(elements))):
        span_text = elements[i].find_element(By.TAG_NAME, 'bidiText').text
        span_text_dict[f'element_{i+1}'] = span_text
    print(span_text_dict)
    return 0

def input_invideo_login_code():
    login_code = input("Please enter your InVideo login code: ")
    return login_code

def login_invideo(driver):
    wait_click(driver, "//button[text()='Login']")
    enter_text(driver, "//input[@name='email_id']", INVIDEO_EMAIL)
    wait_click(driver, "//button[text()='Continue with email']")
    login_code = input_invideo_login_code()
    enter_text(driver, "//input[@name='code']", login_code)
    wait_click(driver, "//button[text()='Login']")

def create_invideo(driver, prompt):
    enter_text(driver, "//textarea[@name='brief']", prompt)
    wait_click(driver, "//div[text()='Generate a video']")
    time.sleep(30)
    wait_click(driver, "//div[text()='Continue']")


def main():
    driver = None
    try:
        driver = initiate_driver()
        # open_page(driver, "Trends")
        # scrape_trends(driver)
        prompt = get_prompt()
        generated_prompt = call_chat_gpt(prompt)
        open_page(driver, "InVideo")
        login_invideo(driver)
        create_invideo(driver, generated_prompt)
        time.sleep(60*20)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()
