
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
from datetime import datetime, timedelta
from process_video import rename_and_move_latest_file
from upload_video import upload_to_youtube
import time
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
        f"you find about the trend to write a script for a 2-minute video. The video should be "
        f"informative, entertaining, and catch people's attention by spiking curiosity. Please start "
        f"with a clickbait title for this video, and then provide the script. Your output should "
        f"be a title introduced with 'Title: (YOUR TITLE)', and the script only, no sources, no special characters. No introducing or ending of the channel as the script is for Youtube Shorts Your topic today is: {topic}"
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
    login_code = input("\n\nPlease enter your InVideo login code: ")
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
    wait = 2
    print(f"\nWaiting for {str(wait)} minutes for InVideo to analyse...\n")
    time.sleep(60*wait)
    if(youtube_short):
        wait_click(driver, "//button//div[text()='YouTube shorts']")
        wait_click(driver, "//div[text()='Continue']")
    else:
        wait_click(driver, "//div[text()='Continue']")


def download_invideo():
    return "" # Needs implementing


def rename_and_move_video_from_downloads():
    downloads_folder = os.path.expanduser("~/Downloads")
    target_folder = os.getenv("TARGET_FOLDER") 
    new_filename = "video.mp4"
    rename_and_move_latest_file(downloads_folder, target_folder, new_filename)



def main():
    driver = None
    try:
        # open_page(driver, "Trends") # We can use an api to find trends such as pytrends
        # scrape_trends(driver)
        prompt = get_prompt()
        generated_prompt = call_chat_gpt(prompt)
        title = extract_title(generated_prompt)
        # driver = initiate_driver()
        # open_page(driver, "InVideo")
        # login_invideo(driver)
        # create_invideo(driver, generated_prompt)
        # print("\n\nWe have not implemented downloading yet, please go and download video to your downloads folder once video has been created. The next process will start in 20 minutes.\n\n")
        # time.sleep(60*12) # Waiting for InVideo to generate video, this should be fine tuned / improved by waiting
        # download_invideo() # Currently not implemented, this step will need to be done manually
        # time.sleep(60*3) # Waiting for download
        # rename_and_move_video_from_downloads()
        # upload_to_youtube(title, "descripition")
        
    except Exception as error:
        print(error)



if __name__ == "__main__":
    main()
