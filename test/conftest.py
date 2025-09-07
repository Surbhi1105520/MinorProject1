# conftest.py
import pytest
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--disable-notifications")  # optional
    drv = webdriver.Chrome(service=Service(), options=options)
    yield drv
    drv.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 12)

def logged_in_driver(driver):
    cookies_path = "guvi_cookies.json"
    driver.get("https://www.guvi.in/")  # must be on domain before add_cookie
    input("Log in manually in this window, then press Enter...")
    with open("guvi_cookies.json", "w") as f:
        json.dump(driver.get_cookies(), f)
    driver.quit()
    assert os.path.exists(cookies_path), "Run the cookie capture once to create guvi_cookies.json"
    for c in json.load(open(cookies_path)):
        # secure cookies require HTTPS domain loaded first
        driver.add_cookie(c)
    driver.refresh()
    WebDriverWait(driver, 10).until(lambda d: "guvi.in" in d.current_url)
    return driver

def _visible_big(el) -> bool:
    try:
        if not el.is_displayed():
            return False
        rect = getattr(el, "rect", {}) or {}
        return rect.get("width", 0) >= 100 and rect.get("height", 0) >= 60
    except Exception:
        return False

def recaptcha_blocking(driver) -> bool:
    """
    True only if a CAPTCHA *challenge* or *checkbox* is actually visible.
    Ignores the small grecaptcha badge (non-blocking).
    """
    # Challenge frames (full-screen or modal)
    challenge_iframes = driver.find_elements(By.CSS_SELECTOR, "iframe[title*='challenge' i], iframe[src*='bframe' i]")
    if any(_visible_big(f) for f in challenge_iframes):
        return True

    # Checkbox (I'm not a robot) anchor container
    anchors = driver.find_elements(By.CSS_SELECTOR, "#rc-anchor-container, .rc-anchor")
    if any(_visible_big(a) for a in anchors):
        return True

    # Sometimes the checkbox is embedded as a generic recaptcha iframe with anchor inside
    recaptcha_ifr = driver.find_elements(By.CSS_SELECTOR, "iframe[src*='recaptcha' i][title*='reCAPTCHA' i]")
    if any(_visible_big(f) for f in recaptcha_ifr):
        # Peek: if it’s tiny, it’s probably just a badge; big means checkbox
        return True

    # Explicitly ignore the small bottom-right badge (non-blocking)
    # .grecaptcha-badge is often ~70x60; we treat it as non-blocking by default.
    return False

def recaptcha_visible(driver) -> bool:
    """Return True only if a reCAPTCHA UI is actually visible (not just present in DOM)."""
    # Common containers:
    #  - iframe[src*='recaptcha'] (checkbox or challenge)
    #  - div.g-recaptcha (explicit render)
    #  - #rc-anchor-container, .rc-anchor (checkbox widget)
    selectors = [
        "iframe[src*='recaptcha']",
        "div.g-recaptcha",
        "#rc-anchor-container",
        ".rc-anchor",
    ]
    for css in selectors:
        for el in driver.find_elements(By.CSS_SELECTOR, css):
            try:
                if el.is_displayed():
                    rect = getattr(el, "rect", {}) or {}
                    if rect.get("width", 0) > 0 and rect.get("height", 0) > 0:
                        return True
            except Exception:
                continue
    return False

