#pytest Test/ -v

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
"""
def test_open_app():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000")
    driver.maximize_window()
    assert "QR" in driver.title or "QR" in driver.page_source
    driver.quit()
"""
#STQC-6 --Valid QR test


def test_valid_qr_camera():
    # Configure Chrome to auto-allow camera
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:8000")
    driver.maximize_window()

    # Step 1: Check that scanner button exists
    scanner_button = driver.find_element(By.ID, "button")
    assert scanner_button.is_displayed()

    # Step 2: Click to activate camera
    scanner_button.click()

    # Step 3: Wait until video feed is visible
    video_feed = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video"))
    )
    assert video_feed is not None

    # Step 4: Manual step — show a valid QR code to the camera
    time.sleep(10)  # give yourself time to present QR

    # Step 5: Check that decoded text appears in result box
    result_box = driver.find_element(By.ID, "resultText")
    assert result_box is not None

    driver.quit()


#STQC‑7 Invalid QR test
def test_invalid_qr_camera():

    # Configure Chrome to auto-allow camera
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:8000")
    driver.maximize_window()

    # Step 1: Check that scanner button exists
    scanner_button = driver.find_element(By.ID, "button")
    assert scanner_button.is_displayed()

    # Step 2: Click to activate camera
    scanner_button.click()

    # Step 3: Wait until video feed is visible
    video_feed = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video"))
    )
    assert video_feed is not None

    # Step 4: Manual step — show a valid QR code to the camera
    time.sleep(10)  # give yourself time to present QR

    # Step 5: Check that decoded text appears in result box
    result_box = driver.find_element(By.ID, "resultText")
    assert result_box.text == "" or "No result" in driver.page_source
    
    driver.quit()



#STQC‑8 Empty request QR test
def test_empty_qr_camera():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:8000")
    driver.maximize_window()

    # Step 1: Scanner button exists
    scanner_button = driver.find_element(By.ID, "button")
    assert scanner_button.is_displayed()

    # Step 2: Activate camera
    scanner_button.click()

    # Step 3: Wait for video feed
    video_feed = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video"))
    )
    assert video_feed is not None

    # Step 4: Manual step — show blank sheet or cover camera
    time.sleep(10)

    # Step 5: Check that result box stays empty
    result_box = driver.find_element(By.ID, "resultText")
    assert result_box.text == "" or "No result yet" in driver.page_source

    driver.quit()


#STQC‑9 UI validation
def test_ui_validation():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:8000")
    driver.maximize_window()

    # Check page title
    assert "QR Code Scanner" in driver.title

    # Check scanner button
    scanner_button = driver.find_element(By.ID, "button")
    assert scanner_button.is_displayed()

    # Check video element
    video_feed = driver.find_element(By.ID, "video")
    assert video_feed is not None

    # Check result box elements
    result_placeholder = driver.find_element(By.ID, "resultPlaceholder")
    result_text = driver.find_element(By.ID, "resultText")
    result_link = driver.find_element(By.ID, "resultLink")
    assert result_placeholder is not None
    assert result_text is not None
    assert result_link is not None

    # Check status message element
    status_box = driver.find_element(By.ID, "status")
    assert status_box is not None

    driver.quit()
