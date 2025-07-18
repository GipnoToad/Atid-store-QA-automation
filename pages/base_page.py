from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class BasePage:
    def __init__(self, browser: Chrome, url: str):
        self.browser = browser
        self.url = url
        self.actions = ActionChains(self.browser)

    def open(self):
        self.browser.get(self.url)

    def element_is_clickable(self, locator: tuple, wait=5):
        try:
            WebDriverWait(self.browser, wait).until(EC.element_to_be_clickable(locator))
        except exceptions.TimeoutException:
            raise AssertionError(f'Element: {locator} is not clickable.')
        
    def click_element(self, locator: tuple):
        try:
            elem = self.browser.find_element(*locator)
            elem.click()
        except exceptions.ElementClickInterceptedException as ex:
            raise AssertionError(f"Element: {locator} was not clicked due {ex}")

    def click_all_elements_in_list(self, locator: tuple, wait=5):
        """Click each element located by ``locator`` using CTRL+click."""
        try:
            elems = WebDriverWait(self.browser, wait).until(
                EC.presence_of_all_elements_located(locator)
            )
            for elem in elems:
                self.actions.key_down(Keys.CONTROL).click(elem).key_up(Keys.CONTROL).perform()
        except exceptions.TimeoutException:
            raise AssertionError(f'Elements: {locator} are not clickable.')
        except exceptions.ElementClickInterceptedException as ex:
            raise AssertionError(f"Elements: {locator} were not clicked due {ex}")

    def element_is_visible(self, locator: tuple, wait=5):
        try:
            WebDriverWait(self.browser, wait).until(EC.visibility_of_element_located(locator))
            return True
        except:
            raise AssertionError(f'Element: {locator} is not visible.')

    def text_as_expected_text(self, locator:  tuple, text: str):
        try:
            elem = self.browser.find_element(*locator)
            assert elem.text == text, f"Expected text: {text}. Actual text: {elem.text}"
        except exceptions.NoSuchElementException:
            raise AssertionError(f'Element: {locator} is not found.')
        
    def get_element_name(self, locator: tuple):
        try:
            name = self.browser.find_element(*locator).text
            return name
        except exceptions.NoSuchElementException:
            raise AssertionError(f'Element: {locator} is not found.')

