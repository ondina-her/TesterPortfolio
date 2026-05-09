#selenium test for the sliders and select box in the sidebar of the streamlit app
#streamlit app is running on localhost:8501
#streamlit run ST_Torre.py
#.venv\Scripts\activate.bat
#pip install selenium
#cd Test
#python test.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. Start Chrome and open your Streamlit app
driver = webdriver.Chrome()
driver.get("http://localhost:8501")
driver.maximize_window()

# 2. Wait until sliders are present
sliders = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-baseweb="slider"]'))
)

# 3. Use ActionChains to drag sliders (send_keys doesn’t work on Streamlit sliders)
actions = ActionChains(driver)

# Floors slider
actions.click_and_hold(sliders[0]).move_by_offset(30, 0).release().perform()
time.sleep(1)

# Rotation per floor slider
actions.click_and_hold(sliders[1]).move_by_offset(60, 0).release().perform()
time.sleep(1)

# Height per floor slider
actions.click_and_hold(sliders[2]).move_by_offset(20, 0).release().perform()
time.sleep(1)

# Radius slider
actions.click_and_hold(sliders[3]).move_by_offset(40, 0).release().perform()
time.sleep(1)

# 4. Handle dropdowns (comboboxes)
comboboxes = driver.find_elements(By.CSS_SELECTOR, '[role="combobox"]')

# First dropdown → Hexagon
comboboxes[0].click()
option = driver.find_element(By.XPATH, '//div[text()="Hexagon"]')
option.click()
time.sleep(1)

# Second dropdown → Ember
comboboxes[1].click()
option = driver.find_element(By.XPATH, '//div[text()="Ember · Red–Gold"]')
option.click()
time.sleep(1)

# 5. Pause to see results, then quit
time.sleep(5)
driver.quit()
