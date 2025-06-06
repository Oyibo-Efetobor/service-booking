from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import time
import pathlib
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--start-maximized')

# Path to your ChromeDriver (update if needed)
# For Windows, chromedriver.exe must be in PATH or specify the path below
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

username = "oyibo.efetobor"
password = "14youareR2++"

def click_reserve_seat(driver):
    from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, UnexpectedAlertPresentException
    # Agree to terms
    agree_checkbox = driver.find_element(By.ID, 'confirm_remove_original')
    if not agree_checkbox.is_selected():
        agree_checkbox.click()
    time.sleep(1)
    # Try clicking Reserve Seat with retries and alternative selectors
    from selenium.common.exceptions import UnexpectedAlertPresentException
    for i in range(5):
        # Before each click, check and accept alert if present
        try:
            alert = driver.switch_to.alert
            print(f'Pre-click: Alert present: {alert.text}')
            alert.accept()
            print('Pre-click: Alert accepted.')
            time.sleep(1)
        except Exception:
            pass
        try:
            # Try by XPATH first
            reserve_btn = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Reserve Seat']")
        except NoSuchElementException:
            # Try by CSS class as fallback
            try:
                reserve_btn = driver.find_element(By.CSS_SELECTOR, "input.bg-emerald.fg-white[type='submit']")
            except NoSuchElementException:
                print(f'Attempt {i+1}: Reserve button not found, retrying...')
                time.sleep(2)
                continue
        driver.execute_script("arguments[0].scrollIntoView(true);", reserve_btn)
        time.sleep(0.5)
        try:
            reserve_btn.click()
            print('Reservation attempted.')
            # Handle JS alert if it appears
            try:
                alert = driver.switch_to.alert
                print(f'Alert present: {alert.text}')
                alert.accept()
                print('Alert accepted.')
            except Exception:
                pass
            break
        except UnexpectedAlertPresentException:
            # Accept the alert and retry
            try:
                alert = driver.switch_to.alert
                print(f'Alert present: {alert.text}')
                alert.accept()
                print('Alert accepted after exception.')
            except Exception:
                pass
            time.sleep(1)
        except ElementClickInterceptedException:
            print(f'Attempt {i+1}: Reserve button not clickable yet, retrying...')
            time.sleep(2)
    else:
        print('Failed to click Reserve Seat after retries.')

try:
    # Step 1: Go to login page
    driver.get('https://att2.lmu.edu.ng/log/login')
    time.sleep(2)

    # Step 2: Enter username and password
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys(username)
    password_input.send_keys(password)
    # Click the submit button
    submit_btn = driver.find_element(By.NAME, 'submit')
    submit_btn.click()
    time.sleep(3)

    # Step 3: Go to service schedule page with auto-reload until successful
    max_retries = 360  # Try for up to 30 minutes (360 x 5s)
    for attempt in range(max_retries):
        driver.get('https://att2.lmu.edu.ng/check/serveChoice')
        time.sleep(5)
        # Check if we have arrived at the service schedule page
        if 'serveChoice' in driver.current_url:
            # Optionally, check for a unique element/text on the page
            print(f'Arrived at service schedule page after {attempt+1} attempt(s).')
            break
        else:
            print(f'Attempt {attempt+1}: Not yet on service schedule page, reloading...')
    else:
        print('Failed to reach service schedule page after maximum retries.')
    # Step 4: Book 1st Service if available, else fallback to 2nd Service
    from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
    try:
        select_elem = driver.find_element(By.NAME, 'pudate')
        options = select_elem.find_elements(By.TAG_NAME, 'option')
        picked = False
        for option in options:
            if '1st Service' in option.text and 'Available Slots' in option.text:
                option.click()
                picked = True
                print('Picked 1st Service.')
                click_reserve_seat(driver)
                break
        if not picked:
            for option in options:
                if '2nd Service' in option.text and 'Available Slots' in option.text:
                    option.click()
                    picked = True
                    print('Picked 2nd Service.')
                    click_reserve_seat(driver)
                    break
        if not picked:
            print('No available service to pick.')
    except NoSuchElementException as e:
        print('Could not complete booking:', e)
    time.sleep(5)
finally:
    # Take screenshot before quitting
    downloads = pathlib.Path.home() / 'Downloads'
    screenshot_dir = downloads / 'service booking'
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_path = screenshot_dir / f'service_booking_{timestamp}.png'
    driver.save_screenshot(str(screenshot_path))
    print(f'Screenshot saved to: {screenshot_path}')
    driver.quit()
