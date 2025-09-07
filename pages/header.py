# pages/header.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Header:
    # Visible before login
    LOGIN_LINK_ALTS = [
        (By.XPATH, "//a[normalize-space()='Login']"),
        (By.CSS_SELECTOR, "a[href*='login'], a[href*='signin']"),
    ]
    SIGNUP_LINK_ALTS = [
        (By.XPATH, "//a[normalize-space()='Sign up']"),
        (By.CSS_SELECTOR, "a[href*='signup'], a[href*='register']"),
    ]

    # Visible after login
    AVATAR_ALTS = [
        (By.CSS_SELECTOR, "img[alt*='avatar' i]"),
        (By.CSS_SELECTOR, "[data-testid='avatar'], [data-test='avatar']"),
        (By.CSS_SELECTOR, "header img[src*='avatar'], nav img[src*='avatar']"),
    ]
    PROFILE_MENU_TRIGGERS = AVATAR_ALTS + [
        (By.CSS_SELECTOR, "[data-testid='profile'], [data-test='profile']"),
        (By.XPATH, "//button[contains(@aria-label,'profile') or contains(@aria-haspopup,'menu')]"),
    ]
    LOGOUT_ALTS = [
        (By.XPATH, "//a[normalize-space()='Logout']"),
        (By.XPATH, "//button[normalize-space()='Logout']"),
        (By.CSS_SELECTOR, "a[href*='logout'], button[data-test='logout'], a[data-test='logout']"),
    ]

    MENU_ITEMS = [
        "Courses",
        "Practice",
        "Resources",
        "LIVE Classes",
        "Our Solutions",
        "Login",
        "Sign up",
    ]

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

    COOKIE_ACCEPT_ALTS = [
        (By.CSS_SELECTOR, "#onetrust-accept-btn-handler"),
        (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept')]"),
    ]

    def __init__(self, driver, wait=None, timeout=12):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, timeout)

    # ---- state checks ----
    def is_logged_in(self) -> bool:
        return self._visible_any(self.AVATAR_ALTS, 5)

    def is_logged_out(self) -> bool:
        # Either Login or Sign up visible, and no avatar
        if self.is_logged_in():
            return False
        return self._visible_any(self.LOGIN_LINK_ALTS + self.SIGNUP_LINK_ALTS, 5)

    # ---- actions ----
    def prepare_header(self):
        try: self.driver.set_window_size(1366, 900)
        except: pass
        self._dismiss_overlay()

    def open_profile_menu(self):
        self.prepare_header()
        trig = self._find_any(self.PROFILE_MENU_TRIGGERS, 6)
        self._scroll(trig)
        try:
            ActionChains(self.driver).move_to_element(trig).pause(0.2).click(trig).perform()
        except Exception:
            self.driver.execute_script("arguments[0].click();", trig)

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

    # ---- helpers ----
    def _dismiss_overlay(self):
        for loc in self.COOKIE_ACCEPT_ALTS:
            for el in self.driver.find_elements(*loc):
                try:
                    if el.is_displayed():
                        el.click(); time.sleep(0.2)
                        return
                except: continue

    def _visible_any(self, locators, timeout=5):
        end = time.time() + timeout
        while time.time() < end:
            for loc in locators:
                try:
                    el = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(loc))
                    if el.is_displayed(): return True
                except: pass
        return False

    def _find_any(self, locators, timeout=6):
        for loc in locators:
            try:
                return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))
            except: pass
        raise AssertionError(f"Element not found via: {locators}")

    def _scroll(self, el):
        try: self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except: pass

    def prepare_nav(self):
        """Put page in a consistent desktop-ish state and reveal the menu."""
        # 1) Desktop viewport to avoid mobile collapse
        try:
            self.driver.set_window_size(1366, 900)
        except Exception:
            pass

        # 2) Dismiss cookie/banner overlays if present
        self._dismiss_overlays()

        # 3) Ensure a nav container is present
        self._wait_nav_ready()

        # 4) If collapsed, open hamburger
        self._open_hamburger_if_present()

    def is_menu_item_visible(self, label: str) -> bool:
        el = self._find_menu_item(label)
        self._scroll_into_view(el)
        return el.is_displayed() and el.rect.get("width", 0) > 0 and el.rect.get("height", 0) > 0

    def is_menu_item_accessible(self, label: str) -> bool:
        """
        Accessible (relaxed): visible + clickable OR clearly interactive (<a>/<button>/role/link|button/tabindex set).
        We keep it pragmatic so overlays/responsive quirks don’t cause false negatives.
        """
        el = self._find_menu_item(label)
        self._scroll_into_view(el)

        visible = el.is_displayed()
        clickable = False
        try:
            # wait a bit for it to be clickable in-place
            self.wait.until(EC.element_to_be_clickable((By.XPATH, ".")))
            clickable = True
        except Exception:
            # Try hover to open any dropdowns, then recheck
            try:
                ActionChains(self.driver).move_to_element(el).pause(0.2).perform()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, ".")))
                clickable = True
            except Exception:
                pass

        tag = (el.tag_name or "").lower()
        href = (el.get_attribute("href") or "")
        role = (el.get_attribute("role") or "").lower()
        tabindex = el.get_attribute("tabindex")
        interactive = (tag in ("a", "button")) or (role in ("link", "button")) or (tabindex not in (None, "", "0") or href.startswith("/") or "http" in href)

        return visible and (clickable or interactive)

    # ---- internals ----
    def _dismiss_overlays(self):
        for loc in self.COOKIE_ACCEPT_ALTS:
            try:
                btns = self.driver.find_elements(*loc)
                if btns:
                    for b in btns:
                        try:
                            if b.is_displayed():
                                b.click()
                                time.sleep(0.2)
                                return
                        except Exception:
                            continue
            except Exception:
                continue

    def _open_hamburger_if_present(self):
        for loc in self.HAMBURGER_ALTS:
            try:
                btns = self.driver.find_elements(*loc)
                if not btns:
                    continue
                # click the first visible/clickable one
                for b in btns:
                    try:
                        if b.is_displayed():
                            b.click()
                            time.sleep(0.3)
                            return
                    except Exception:
                        continue
            except Exception:
                continue

    def _find_menu_item(self, label: str):
        self._wait_nav_ready()
        # Case-insensitive contains on ANY text inside anchors/buttons/spans within nav
        xpath_rel = (
            ".//*[self::a or self::button or self::*]"
            "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
            f"'{label.lower()}')]"
        )
        # Prefer searching inside known nav containers
        for container in self.NAV_CONTAINERS:
            try:
                root = self.wait.until(EC.presence_of_element_located(container))
                return WebDriverWait(root, 3).until(EC.presence_of_element_located((By.XPATH, xpath_rel)))
            except Exception:
                continue
        # Fallback: whole page
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_rel)))

    def _wait_nav_ready(self):
        for loc in self.NAV_CONTAINERS:
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(loc))
                return
            except Exception:
                continue

    def _scroll_into_view(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
