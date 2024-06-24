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
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class GooglePlayScraper:
    def __init__(self, app_id, chrome_driver_path, desired_comment_count=5, timeout=5):
        self.app_id = app_id
        self.url = f"https://play.google.com/store/apps/details?id={app_id}&hl=pl"
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
            return self.wait.until(
                EC.presence_of_element_located((by, value))
            ).get_attribute(attribute)
        except TimeoutException:
            logging.error(f"Timeout while waiting for element {value}")
            return None

    def click_element(self, by, value):
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            element.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            logging.error(f"Error clicking element {value}: {e}")

    def scrape_app_details(self):
        self.driver.get(self.url)

        details = {
            "title": self.get_element_text(By.XPATH, '//h1[@itemprop="name"]'),
            "description": self.get_element_attribute(
                By.XPATH, '//meta[@itemprop="description"]', "content"
            ),
            "image": self.get_element_attribute(
                By.CSS_SELECTOR, '[itemprop="image"]', "src"
            ),
            "starRating": self.get_element_text(
                By.XPATH, '//div[@itemprop="starRating"]'
            ).split("\n")[0],
            "contentRating": self.get_element_text(
                By.XPATH, '//span[@itemprop="contentRating"]'
            ),
            "downloads": self.get_element_text(
                By.XPATH, "//div[contains(text(), 'Pobrane')]/preceding-sibling::*"
            ),
            "updatedOn": self.get_element_text(
                By.XPATH,
                "//div[contains(text(), 'Ostatnia aktualizacja')]/following-sibling::*",
            ),
            "containsAds": bool(
                self.get_element_text(
                    By.XPATH, "//span[contains(text(), 'Zawiera reklamy')]"
                )
            ),
            "inAppPurchases": bool(
                self.get_element_text(
                    By.XPATH, "//span[contains(text(), 'Zakupy w aplikacji')]"
                )
            ),
        }

        self.click_element(
            By.XPATH, "//button[contains(@aria-label, 'Zobacz więcej informacji')]"
        )

        details["releasedOn"] = self.get_visible_element_text(
            By.XPATH, "//*[contains(text(), 'Data premiery')]/following-sibling::*"
        )
        details["developer"] = self.get_visible_element_text(
            By.XPATH, "//*[contains(text(), 'Oferowany przez')]/following-sibling::*"
        )

        self.click_element(By.XPATH, "//button[contains(@aria-label, 'Zamknij okno')]")

        return details

    def scrape_comments(self):
        comments = []
        current_comment_count = 0

        try:
            self.click_element(By.XPATH, "//span[text()='Pokaż wszystkie opinie']")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            logging.error(f"Error clicking 'Pokaż wszystkie opinie': {e}")

        while current_comment_count < self.desired_comment_count:
            elements_with_review_id = self.driver.find_elements(
                By.XPATH, "//*[@data-review-id]"
            )

            for element in elements_with_review_id:
                if current_comment_count >= self.desired_comment_count:
                    break
                if element.get_attribute("data-review-id"):
                    try:
                        comment_text = element.find_element(
                            By.XPATH, "following-sibling::*"
                        ).text
                        if (
                            comment_text.strip()
                            and comment_text.strip() not in comments
                        ):
                            comments.append(comment_text)
                            current_comment_count += 1
                    except NoSuchElementException:
                        continue

            if current_comment_count < self.desired_comment_count:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(false);", elements_with_review_id[-1]
                )
                time.sleep(2)

        return comments

    def scrape(self):
        try:
            app_details = self.scrape_app_details()
            app_details["comments"] = self.scrape_comments()
            return app_details
        finally:
            self.driver.quit()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    app_id = input("Proszę podaj identyfikator aplikacji: ")
    desired_comment_count = int(
        input("Proszę podaj pożądaną liczbę komentarzy do pobrania: ")
    )
    scraper = GooglePlayScraper(
        app_id=app_id,
        chrome_driver_path="./chromedriver",
        desired_comment_count=desired_comment_count,
    )
    print(json.dumps(scraper.app_details, indent=2, ensure_ascii=False))
