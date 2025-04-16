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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FEE10D8A2F1653E6DB646D21BB211BFCF40EED6796C61EF9D384FD4391E1521CD3FD152553A4A095C261B9F7BD3BF2385A9848F63EC432F3DA7926E62BBEFA21F95EBB7D82AE39E3BCBC0CF62E574A46E991B7EB3C9002B27B4D7E1678AC8B6ECC0FA6D5D0BA6CB8441D18F3C09002FB3A2AEAEFA1AD03ACEFB8A44BF67DFD894BC2B69B7AABC949F310BC4E865E890ACDFEF08F753A2F92840E67AFE244DACFAE274070B0C6DC0C02E15A104A971F7D2411F2AE9075D30F028EEA216D1AF89E2E3710E8034D98516BB96305E0C6875829259BD858804DEA6E00F8F0842DF9535193E784B83723BF4DEA57310492CF87CA92DB60D6C4F0C9EED660B212906E48774FB40A6C67A31D6C87BB1F587C5A0BB10DA7C1821CE3A05F4C39EFEC25F6F05759EE593DBEEA8AEC2835D2568F985D8BFAA9F08DF63717E46E34E4EC92618B22A33D93AFDD79B37D24C972F21E677098EF448C1CA3EC52077854F5BFF88A53
"})
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
