
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
from datetime import datetime, timedelta
from process_video import rename_latest_mp4_to_video
from upload_video import upload_to_youtube
import time
import glob
import sys
import re
import os


MY_API_KEY = os.getenv("CHAT_GPT_API_KEY")
INVIDEO_EMAIL = os.getenv("INVIDEO_EMAIL")
INVIDEO_PASSWORD = os.getenv("INVIDEO_PASSWORD")
youtube_short = True



def initiate_driver():
    print("\nInitiating driver\n")
    chrome_options = Options()
    # Set Chrome options
    prefs = {
        "download.default_directory": os.getenv("TARGET_FOLDER"),  # Directory to download video
        "download.prompt_for_download": False,  # To auto-download the file
        "directory_upgrade": True,
        "safebrowsing.enabled": True,  # Enable safe browsing
        "profile.default_content_settings.popups": 0,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver


def open_page(driver, option):
    print("Accessing URL: " + option)
    url = get_url(option)
    driver.get(url)


def enter_text(driver, xpath, text):
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    input_element.clear()
    input_element.send_keys(text)


def get_prompt():
    topic = input("\n\nPlease enter your topic: ")
    prompt = (
        f"I want you to act as a YouTube content creator, creating Youtube shorts on a broad range of "
        f"topics relating to the latest trends. I will send you a keyword that will be a "
        f"recently searched trend on YouTube. I want you to find out why this is trending on the "
        f"web (so that your information is up to date) and then find out about the trend. Use what "
        f"you find about the trend to write a script for a 50 second video. The video should be "
        f"informative, entertaining, and catch people's attention by spiking curiosity. Please start "
        f"with a clickbait title for this video, and then provide the script. Your output should "
        f"be a title introduced with 'Title: (YOUR TITLE)', then script introduced with 'Script: (YOUR SCRIPT)', "
        f"and then a video description, introduced with 'Description: (DESCRIPTION)'. Please stick to this structure."
        f"Do not add sources, do not add special characters, do not ask for comments below "
        f"and do not introduce or end of the channel as the script is for Youtube Shorts Your topic today is: {topic}"
    )
    print("\n\nTHIS IS THE PROMPT\n\n" + prompt + "\n\n")
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
    print("\nTHIS IS WHAT CHATGPT CAME UP WITH:\n\n" + completion.choices[0].message.content + "\n\n")
    return completion.choices[0].message.content


def extract_title(text):
    # Define the prefix for the title
    title_prefix = "Title: "
    # Check if the title prefix is in the text
    if title_prefix in text:
        # Find the start position of the title
        start_pos = text.find(title_prefix) + len(title_prefix)
        # Extract the part of the string after the prefix
        rest_of_text = text[start_pos:]
        # Find the end of the title (first newline character or end of string)
        end_pos = rest_of_text.find('\n')
        if end_pos == -1:
            # No newline character found, title goes to the end of the string
            end_pos = len(rest_of_text)
        # Extract the title
        title = rest_of_text[:end_pos].strip()
        return title
    else:
        return "Title not found, please rename"  # Return a default if not found

def extract_and_remove_description(input_string):
    # Find the start of the description section
    description_start = input_string.find("Description:")
    if description_start == -1:
        # If "Description:" is not found, return the original string and an empty description
        return input_string, ""
    # Extract the description content starting after "Description: "
    description_content = input_string[description_start + len("Description:"):].strip()
    # Remove the description from the original string
    updated_string = input_string[:description_start].strip()
    return updated_string, description_content

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

def wait_click_long(driver, xpath):
    wait = WebDriverWait(driver, timeout=1200, poll_frequency=5)
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
    login_code = input("\n\nPlease enter your InVideo login code: ")
    return login_code


def login_invideo(driver):
    wait_click(driver, "//button[text()='Login']")
    enter_text(driver, "//input[@name='email_id']", INVIDEO_EMAIL)
    wait_click(driver, "//button[text()='Continue with email']")
    login_code = input_invideo_login_code()
    enter_text(driver, "//input[@name='code']", login_code)
    wait_click(driver, "//button[text()='Login']")


def create_invideo_prompt(chatgpt_script):
    invideo_prompt = "Create a fun and viral Youtube short that is 50 seconds long. Here is the script and title:\n\n"
    return invideo_prompt + chatgpt_script

def create_invideo_and_download(driver, prompt):
    enter_text(driver, "//textarea[@name='brief']", prompt)
    wait_click(driver, "//div[text()='Generate a video']")
    if(youtube_short):
        wait_click_long(driver, "//button//div[text()='YouTube shorts']")
        wait_click(driver, "//div[text()='Continue']")
    else:
        wait_click_long(driver, "//div[text()='Continue']")
    wait_click_long(driver, "//div[text()='Download']")
    wait_click_long(driver, "//p[text()='Continue']")


def main():
    driver = None
    try:
        # open_page(driver, "Trends") # We can use an api to find trends such as pytrends
        # scrape_trends(driver)
        prompt = get_prompt()
        generated_prompt = call_chat_gpt(prompt)
        title = extract_title(generated_prompt)
        generated_prompt, description = extract_and_remove_description(generated_prompt)
        invideo_prompt = create_invideo_prompt(generated_prompt)
        driver = initiate_driver()
        open_page(driver, "InVideo")
        login_invideo(driver)
        create_invideo_and_download(driver, invideo_prompt)
        print("\nWaiting 2 minutes for download\n")
        time.sleep(60*2) # Waiting for download
        rename_latest_mp4_to_video()
        time.sleep(10)
        upload_to_youtube(title, description)
        
    except Exception as error:
        print(error)



if __name__ == "__main__":
    main()
