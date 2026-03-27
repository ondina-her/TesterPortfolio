from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()
driver.get("https://demoqa.com/automation-practice-form")

driver.maximize_window()


driver.find_element (By.ID, "firstName").send_keys("Lenovo")
driver.find_element (By.ID, "lastName").send_keys("Lenovo")
driver.find_element (By.ID, "userEmail").send_keys("asaj@correo.com")
driver.find_element (By.ID, "firstName").clear()
driver.find_element (By.ID, "firstName").send_keys("LLLenovo")


#driver.find_element (By.XPATH, "label.costum-control-label").clear()
#checkbox
#Button

input("Presiona Enter para cerrar...")
driver.quit()

