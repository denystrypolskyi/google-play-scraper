import json
import logging
import os
from google_play_scraper import GooglePlayScraper

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    app_id = input("Please enter the application identifier: ")
    desired_comment_count = int(
        input("Please enter the desired number of comments to fetch: ")
    )

    scraper = GooglePlayScraper(
        app_id=app_id,
        chrome_driver_path="./chromedriver.exe",
        desired_comment_count=desired_comment_count,
    )

    app_details_json = json.dumps(scraper.app_details, indent=2, ensure_ascii=False)
    print(app_details_json)

    folder_name = "output"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = f"{scraper.app_details['title']}.txt"
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(app_details_json)
    
    logging.info(f"App details saved to {file_path}")

