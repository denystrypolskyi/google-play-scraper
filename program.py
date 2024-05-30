from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

url = 'https://play.google.com/store/apps/details?id=com.instagram.android&showAllReviews=true'

options = Options()
options.headless = True
chrome_driver_path = './chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

title = driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text
description = driver.find_element(By.XPATH, '//meta[@itemprop="description"]').get_attribute('content')
image_src = driver.find_element(By.CSS_SELECTOR, '[itemprop="image"]').get_attribute('src')
star_rating = driver.find_element(By.XPATH, '//div[@itemprop="starRating"]').text.split("\n")[0]
content_rating = driver.find_element(By.XPATH, '//span[@itemprop="contentRating"]').text
downloads_count = driver.find_element(By.XPATH, "//div[contains(text(), 'Downloads')]").find_element(By.XPATH, "preceding-sibling::*").text
updated_on = driver.find_element(By.XPATH, "//div[contains(text(), 'Updated on')]").find_element(By.XPATH, "following-sibling::*").text
contains_ads = bool(driver.find_element(By.XPATH, "//span[contains(text(), 'Contains ads')]"))
in_app_purchases = bool(driver.find_element(By.XPATH, "//span[contains(text(), 'In-app purchases')]"))

show_more_info_button = driver.find_element(By.XPATH, "//button[@aria-label='See more information on About this app']").click()

time.sleep(2)

released_on_label = driver.find_element(By.XPATH, "//*[contains(text(), 'Released on')]")
released_on = released_on_label.find_element(By.XPATH, "following-sibling::*").text

developer_label = driver.find_element(By.XPATH, "//*[contains(text(), 'Offered by')]")
developer = developer_label.find_element(By.XPATH, "following-sibling::*").text

close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close about app dialog']")
close_button.click()

comments = []

desired_comment_count = 2
current_comment_count = 0
last_height = driver.execute_script("return document.body.scrollHeight")

while current_comment_count < desired_comment_count:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            load_more_button = driver.find_element(By.XPATH, "//span[text()='See all reviews']").click()
            time.sleep(2) 
        except NoSuchElementException:
            break
        except ElementClickInterceptedException:
            break
    last_height = new_height

    elements_with_review_id = driver.find_elements(By.XPATH, "//*[@data-review-id]")

    for element in elements_with_review_id:
        if current_comment_count >= desired_comment_count:
            break
        if element.get_attribute("data-review-id"):
            try:
                comment_text = element.find_element(By.XPATH, "following-sibling::*").text
                if comment_text.strip(): 
                    comments.append(comment_text)
                    current_comment_count += 1
            except NoSuchElementException:
                pass

output = {
    "title": title,
    "releasedOn": released_on,
    "developer": developer,
    "description": description,
    "downloads": downloads_count,
    "image": image_src,
    "updatedOn": updated_on,
    "starRating": star_rating,
    "contentRating": content_rating,
    "containsAds": contains_ads,
    "inAppPurchases": in_app_purchases,
    "comments": comments
}

print(json.dumps(output, indent=2))

driver.quit()
