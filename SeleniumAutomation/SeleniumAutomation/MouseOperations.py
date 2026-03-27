from selenium.webdriver import Chrome, Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By

driver = Chrome()
driver.get("https://demoqa.com/automation-practice-form")

driver.maximize_window()


driver.find_element (By.ID, "firstName").send_keys("Lenovo")

actions = ActionChains(driver)
actions.click().perform()
actions.context_click().perform()
actions.click(driver.find_element(By.XPATH)).perform()


#driver.find_element (By.XPATH, "//input[@value=´Female´]").clear()
#checkbox
#Button

time.sleep(20)
