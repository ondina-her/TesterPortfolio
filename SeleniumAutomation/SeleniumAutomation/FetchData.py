from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()
driver.get("https://demoqa.com/automation-practice-form")

driver.maximize_window()

print(driver.title)
print(driver.current_url)
print(driver.page_source)


input("Presiona Enter para cerrar...")
driver.quit()

