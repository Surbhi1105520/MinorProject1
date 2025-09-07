from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, timeout: int = 10):
        """
        Base page constructor.
        :param driver: Selenium WebDriver instance
        :param timeout: default explicit wait timeout (seconds)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_url(self, url_fragment: str):
        """
        Wait until current URL contains the given fragment.
        """
        self.wait.until(EC.url_contains(url_fragment))
        return self.driver.current_url

    def get_current_url(self):
        """
        Return current URL from the browser.
        """
        return self.driver.current_url
    
    #  test2
    def wait_for_title_contains(self, text: str, timeout: int = None):
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        w.until(EC.title_contains(text))
        return self.driver.title

    #  test 2
    def wait_for_title_is(self, title: str, timeout: int = None):
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        w.until(EC.title_is(title))
        return self.driver.title

    #test 4 #tets 5
    # def wait_for_visible(self, locator, timeout: int = None):
    #     w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
    #     return w.until(EC.visibility_of_element_located(locator))
    # def wait_for_visible_any(self, locators, timeout=None):
    #     """Wait until the FIRST of multiple alternative locators is visible."""
    #     t = timeout or self.timeout
    #     end = time.time() + t
    #     last_err = None
    #     while time.time() < end:
    #         for loc in locators:
    #             try:
    #                 return WebDriverWait(self.driver, 0.8).until(
    #                     EC.visibility_of_element_located(loc)
    #                 )
    #             except TimeoutException as e:
    #                 last_err = e
    #         time.sleep(0.2)
    #     # none matched in time
    #     raise last_err or TimeoutException(f"No locator visible from: {locators}")
    
    # def wait_for_visible(self, locator, timeout=None):
    #     """Wait for a single locator (By, value) to be visible."""
    #     t = timeout or self.timeout
    #     return WebDriverWait(self.driver, t).until(
    #         EC.visibility_of_element_located(locator)
    #     )
    def _visible_any(driver, locators, per_try=0.8):
        for by, sel in locators:
            try:
                return WebDriverWait(driver, per_try).until(EC.visibility_of_element_located((by, sel)))
            except TimeoutException:
                continue
        raise TimeoutException("None visible")

    def wait_for_visible_any(self, locators, timeout=None):
        """First visible among multiple locators."""
        t = timeout or self.timeout
        end = time.time() + t
        last = None
        while time.time() < end:
            try:
                return self._visible_any(self.driver, locators)
            except TimeoutException as e:
                last = e
                time.sleep(0.2)
        raise last or TimeoutException(f"No locator visible from: {locators}")


    def wait_for_visible(self, locator, timeout=None):
        """Single (By, value) locator."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))

    
    #test 4 #test 5
    def wait_for_clickable(self, locator, timeout: int = None):
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return w.until(EC.element_to_be_clickable(locator))

    #test 3 #test 4 #test 5
    def click(self, locator, timeout: int = None):
        el = self.wait_for_clickable(locator, timeout=timeout)
        el.click()
        return el
    
    def enter_text(self, locator, text, timeout=None):
        el = self.wait_for_visible(locator, timeout)
        el.clear()
        el.send_keys("" if text is None else str(text))
        return el
    
    
    

    
    
    