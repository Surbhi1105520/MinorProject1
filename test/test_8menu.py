# test/test_8menu.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.guvi_home_page import GuviHomePage
from pages.header import Header

@pytest.mark.smoke
@pytest.mark.parametrize("item", GuviHomePage.MENU_ITEMS)
def test_top_menu_items_visible_and_accessible(driver, item):
    home = GuviHomePage(driver)
    home.open()
    assert home.is_url_valid(), "❌ Not on GUVI homepage"

    #header = Header(driver, WebDriverWait(driver, 10))
    home.prepare_nav()

    assert home.is_menu_item_visible(item), f"❌ Menu item not visible: {item}"
    assert home.is_menu_item_accessible(item), f"❌ Menu item not accessible (focus/click/link): {item}"
