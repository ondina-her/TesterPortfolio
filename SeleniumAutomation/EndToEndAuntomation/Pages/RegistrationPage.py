from selenium.webdriver.common.by import By

from Library import ConfigReader
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Library  import ConfigReader


class RegistrationPage:

    def __init__(self, obj):

        global driver
        driver = obj

    def enter_username(self, username):
        driver.find_element(By.ID, ConfigReader.fetchElementLocators("Registration", "username")).send_keys(username)

    def enter_lastname(self, lastname):
        driver.find_element(By.ID, ConfigReader.fetchElementLocators("Registration", "lastname")).send_keys(lastname)

