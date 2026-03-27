from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from Library import ConfigReader


def start_browser():
    driver = Chrome()
    if ((ConfigReader.readConfigData('Details', 'Browser'))== 'chrome'):
        driver.get("https://demoqa.com/automation-practice-form")
    elif ((ConfigReader.readConfigData('Details', 'Browser'))== 'firefox'):
        driver.get("https://demoqa.com/automation-practice-form")

    driver.get(ConfigReader.readConfigData('Details', 'Application_URL'))
    driver.maximize_window()
    return driver

def close_browser(driver):
    driver.close()

