#pytest -v

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501")
    driver.maximize_window()
    yield driver
    driver.quit()

class TestSliders:
    @pytest.mark.parametrize("slider_index, offset, expected_text", [
        (0, 30, "FLOORS"),
        (1, 20, "ROTATION PER FLOOR"),
        (2, 6,  "FLOOR HEIGHT"),
        (3, 40, "RADIUS")
    ], ids=["floors","rotation","height","radius"])
    def test_slider_controls(self, driver, slider_index, offset, expected_text):
        sliders = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-baseweb="slider"]'))
        )
        actions = ActionChains(driver)
        actions.click_and_hold(sliders[slider_index]).move_by_offset(offset, 0).release().perform()

        sidebar_text = driver.find_element(By.CSS_SELECTOR, '[data-testid="stSidebar"]').text
        assert expected_text in sidebar_text

class TestDropdowns:
    @pytest.mark.parametrize("dropdown_index, option_text", [
        (0, "Hexagon"),
        (1, "Ember")
    ], ids=["dropdown_hexagon","dropdown_ember"])
    def test_dropdown_controls(self, driver, dropdown_index, option_text):
        comboboxes = driver.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
        comboboxes[dropdown_index].click()
        option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//div[contains(text(),"{option_text}")]'))
        )
        option.click()

        sidebar_text = driver.find_element(By.CSS_SELECTOR, '[data-testid="stSidebar"]').text
        assert option_text in sidebar_text

# Screenshot hook on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_name = f"{item.name}.png"
            driver.save_screenshot(screenshot_name)
            print(f"Screenshot saved: {screenshot_name}")
