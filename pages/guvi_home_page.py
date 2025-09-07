from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import time
from typing import List, Tuple, Optional

class GuviHomePage(BasePage):
    URL = "https://www.guvi.in"
    LOGIN_BTN = (By.CSS_SELECTOR ,"#login-btn")
    SIGN_BTN = (By.XPATH, "//a[normalize-space()='Sign up']" )
    LOGIN_LINK = (By.LINK_TEXT, "Login")  # alternative login trigger
    
    MENU_ITEMS = [
        "Courses",
        "Practice",
        "Resources",
        "LIVE Classes",
        "Products",
        "Login",
        "Sign up",
    ]

    NAV_CONTAINERS: List[Tuple[str, str]] = [
        (By.CSS_SELECTOR, "header"),
        (By.CSS_SELECTOR, "header nav"),
        (By.CSS_SELECTOR, "nav"),
        (By.CSS_SELECTOR, "[role='navigation']"),
        (By.CSS_SELECTOR, ".navbar, .topnav, .menu, .menu-container, .navbar-nav"),
        (By.CSS_SELECTOR, "ul[role='menubar']"),
    ]

    # Add/keep common cookie acceptors (OneTrust etc.)
    COOKIE_ACCEPT_ALTS: List[Tuple[str, str]] = [
        (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
        (By.CSS_SELECTOR, "button[aria-label*='Accept']"),
        (By.XPATH, "//button[contains(.,'Accept') or contains(.,'I Agree') or contains(.,'Okay')]"),
        # (Optional) add site-specific selectors here if you see a banner
    ]

    HAMBURGER_ALTS: List[Tuple[str, str]] = [
        (By.CSS_SELECTOR, "button[aria-label*='menu' i]"),
        (By.CSS_SELECTOR, "button[aria-label*='hamburger' i]"),
        (By.CSS_SELECTOR, "button.navbar-toggler, .hamburger, .menu-toggle, [data-toggle='nav']"),
    ]

    # Panels that indicate the menu actually opened (heuristics)
    HAMBURGER_MENU_PANEL_ALTS: List[Tuple[str, str]] = [
        (By.CSS_SELECTOR, ".mobile-menu[aria-hidden='false']"),
        (By.CSS_SELECTOR, ".nav-drawer.is-open, .offcanvas.show"),
        (By.CSS_SELECTOR, "nav[aria-expanded='true'], [data-menu-open='true']"),
        (By.CSS_SELECTOR, ".navbar-collapse.show, .menu.open, .menu.is-open"),
    ]

    DOBBY_LAUNCHER_ALTS: List[Tuple[str, str]] = [
        # Common “chat” launchers
        (By.CSS_SELECTOR, "button[aria-label*='chat' i]"),
        (By.CSS_SELECTOR, "button[aria-label*='assistant' i]"),
        (By.CSS_SELECTOR, "button[aria-label*='dobby' i]"),
        # Yellow.ai typical ids/classes
        (By.CSS_SELECTOR, "#ymBtn, #ymLauncher, .ym-launcher, .ym-chat-icon"),
        # Generic floating launchers
        (By.CSS_SELECTOR, "[data-testid*='launcher' i]"),
    ]

    DOBBY_IFRAME_ALTS: List[Tuple[str, str]] = [
        (By.CSS_SELECTOR, "iframe#ymIframe"),
        (By.CSS_SELECTOR, "iframe[id*='ym' i]"),
        (By.CSS_SELECTOR, "iframe[src*='yellow' i]"),
        (By.CSS_SELECTOR, "iframe[src*='yello' i]"),  # just-in-case typos
    ]

    # The welcome popup you showed
    DOBBY_WELCOME_ALTS: List[Tuple[str, str]] = [
        (By.ID, "ym-auto-pop-up-description"),
        (By.XPATH, "//div[@id='ym-auto-pop-up-description']"),
        (By.XPATH, "//div[contains(.,\"Let's make things easier\") or contains(., 'Dobby')]"),
    ]

    URL = "https://www.guvi.in/"
    
    def __init__(self, driver, wait=None, timeout=12):
        super().__init__(driver, timeout)
        self.wait = wait or self.wait
        self.driver = driver
        self.timeout = timeout

    #test1 #test2 #test3 #test4 #test5 #test6 #test7
    def open(self):
        """Navigate to the GUVI homepage"""
        self.driver.get(self.URL)

    #test1
    def wait_for_url(self, url_fragment="guvi.in"):
        """Wait until the URL contains a fragment"""
        return super().wait_for_url(url_fragment)

    #test1
    def get_current_url(self):
        """Return current URL"""
        return super().get_current_url()

    #test1 #tets 6 #test7
    def is_url_valid(self):
        """Check if the page URL is correct"""
        return "guvi.in" in self.driver.current_url
    
    # def is_title_valid(self):
    #     """check if the page TITLE is correct"""
    #     return "GUVI | Learn to code in your native language" in self.driver.current_title
    
    
   #test3
    def wait_login_visible(self, timeout: int = None):
        return self.wait_for_visible(self.LOGIN_BTN, timeout=timeout)

    #test3
    def wait_login_clickable(self, timeout: int = None):
        return self.wait_for_clickable(self.LOGIN_BTN, timeout=timeout)

    
    def click_login(self, timeout: int = 15):
        self.wait_for_clickable(self.LOGIN_LINK, timeout).click()
        self.wait_for_url_contains("/sign-in", timeout=15)

    #test4
    def wait_sign_visible(self, timeout: int = None):
        return self.wait_for_visible(self.SIGN_BTN, timeout=timeout)

    #test4 #test5
    def wait_sign_clickable(self, timeout: int = None):
        return self.wait_for_clickable(self.SIGN_BTN, timeout=timeout)
    
    def click_sign(self, timeout: int = None):
        return self.click(self.SIGN_BTN, timeout=timeout)
    
  
    # test8
    def prepare_nav(self):
        """Put page in a consistent desktop-ish state and reveal the menu."""
        try:
            self.driver.set_window_size(1366, 900)
        except Exception:
            pass
        self._dismiss_overlays()
        self._wait_nav_ready()
        self._open_hamburger_if_present()

    #test8
    def is_menu_item_visible(self, label: str) -> bool:
        el = self._find_menu_item(label, require_visible=True)
        if el is None:
            return False
        self._scroll_into_view(el)
        rect = getattr(el, "rect", {}) or {}
        return el.is_displayed() and rect.get("width", 0) > 0 and rect.get("height", 0) > 0

    #test8
    def is_menu_item_accessible(self, label: str) -> bool:
        """
        Accessible (relaxed): visible + clickable OR clearly interactive.
        """
        el = self._find_menu_item(label, require_visible=True)
        if el is None:
            return False

        self._scroll_into_view(el)

        visible = el.is_displayed()
        clickable = False

        try:
            self.wait.until(EC.element_to_be_clickable(el))
            clickable = True
        except Exception:
            try:
                ActionChains(self.driver).move_to_element(el).pause(0.25).perform()
                self.wait.until(EC.element_to_be_clickable(el))
                clickable = True
            except Exception:
                try:
                    self.driver.execute_script("window.scrollBy(0, -80);")
                    self.wait.until(EC.element_to_be_clickable(el))
                    clickable = True
                except Exception:
                    pass

        tag = (el.tag_name or "").lower()
        href = (el.get_attribute("href") or "")
        role = (el.get_attribute("role") or "").lower()
        tabindex = el.get_attribute("tabindex")
        focusable = tabindex is not None and tabindex != ""

        interactive = (tag in ("a", "button")) or (role in ("link", "button")) or focusable or bool(href)
        return visible and (clickable or interactive)

    # -------------------------- Internals --------------------------
    #test8
    def _dismiss_overlays(self):
        for loc in self.COOKIE_ACCEPT_ALTS:
            try:
                btns = self.driver.find_elements(*loc)
                if not btns:
                    continue
                for b in btns:
                    try:
                        if b.is_displayed():
                            try:
                                b.click()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", b)
                            time.sleep(0.2)
                            return
                    except Exception:
                        continue
            except Exception:
                continue

    #test8
    def _open_hamburger_if_present(self):
        opened = False
        for loc in self.HAMBURGER_ALTS:
            try:
                btns = self.driver.find_elements(*loc)
                if not btns:
                    continue
                for b in btns:
                    try:
                        if b.is_displayed():
                            try:
                                b.click()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", b)
                            time.sleep(0.3)
                            opened = True
                            break
                    except Exception:
                        continue
                if opened:
                    break
            except Exception:
                continue

        if opened and not self._is_menu_open():
            # Nudge once more if needed
            for loc in self.HAMBURGER_ALTS:
                try:
                    btns = self.driver.find_elements(*loc)
                    for b in btns:
                        if b.is_displayed():
                            try:
                                ActionChains(self.driver).move_to_element(b).pause(0.15).click(b).perform()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", b)
                            time.sleep(0.25)
                            if self._is_menu_open():
                                return
                except Exception:
                    continue

    #test8
    def _is_menu_open(self) -> bool:
        for loc in self.HAMBURGER_MENU_PANEL_ALTS:
            try:
                panel = self.driver.find_elements(*loc)
                if any(p.is_displayed() for p in panel):
                    return True
            except Exception:
                continue
        return False

    #test8
    def _find_menu_item(self, label: str, require_visible: bool = True) -> Optional[WebElement]:
        """
        Find the first nav item whose *visible text* contains `label` (case-insensitive).
        Prefers items inside known NAV_CONTAINERS. If `require_visible`, filters hidden/zero-size nodes.
        """
        self._wait_nav_ready()

        # Case-insensitive contains on normalized text.
        # We purposely keep nodes to common nav text carriers to reduce false positives.
        # NOTE: We do *not* include the body-wide search until container search fails.
        text_ci = label.lower()
        xpath_rel = (
            ".//*[self::a or self::button or self::span or self::p]"
            "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
            f"'{text_ci}')]"
        )

        #test8
        def first_visible_match(scope: WebElement) -> Optional[WebElement]:
            # Collect all matches then pick the first that is visible & non-zero-size
            try:
                candidates = scope.find_elements(By.XPATH, xpath_rel)
            except Exception:
                candidates = []
            for el in candidates:
                if not require_visible:
                    return el
                try:
                    rect = getattr(el, "rect", {}) or {}
                    if el.is_displayed() and rect.get("width", 0) > 0 and rect.get("height", 0) > 0:
                        # Filter common hidden states
                        aria_hidden = (el.get_attribute("aria-hidden") or "").lower() == "true"
                        style = (el.get_attribute("style") or "").replace(" ", "").lower()
                        if aria_hidden:
                            continue
                        if "display:none" in style or "visibility:hidden" in style:
                            continue
                        return el
                except Exception:
                    continue
            return None

        # Search inside known nav containers first
        for container in self.NAV_CONTAINERS:
            try:
                root = self.wait.until(EC.presence_of_element_located(container))
                # Wait a beat for layout/JS menus
                el = WebDriverWait(root, 2).until(lambda r: first_visible_match(r))
                if el:
                    return el
            except Exception:
                continue

        # Fallback: whole page (as a last resort)
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_rel)))
            return first_visible_match(self.driver)
        except Exception:
            return None

    #test8
    def _wait_nav_ready(self):
        for loc in self.NAV_CONTAINERS:
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(loc))
                return
            except Exception:
                continue

    #test8
    def _scroll_into_view(self, el: WebElement):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass

    #test9
    def is_dobby_present(self, timeout: int = 20) -> bool:
        """
        Robustly check for the Dobby assistant presence.
        Returns True if launcher OR iframe OR welcome text is found
        (in main DOM or inside the Dobby iframe).
        """
        # 1) Clear blocking overlays first
        self._dismiss_overlays()

        end = time.time() + timeout
        while time.time() < end:
            # (A) Look for any launcher in main DOM
            if self._any_displayed(self.DOBBY_LAUNCHER_ALTS):
                return True

            # (B) Look for welcome text in main DOM (sometimes rendered outside iframe)
            if self._any_displayed(self.DOBBY_WELCOME_ALTS):
                return True

            # (C) Look for iframes that may contain the widget; if found, peek inside
            iframe = self._first_present(self.DOBBY_IFRAME_ALTS)
            if iframe:
                if self._welcome_inside_iframe(iframe, self.DOBBY_WELCOME_ALTS):
                    return True

            time.sleep(0.3)

        return False
    
    def _any_displayed(self, locs: List[Tuple[str, str]]) -> bool:
        for by, sel in locs:
            try:
                els = self.driver.find_elements(by, sel)
                if any(e.is_displayed() for e in els):
                    return True
            except Exception:
                continue
        return False

    def _first_present(self, locs: List[Tuple[str, str]]) -> Optional[WebElement]:
        for by, sel in locs:
            try:
                els = self.driver.find_elements(by, sel)
                for e in els:
                    if e:  # present in DOM
                        return e
            except Exception:
                continue
        return None

    def _welcome_inside_iframe(self, iframe_el: WebElement, welcome_locs: List[Tuple[str, str]]) -> bool:
        """Temporarily switch into iframe, search for welcome text, then switch back."""
        default = self.driver.current_window_handle
        try:
            self.driver.switch_to.frame(iframe_el)
            # small wait for inner DOM to paint
            WebDriverWait(self.driver, 5).until(lambda d: any(
                self._has_any(d, welcome_locs)
            ))
            return True
        except Exception:
            return False
        finally:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.window(default)
            except Exception:
                # best effort
                self.driver.switch_to.default_content()

    def _has_any(self, driver_or_ctx, locs: List[Tuple[str, str]]) -> bool:
        for by, sel in locs:
            try:
                els = driver_or_ctx.find_elements(by, sel)
                if any(e.is_displayed() for e in els):
                    return True
            except Exception:
                continue
        return False
