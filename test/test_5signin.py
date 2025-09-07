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

def test_sign_click_positive(driver):
    page = GuviHomePage(driver)
    page.open()
    el_clickable = page.wait_sign_clickable(timeout=15)
    assert el_clickable.is_enabled(), "❌ Sign button is not enabled/clickable"
    # Optional: click and verify navigation goes to sign-in page
    el_clickable.click()
    assert "/register" in driver.current_url or "sign" in driver.current_url.lower()

def test_sign_click_negative_bad_locator(driver, monkeypatch):
    page = GuviHomePage(driver)
    page.open()
    # Replace the valid locator with a bogus one temporarily
    monkeypatch.setattr(page, "SIGN_BTN", (By.ID, "signup-button-does-not-exist"))
    with pytest.raises(TimeoutException):
        page.wait_sign_clickable(timeout=5)

