# test/test_6login_negative.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.guvi_home_page import GuviHomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from selenium.webdriver.common.by import By

USER = "surbhi1105520@gmail.com"
VALID_PASS = "Avnisingh@2575"

@pytest.mark.positive
@pytest.mark.parametrize(
    "email,password,case",
    [
        ("bad_email", VALID_PASS, "invalid_email"),
        (USER, "wrong_password", "wrong_password"),
        ("bad_email", "wrong_password", "both_wrong"),
    ],
)
def test_login_rejects_invalid_credentials_shows_error(driver, email, password, case):
    # Go to homepage and open login
    home = GuviHomePage(driver)
    home.open()
    assert home.is_url_valid(), "❌ Not on GUVI homepage"

    login = LoginPage(driver)
    login.open()

    # Attempt login with invalid creds
    login.login(email, password, expect_success=False)

    # Verify NOT logged in
    wait = WebDriverWait(driver, 10)
    head = DashboardPage(driver, wait)
    assert not head.is_logged_in(), "❌ Avatar should NOT be visible after failed login"

    # Verify an error indicator/message is shown (inline or banner)
    assert login.has_login_error(), "❌ No error indicator shown for invalid login"

    # (Optional) Check message text is sensible (be tolerant to wording)
    msg = login.get_error_text()
    if msg:
        msg_l = msg.lower()
        assert any(
            key in msg_l
            for key in ["invalid", "wrong", "try again", "doesn't look", "doesnt look", "not registered", "incorrect"]
        ), f"Unexpected error text for {case}: {msg}"

    # (Optional) Also ensure we did NOT land on the signed-in homepage URL
    assert driver.current_url.rstrip("/") != home.URL.rstrip("/"), "❌ Should not be on homepage URL after failed login"

def recaptcha_present(driver):
    return bool(
        driver.find_elements(By.CSS_SELECTOR, "iframe[src*='recaptcha'], div.g-recaptcha")
    )

@pytest.mark.negative
@pytest.mark.parametrize(
    "email,password,case",
    [
        ("bad_email", VALID_PASS, "invalid_email_format"),
        (USER, "wrong_password", "wrong_password"),
        ("", VALID_PASS, "empty_email"),
        (USER, "", "empty_password"),
        ("   ", "   ", "whitespace_both"),
        ("foo@", VALID_PASS, "email_missing_domain"),
        ("@bar.com", VALID_PASS, "email_missing_local"),
    ],
    ids=lambda x: x if isinstance(x, str) else None,
)
def test_login_rejects_invalid_credentials_shows_error(driver, email, password, case):
    # Skip if reCAPTCHA is visible (site will block automation, making this flaky)
    if recaptcha_present(driver):
        pytest.skip("reCAPTCHA visible — skipping automated negative login UI test.")

    home = GuviHomePage(driver)
    home.open()
    assert home.is_url_valid(), "❌ Not on GUVI homepage"

    login = LoginPage(driver)
    login.open()

    # Attempt login with invalid creds
    login.login(email, password, expect_success=False)

    # Verify NOT logged in
    wait = WebDriverWait(driver, 10)
    head = DashboardPage(driver, wait)
    assert not head.is_logged_in(), "❌ Avatar should NOT be visible after failed login"

    # Verify an error indicator/message is shown (inline or banner)
    assert login.has_login_error(), f"❌ No error indicator shown for invalid login ({case})"

    # Optional: check message text (tolerant to copy changes)
    msg = (login.get_error_text() or "").lower()
    if msg:
        assert any(
            key in msg for key in
            ["invalid", "wrong", "try again", "doesn't look", "doesnt look", "not registered", "incorrect"]
        ), f"Unexpected error text for {case}: {msg}"

    # Ensure we did NOT land on the signed-in homepage
    assert driver.current_url.rstrip("/") != home.URL.rstrip("/"), \
        f"❌ Should not be on homepage URL after failed login ({case})"