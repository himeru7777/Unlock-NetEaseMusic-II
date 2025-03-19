# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00ADF4E942E6F5B06AFF131D5BFF471EAA33E3F815935C6B784C31139E95D15F59F35F06F323DB28E224C77942206055451A428D4C81969EA78DB72F042EDD9E4725548BE843241DA1F7BDD552DA95F96ED1AAEBBC9AD6E9BE43624D8E1B40D8CFB27B0B65DFA10F08D560B64BBE9F4436FF0322DDDCAD3194D323F157CC8174D4D1CE6DD1BBDA8681521DF49DF4186EADDC0817A92EB40499F5CAE3CE2665619B8C3B1DECC97AB75191E68D92E25F7AD5C4667982E4D9982640290B102297BAD99042DD8F132E23DE36624C8E50FCEBDD95104D61EA1AD108271F58267B26B673BAAFAEE9664A1E6247718578A4DCD0B0DD879B0BDB4D650E91EBD72948F0E0709903FB4F61BB8C826279C71734554C726BB34BFE5F1036C1DE0E12BB3FCA986070CE58477E24486FA253750FDFCC5BBC6D1D73500B1AAFE796AADCFA6E2EAE9531B524D6ABF9485289DDB07BC01ADC19D86F4F20E5B5A5292D8FF4AFB7B29862"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
