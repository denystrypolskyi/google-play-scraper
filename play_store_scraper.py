import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementClickInterceptedException, 
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PlayStoreScraper:
    def __init__(self, app_id, chrome_driver_path, desired_comment_count=2, timeout=5):
        self.app_id = app_id
        self.url = f'https://play.google.com/store/apps/details?id={app_id}&showAllReviews=true'
        self.desired_comment_count = desired_comment_count
        self.timeout = timeout

        self.service = Service(chrome_driver_path)
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, self.timeout)
        
        self.app_details = self.scrape()
        
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
            self.wait.until(EC.element_to_be_clickable((by, value))).click()
        except (TimeoutException, ElementClickInterceptedException, WebDriverException) as e:
            logging.error(f"Error clicking element {value}: {e}")

    def scrape_app_details(self):
        self.driver.get(self.url)
        
        details = {
            "title": self.get_element_text(By.XPATH, '//h1[@itemprop="name"]'),
            "description": self.get_element_attribute(By.XPATH, '//meta[@itemprop="description"]', 'content'),
            "image": self.get_element_attribute(By.CSS_SELECTOR, '[itemprop="image"]', 'src'),
            "starRating": self.get_element_text(By.XPATH, '//div[@itemprop="starRating"]').split("\n")[0],
            "contentRating": self.get_element_text(By.XPATH, '//span[@itemprop="contentRating"]'),
            "downloads": self.get_element_text(By.XPATH, "//div[contains(text(), 'Downloads')]/preceding-sibling::*"),
            "updatedOn": self.get_element_text(By.XPATH, "//div[contains(text(), 'Updated on')]/following-sibling::*"),
            "containsAds": bool(self.get_element_text(By.XPATH, "//span[contains(text(), 'Contains ads')]")),
            "inAppPurchases": bool(self.get_element_text(By.XPATH, "//span[contains(text(), 'In-app purchases')]"))
        }

        self.click_element(By.XPATH, "//button[@aria-label='See more information on About this app']")
        
        details["releasedOn"] = self.get_visible_element_text(By.XPATH, "//*[contains(text(), 'Released on')]/following-sibling::*")
        details["developer"] = self.get_visible_element_text(By.XPATH, "//*[contains(text(), 'Offered by')]/following-sibling::*")
        
        self.click_element(By.XPATH, "//button[@aria-label='Close about app dialog']")
        
        return details

    def scrape_comments(self):
        comments = []
        current_comment_count = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while current_comment_count < self.desired_comment_count:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                try:
                    self.click_element(By.XPATH, "//span[text()='See all reviews']")
                except NoSuchElementException:
                    break
                except ElementClickInterceptedException:
                    break
            
            last_height = new_height
            elements_with_review_id = self.driver.find_elements(By.XPATH, "//*[@data-review-id]")
            
            for element in elements_with_review_id:
                if current_comment_count >= self.desired_comment_count:
                    break
                if element.get_attribute("data-review-id"):
                    try:
                        comment_text = element.find_element(By.XPATH, "following-sibling::*").text
                        if comment_text.strip():
                            comments.append(comment_text)
                            current_comment_count += 1
                    except NoSuchElementException:
                        continue
        
        return comments

    def scrape(self):
        try:
            app_details = self.scrape_app_details()
            app_details["comments"] = self.scrape_comments()
            return app_details
        finally:
            self.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    app_id = input("Please enter the app ID: ")
    scraper = PlayStoreScraper(app_id=app_id, chrome_driver_path='./chromedriver.exe')
    print(json.dumps(scraper.app_details, indent=2))
    input("Press any key to exit...")