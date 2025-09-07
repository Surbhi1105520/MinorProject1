import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pages.guvi_home_page import GuviHomePage
from urllib.parse import urlparse

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# ✅ Positive Test
def test_positive_url(driver):
    page = GuviHomePage(driver)
    page.open()
    page.wait_for_url("guvi.in")   # wait until correct URL loads
    current = page.get_current_url()
    assert page.is_url_valid(), f"❌ Expected 'guvi.in' in URL but got {current}"
    print("✅ Positive test passed: GUVI homepage loaded successfully.")

# ❌ Negative Test
def test_negative_url(driver):
    bad_url = "https://www.guvii.in"  # intentional typo (extra 'i')

    try:
        # This may raise WebDriverException on DNS failure
        driver.get(bad_url)

    except WebDriverException as e:
        # DNS/connection errors are acceptable for the negative case
        msg = str(e)
        assert (
            "ERR_NAME_NOT_RESOLVED" in msg
            or "ERR_CONNECTION" in msg
            or "Name not resolved" in msg
            or "DNS" in msg
        ), f"Unexpected WebDriver error for negative URL: {msg}"
        return  # ✅ negative case passed via DNS failure

    # If no exception was raised, we still must ensure it's NOT GUVI
    host = urlparse(driver.current_url).netloc.lower()
    assert not host.endswith("guvi.in"), f"Unexpectedly landed on GUVI: {driver.current_url}"



