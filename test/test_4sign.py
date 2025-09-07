# tests/test_3_login_button.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pages.guvi_home_page import GuviHomePage

@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--start-maximized")
    drv = webdriver.Chrome(options=opts)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()


def test_sign_visible_and_clickable_positive(driver):
    page = GuviHomePage(driver)
    page.open()

    # Visible
    el_visible = page.wait_sign_visible(timeout=15)
    assert el_visible.is_displayed(), "❌ Sign button is not visible"
    #assert "/register" in driver.current_url.lower()

    # Clickable
    el_clickable = page.wait_sign_clickable(timeout=15)
    assert el_clickable.is_enabled(), "❌ Sign button is not enabled/clickable"

    # Optional: click and verify navigation goes to sign-in page
    el_clickable.click()
    assert "/register" in driver.current_url or "sign" in driver.current_url.lower()

# ❌ Negative: wrong locator (intentionally) should timeout on clickability
def test_sign_button_wrong_locator_times_out(driver):
    page = GuviHomePage(driver)
    page.open()
    page.wait_for_url("guvi.in")

    WRONG_LOGIN = (By.XPATH, "//*[normalize-space()='Loginn']")  # typo on purpose

    with pytest.raises(TimeoutException):
        page.wait_for_clickable(WRONG_LOGIN, timeout=5)
