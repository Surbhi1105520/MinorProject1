from pages.base_page import BasePage
from pages.guvi_home_page import GuviHomePage
from pages.dashboard_page import DashboardPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
class LoginPage:
    URL = "https://www.guvi.in/sign-in/"

    #  Stored in code as requested (don’t commit secrets to Git!)
    DEFAULT_EMAIL = "surbhi1105520@gmail.com"
    DEFAULT_PASSWORD = "Avnisingh@2575"
    EMAIL_ALTS = [
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.ID, "email"),
        (By.NAME, "email"),
        (By.XPATH, "//input[contains(@placeholder,'Email') or contains(@aria-label,'email')]"),
    ]
    PASSWORD_ALTS = [
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.XPATH, "//input[@type='password']"),
    ]

    AVATAR_ALTS = [
        (By.CSS_SELECTOR, "img[alt*='avatar' i]"),
        (By.CSS_SELECTOR, "[data-testid='avatar'], [data-test='avatar']"),
        (By.CSS_SELECTOR, "header img[src*='avatar'], nav img[src*='avatar']"),
    ]
    SUBMIT_ALTS = [
    # buttons
    (By.XPATH, "//button[@type='submit']"),
    (By.XPATH, "//button[contains(@class,'login') or contains(@id,'login')]"),
    (By.XPATH, "//button[normalize-space()='Login' or normalize-space()='Sign in']"),
    # anchors that act like buttons
    (By.XPATH, "//a[@id='login-btn' or contains(@class,'login-btn')]"),
    (By.XPATH, "//a[contains(@href,'login') or contains(@href,'signin')]"),
    (By.XPATH, "(//a|//button)[normalize-space()='Login']"),
]
    LOGIN_TRIGGERS = [
        (By.XPATH, "//a[normalize-space()='Login' or normalize-space()='Sign in']"),
        (By.CSS_SELECTOR, "a[href*='login'], a[href*='signin'], button[href*='login']"),
    ]
    ERROR_ALTS = [
        (By.XPATH, "//*[contains(@class,'error') or contains(@class,'alert') or contains(@class,'toast')]"),
        (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'invalid')]"),
    ]

    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password") 
    SUBMIT = (By.ID, "#login-btn")
    AVATAR = (By.CSS_SELECTOR, 'img.gravatar[alt="Profile"]')  # post-login check
    ERROR_ALTS = [
        # Inline invalid feedback (what your screenshot shows)
        (By.CSS_SELECTOR, "div.invalid-feedback.is-invalid"),
        (By.XPATH, "//div[contains(@class,'invalid-feedback') and contains(@class,'is-invalid')]"),
        # Generic inline red text near fields
        (By.CSS_SELECTOR, ".text-danger, .error, .alert-danger, .help-block"),
        (By.XPATH, "//*[contains(@class,'text-danger') or contains(@class,'error') or contains(@class,'alert-danger')]"),
        # Banners / toasts
        (By.XPATH, "//*[contains(@class,'toast') and (contains(@class,'error') or contains(@class,'danger') or contains(@class,'invalid'))]"),
        (By.XPATH, "//*[@role='alert']"),
        # Fallback: any element that contains “password” + “try again / invalid” wording
        (By.XPATH, "//*[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'password') and "
                   "(contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'try again') "
                   "or contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'invalid') "
                   "or contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'wrong'))]"),
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


    def _first_visible(self, locators, timeout=5):
        end = time.time() + timeout
        while time.time() < end:
            for by, sel in locators:
                try:
                    el = WebDriverWait(self.driver, 0.8).until(EC.visibility_of_element_located((by, sel)))
                    if el.is_displayed():
                        return el
                except TimeoutException:
                    continue
            time.sleep(0.2)
        return None

    def _visible_any(self, locators, timeout=5) -> bool:
        """True if any of the locators becomes visible within timeout."""
        return self._first_visible(locators, timeout) is not None

    # ---- helpers to check visibility across frames ----
    def __init__(self, driver, wait=None, timeout=12):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, timeout)
 
    #test6 #test7
    def open(self):
        # Go to home then click a login trigger if present
        self.driver.get(self.URL)
        for loc in self.LOGIN_TRIGGERS:
            try:
                self.wait.until(EC.element_to_be_clickable(loc)).click()
                break
            except TimeoutException:
                continue
        self._switch_to_last_window()

    #test7
    def _visible_any_in_any_frame(self, locator_list, timeout=5):
        self.driver.switch_to.default_content()
        # default content first
        for loc in locator_list:
            try:
                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(loc))
                return True
            except TimeoutException:
                pass
        # then search all iframes
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(frame)
            for loc in locator_list:
                try:
                    WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(loc))
                    return True
                except TimeoutException:
                    pass
        self.driver.switch_to.default_content()
        return False

    def _text_of_any_in_any_frame(self, locator_list, timeout=5):
        self.driver.switch_to.default_content()
        for loc in locator_list:
            try:
                el = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(loc))
                return el.text.strip()
            except TimeoutException:
                pass
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(frame)
            for loc in locator_list:
                try:
                    el = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(loc))
                    return el.text.strip()
                except TimeoutException:
                    pass
        self.driver.switch_to.default_content()
        return ""

    # Public API used by your tests
    #test 7
    def error_visible(self) -> bool:
        return self._visible_any_in_any_frame(self.ERROR_ALTS, timeout=5)

    def get_error_text(self) -> str:
        return self._text_of_any_in_any_frame(self.ERROR_ALTS, timeout=5)

    def password_marked_invalid(self) -> bool:
        """Fallback: input itself flagged invalid (class/aria)."""
        try:
            pwd = self._find_in_any_frame(self.PASSWORD_ALTS, timeout=3)
        except TimeoutException:
            return False
        cls = (pwd.get_attribute("class") or "").lower()
        aria = (pwd.get_attribute("aria-invalid") or "").lower()
        return ("is-invalid" in cls) or (aria == "true")

    #tets6 #tets 7 
    def has_login_error(self) -> bool:
        """One-shot: true if inline/banner error visible OR input marked invalid."""
        if self.error_visible():
            return True
        return self.password_marked_invalid()


    def _find_clickable_in_any_frame(self, locator_list, timeout=8):
        self.driver.switch_to.default_content()
        # default content first
        for loc in locator_list:
            try:
                el = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(loc))
                return el
            except TimeoutException:
                pass
        # then every iframe
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(frame)
            for loc in locator_list:
                try:
                    el = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(loc))
                    return el
                except TimeoutException:
                    pass
        self.driver.switch_to.default_content()
        raise TimeoutException(f"Clickable submit not found via: {locator_list}")

    # test6 #test7
    def login(self, email, password, expect_success=True):
        email_el = self._find_in_any_frame(self.EMAIL_ALTS, timeout=8)
        pwd_el   = self._find_in_any_frame(self.PASSWORD_ALTS, timeout=8)

        # robust typing
        from selenium.webdriver.common.keys import Keys
        email = email.strip(); password = password.strip()
        email_el.click(); email_el.send_keys(Keys.CONTROL, "a", Keys.DELETE, email)
        pwd_el.click();   pwd_el.send_keys(Keys.CONTROL, "a", Keys.DELETE, password)

        # IMPORTANT: do NOT force default_content here; find the submit in the same context
        submit_el = self._find_clickable_in_any_frame(self.SUBMIT_ALTS, timeout=8)

        # scroll & click (with JS fallback for overlays)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_el)
            submit_el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", submit_el)

        # (optional) if your app sometimes opens auth in new tab
        self._switch_to_last_window()

        if expect_success:
            self.wait.until(EC.title_contains("GUVI"))
        else:
            for loc in self.ERROR_ALTS:
                try:
                    WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(loc))
                    break
                except TimeoutException:
                    continue

    def open_forgot_password(self):
        """Open the Forgot Password UI from the login view (handles modal/iframe/new tab)."""
        # Ensure login UI is open
        self.open()

        # Click the 'Forgot password' link/button (search default + iframes)
        forgot_el = self._find_in_any_frame(self.FORGOT_LINK_ALTS, timeout=8)
        forgot_el.click()

        # It might open in a new window
        self._switch_to_last_window()

        # Wait for either URL contains forgot/reset OR the reset email field is visible
        try:
            WebDriverWait(self.driver, 5).until(
                EC.url_matches(r".*(forgot|reset).*")
            )
        except TimeoutException:
            # If URL doesn't change, ensure the email field exists in current context
            self._find_in_any_frame(self.RESET_EMAIL_ALTS, timeout=8)

    def reset_password(self, email, expect_success=True):
        """Fill reset email and submit; wait for confirmation or error."""
        # Ensure we're on forgot/reset UI
        try:
            self._find_in_any_frame(self.RESET_EMAIL_ALTS, timeout=5)
        except TimeoutException:
            self.open_forgot_password()

        email_el = self._find_in_any_frame(self.RESET_EMAIL_ALTS, timeout=8)
        email_el.clear(); email_el.send_keys(email)

        self.driver.switch_to.default_content()
        clicked = False
        for loc in self.RESET_SUBMIT_ALTS:
            try:
                self.wait.until(EC.element_to_be_clickable(loc)).click()
                clicked = True
                break
            except TimeoutException:
                continue
        if not clicked:
            raise TimeoutException("Reset submit button not found/clickable")

        if expect_success:
            self._wait_any(self.RESET_CONFIRM_ALTS, timeout=8)
        else:
            self._wait_any(self.RESET_ERROR_ALTS, timeout=8)

    def on_forgot_page(self):
        """Heuristic: URL shows forgot/reset or reset email field is present."""
        if any(w in self.driver.current_url.lower() for w in ("forgot", "reset")):
            return True
        try:
            self._find_in_any_frame(self.RESET_EMAIL_ALTS, timeout=3)
            return True
        except TimeoutException:
            return False

    def forgot_confirmation_visible(self):
        return self._visible_any(self.RESET_CONFIRM_ALTS, timeout=3)

    def forgot_error_visible(self):
        return self._visible_any(self.RESET_ERROR_ALTS, timeout=3)


    def error_visible(self):
        for loc in self.ERROR_ALTS:
            try:
                el = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(loc))
                return True if el and el.is_displayed() else False
            except TimeoutException:
                continue
        return False

    # ---- helpers ---- #test6
    def _switch_to_last_window(self):
        handles = self.driver.window_handles
        if handles and self.driver.current_window_handle != handles[-1]:
            self.driver.switch_to.window(handles[-1])
    
    #test 6
    def _find_in_any_frame(self, locator_list, timeout=8):
        self.driver.switch_to.default_content()
        # try default content
        for loc in locator_list:
            try:
                return WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(loc))
            except TimeoutException:
                pass
        # try iframes
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(frame)
            for loc in locator_list:
                try:
                    return WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(loc))
                except TimeoutException:
                    pass
        self.driver.switch_to.default_content()
        raise TimeoutException(f"Could not find element via: {locator_list}")
    
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

    
    def _first_visible(self, locs, timeout=5):
        import time
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

    def _visible_any(self, locs, timeout=5) -> bool:
        return self._first_visible(locs, timeout) is not None



    def _click_first_visible(self, locs, timeout=5) -> bool:
        el = self._first_visible(locs, timeout)
        if not el:
            return False
        try:
            el.click()
            return True
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                return False

    def _find_any(self, locs, timeout=5):
        el = self._first_visible(locs, timeout)
        if not el:
            raise TimeoutException(f"None visible from {locs}")
        return el

    def _scroll(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass

    def open_profile_menu(self):
        # If logout is already visible, nothing to do
        if self._visible_any(self.LOGOUT_ALTS, 1):
            return
        # Otherwise click avatar/menu trigger
        self._click_first_visible(self.PROFILE_MENU_TRIGGERS, 5)



