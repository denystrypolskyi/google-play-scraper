import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options

class WebDriverUtils:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def get_element_text(self, by, value):
        try:
            return self.wait.until(EC.presence_of_element_located((by, value))).text
        except TimeoutException:
            logging.error(f"Timeout while waiting for element {value}")
            return None

    def get_visible_element_text(self, by, value):
        try:
            return self.wait.until(EC.visibility_of_element_located((by, value))).text
        except TimeoutException:
            logging.error(f"Timeout while waiting for visible element {value}")
            return None

    def get_element_attribute(self, by, value, attribute):
        try:
            return self.wait.until(EC.presence_of_element_located((by, value))).get_attribute(attribute)
        except TimeoutException:
            logging.error(f"Timeout while waiting for element {value}")
            return None

    def click_element(self, by, value):
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            logging.error(f"Error clicking element {value}: {e}")
