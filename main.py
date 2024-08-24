
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from process_video import rename_latest_mp4_to_video
from upload_video import upload_to_youtube
from chatGPT_promt import get_title_prompt_description
from select_trend import display_trends, get_keywords
import time
import os


INVIDEO_EMAIL = os.getenv("INVIDEO_EMAIL")
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
        display_trends()
        input, title, generated_prompt, description = get_title_prompt_description()
        tags = get_keywords(input)
        invideo_prompt = create_invideo_prompt(generated_prompt)
        driver = initiate_driver()
        open_page(driver, "InVideo")
        login_invideo(driver)
        create_invideo_and_download(driver, invideo_prompt)
        print("\nWaiting 2 minutes for download\n")
        time.sleep(60*2) # Waiting for download
        rename_latest_mp4_to_video()
        time.sleep(10)
        upload_to_youtube(title, description, tags)
        
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()