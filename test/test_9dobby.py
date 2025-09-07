# test/test_9dobby.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.guvi_home_page import GuviHomePage

@pytest.mark.smoke
def test_dobby_assistant_present(driver):
    home = GuviHomePage(driver, WebDriverWait(driver, 10))
    home.open()
    assert home.is_url_valid(), "❌ Not on GUVI homepage"

    # Prepare header to dismiss overlays (optional but helpful)
    home.prepare_nav()

    assert home.is_dobby_present(), "❌ Dobby Guvi Assistant not found on homepage"

YELLOWAI_URL_PATTERNS = [
    "*yellow.ai*",
    "*yellowmessenger.com*",
    "*ymchat*",
    "*ymbot*",
]

def _cdp_supported(driver) -> bool:
    return hasattr(driver, "execute_cdp_cmd")

def _block_yellowai(driver) -> bool:
    """Block Yellow.ai widget URLs via CDP. Return True if successful."""
    try:
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": YELLOWAI_URL_PATTERNS})
        return True
    except Exception:
        return False

def _unblock_yellowai(driver):
    """Best-effort unblock / cleanup CDP network state."""
    try:
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": []})
        driver.execute_cdp_cmd("Network.disable", {})
    except Exception:
        pass

@pytest.mark.negative
def test_dobby_assistant_absent_when_widget_network_blocked(driver):
    # Skip if CDP not available (e.g., Firefox) or blocking failed
    if not _cdp_supported(driver):
        pytest.skip("CDP not supported by this driver; skipping network-block negative test.")
    if not _block_yellowai(driver):
        pytest.skip("Could not enable CDP network blocking; skipping.")

    try:
        home = GuviHomePage(driver, WebDriverWait(driver, 10))
        home.open()
        assert home.is_url_valid(), "❌ Not on GUVI homepage"

        # Clear overlays just like positive flow, but the widget network is blocked
        home.prepare_nav()

        # With Yellow.ai endpoints blocked, Dobby must NOT be detected
        assert not home.is_dobby_present(timeout=12), \
            "❌ Dobby should NOT load when Yellow.ai endpoints are blocked"
    finally:
        _unblock_yellowai(driver)