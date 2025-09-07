import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from pages.guvi_home_page import GuviHomePage
from urllib.parse import urlparse

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_positive_title(driver):
    page = GuviHomePage(driver)
    page.open()
    got = page.wait_for_title_contains("GUVI")
    assert "GUVI" in got, f"Expected 'GUVI' in title, got: {got!r}"

def test_negative_title(driver):
    page = GuviHomePage(driver)
    page.open()
    # Expect a wrong title on purpose
    try:
        page.wait_for_title_is("Totally Wrong Title", timeout=8)
        pytest.fail("Title unexpectedly matched the wrong value.")
    except TimeoutException:
        # ✅ Expected: exact title never became the wrong value
        pass