from pygments.lexers import data
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import sys, os

from Pages.RegistrationPage import RegistrationPage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Library  import ConfigReader
from Base import InitiateDriver
import pytest
import openpyxl
from DataGenerate import DataGen

@pytest.mark.parametrize("data", DataGen.dataGenerator())
def test_validate_registration(data):

    driver = InitiateDriver.start_browser()
    #driver.find_element (By.ID, "firstName").send_keys("Lenovo")
    #driver.find_element (By.ID, "lastName").send_keys("Lenovo")
    #driver.find_element(By.ID, ConfigReader.fetchElementLocators("Registration", "username")).send_keys("lenovo")
    #driver.find_element(By.ID, ConfigReader.fetchElementLocators("Registration", "lastname")).send_keys("lLenovo")
    register = RegistrationPage(driver)
    register.enter_username(data[0])
    register.enter_lastname(data[1])


