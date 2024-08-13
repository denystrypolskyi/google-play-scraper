import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import time

from webdriver_utils import WebDriverUtils

class GooglePlayScraper:
    def __init__(self, app_id, chrome_driver_path, desired_comment_count=5, timeout=5):
        self.app_id = app_id
        self.url = f"https://play.google.com/store/apps/details?id={app_id}"
        self.desired_comment_count = desired_comment_count
        self.timeout = timeout
        
        self.service = Service(chrome_driver_path)
        
        self.options = Options()
        self.options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.utils = WebDriverUtils(self.driver, self.wait)

        self.app_details = self.scrape()

    def scrape_app_details(self):
        self.driver.get(self.url)

        details = {
            "title": self.utils.get_element_text(By.XPATH, '//h1[@itemprop="name"]'),
            "description": self.utils.get_element_attribute(By.XPATH, '//meta[@itemprop="description"]', "content"),
            "image": self.utils.get_element_attribute(By.CSS_SELECTOR, '[itemprop="image"]', "src"),
            "starRating": self.utils.get_element_text(By.XPATH, '//div[@itemprop="starRating"]').split("\n")[0],
            "contentRating": self.utils.get_element_text(By.XPATH, '//span[@itemprop="contentRating"]'),
            "downloads": self.utils.get_element_text(By.XPATH, "//div[contains(text(), 'Downloads')]/preceding-sibling::*"),
            "updatedOn": self.utils.get_element_text(By.XPATH, "//div[contains(text(), 'Updated on')]/following-sibling::*"),
            "containsAds": bool(self.utils.get_element_text(By.XPATH, "//span[contains(text(), 'Contains ads')]")),
            "inAppPurchases": bool(self.utils.get_element_text(By.XPATH, "//span[contains(text(), 'In-app purchases')]")),
        }

        self.utils.click_element(By.XPATH, "//button[contains(@aria-label, 'See more information on About this app')]")
        details["releasedOn"] = self.utils.get_visible_element_text(By.XPATH, "//*[contains(text(), 'Released on')]/following-sibling::*")
        details["developer"] = self.utils.get_visible_element_text(By.XPATH, "//*[contains(text(), 'Offered by')]/following-sibling::*")
        self.utils.click_element(By.XPATH, "//button[contains(@aria-label, 'Close about app dialog')]")

        return details

    def scrape_comments(self):
        comments = []
        current_comment_count = 0

        try:
            self.utils.click_element(By.XPATH, "//button[contains(@aria-label, 'See more information on Ratings and reviews')]")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            logging.error(f"Error clicking 'See more information on Ratings and reviews': {e}")

        while current_comment_count < self.desired_comment_count:
            elements_with_review_id = self.driver.find_elements(By.XPATH, "//*[@data-review-id]")

            for element in elements_with_review_id:
                if current_comment_count >= self.desired_comment_count:
                    break
                if element.get_attribute("data-review-id"):
                    try:
                        comment_text = element.find_element(By.XPATH, "following-sibling::*").text
                        if comment_text.strip() and comment_text.strip() not in comments:
                            comments.append(comment_text)
                            current_comment_count += 1
                    except NoSuchElementException:
                        continue

            if current_comment_count < self.desired_comment_count:
                self.driver.execute_script("arguments[0].scrollIntoView(false);", elements_with_review_id[-1])
                time.sleep(2)

        return comments

    def scrape(self):
        try:
            app_details = self.scrape_app_details()
            app_details["comments"] = self.scrape_comments()
            return app_details
        finally:
            self.driver.quit()