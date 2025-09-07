from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple
import time

class DashboardPage(BasePage):
    AVATAR_ALTS = (By.CSS_SELECTOR, "img.gravatar[alt='Profile']")


    MENU_ITEMS = [
        "Courses",
        "Practice",
        "Resources",
        "LIVE Classes",
        "Our Solutions",
        "Login",
        "Sign up",
    ]

    # Common containers/toggles for responsive navs (desktop & mobile)
    NAV_CONTAINERS = [
        (By.CSS_SELECTOR, "header nav"),
        (By.CSS_SELECTOR, "nav[role='navigation']"),
        (By.CSS_SELECTOR, "header"),
    ]
    HAMBURGER_ALTS = [
        (By.CSS_SELECTOR, "button.navbar-toggler"),
        (By.CSS_SELECTOR, "button[aria-label*='menu' i]"),
        (By.CSS_SELECTOR, "button[aria-controls*='menu' i]"),
        (By.CSS_SELECTOR, ".hamburger, .menu-toggle"),
    ]

    LOGOUT_ALTS = [
    (By.XPATH, "//a[normalize-space()='Logout' or normalize-space()='Sign out']"),
    (By.CSS_SELECTOR, "a[href*='logout' i], button[aria-label*='logout' i], button[data-action='logout']"),]
    LOGIN_LINK_ALTS = [
        (By.ID, "login-btn"),
        (By.XPATH, "//a[normalize-space()='Login' or normalize-space()='Sign in']"),
        (By.CSS_SELECTOR, "a[href*='login' i], a[href*='sign-in' i]"),
    ]
    SIGNUP_LINK_ALTS = [
        (By.XPATH, "//a[normalize-space()='Sign up' or normalize-space()='Register']"),
        (By.CSS_SELECTOR, "a[href*='register' i], a[href*='signup' i]"),
    ]
    PROFILE_MENU_TRIGGERS = [
        (By.CSS_SELECTOR, "[data-testid*='avatar' i], .avatar, .user-avatar"),
        (By.CSS_SELECTOR, "button[aria-label*='profile' i], [aria-haspopup='menu']"),
    ]
    # AVATAR_ALTS: List[Tuple[str, str]] = [
    #     (By.CSS_SELECTOR, "[data-testid*='avatar' i]"),
    #     (By.CSS_SELECTOR, ".avatar, .user-avatar"),
    #     (By.CSS_SELECTOR, "img[alt*='avatar' i], img[alt*='profile' i]"),
    #     (By.CSS_SELECTOR, "header img[src*='avatar'], nav img[src*='avatar']"),
    #     (By.CSS_SELECTOR, "[aria-label*='account' i], [aria-haspopup='menu']"),
    # ]

    def __init__(self, driver, wait=None, timeout=10):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, timeout)

    # test6
    def avatar_visible(self, timeout=6):
        try:
            self.wait.until(EC.visibility_of_element_located(self.AVATAR_ALTS))
            return True
        except TimeoutException:
            return False
        # for loc in self.AVATAR_ALTS:
        #     try:
        #         WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(loc))
        #         return True
        #     except Exception:
        #         continue
        # return False

    # test6 #test7
    def is_logged_in(self):
        return self.avatar_visible()
    
    
    ##
    def wait_avatar_visible(self, timeout: int = 10):
        return self.wait_for_visible(self.AVATAR_ALTS, timeout)

    def is_avatar_visible(self, timeout: int = 5) -> bool:
        try:
            self.wait_avatar_visible(timeout)
            return True
        except TimeoutException:
            return False
        
    def _first_visible(self, locs, timeout: int = 5):
        end = time.time() + timeout
        while time.time() < end:
            for by, sel in locs:
                try:
                    el = WebDriverWait(self.driver, 0.8).until(
                        EC.visibility_of_element_located((by, sel))
                    )
                    if el.is_displayed():
                        return el
                except TimeoutException:
                    continue
            time.sleep(0.2)
        return None

    def _visible_any(self, locs, timeout: int = 5) -> bool:
        return self._first_visible(locs, timeout) is not None

    # ----- public API -----
    def is_logged_in(self) -> bool:
        return self._visible_any(self.AVATAR_ALTS, 8)
        
    def logout(self):
        self.open_profile_menu()
        item = self._find_any(self.LOGOUT_ALTS, 6)
        self._scroll(item)
        try:
            item.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", item)
        # Post-condition: logged-out UI is back
        self.wait.until(lambda d: self.is_logged_out())
    
    def is_logged_in(self) -> bool:
        return self._visible_any(self.AVATAR_ALTS, 5)

    def is_logged_out(self) -> bool:
        # Either Login or Sign up visible, and no avatar
        if self.is_logged_in():
            return False
        return self._visible_any(self.LOGIN_LINK_ALTS + self.SIGNUP_LINK_ALTS, 5)

        
    
        
    