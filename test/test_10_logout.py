from pages.guvi_home_page import GuviHomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from selenium.webdriver.support.ui import WebDriverWait
import pytest

USER = "surbhi1105520@gmail.com"
PASS = "Avnisingh@2575"

def test_positive_login_shows_avatar(driver):
    home = GuviHomePage(driver)
    home.open()
    assert home.is_url_valid(), "❌ Not on GUVI homepage"

    login = LoginPage(driver)
    login.open()
    login.login(USER, PASS, expect_success=True)
    # Define wait using WebDriverWait
    
    wait = WebDriverWait(driver, 10)
    head = DashboardPage(driver, wait)
    assert head.is_logged_in , "❌ Avatar not visible after login"

def test_negative_login_wrong_password(driver):
    home = GuviHomePage(driver)
    home.open()
    assert home.is_url_valid(), "❌ Not on GUVI homepage"

    login = LoginPage(driver)
    login.open()
    login.login(USER, "wrong_password", expect_success=False)

    wait = WebDriverWait(driver, 10)
    head = DashboardPage(driver, wait)

    # Not logged in
    assert not head.is_logged_in(), "❌ Avatar should NOT be visible after failed login"

    # Accept either inline invalid-feedback OR an error banner/toast
    assert login.has_login_error(), "❌ No visible error or invalid state after wrong password"
