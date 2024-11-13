import json
import random
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from urllib.parse import urlparse
import pandas as pd

# Path to Microsoft Edge WebDriver
msedgedriver_path = r'C:\\Users\\mouns\\Documents\\fiverr\\Orders\\Order 16\\scrapping tool\\msedgedriver.exe'

# User agents for random selection in CNN scraper
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36"
]

# Initialize WebDriver
def initialize_driver(user_agent=None):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")

    driver_service = Service(msedgedriver_path)
    driver = webdriver.Edge(service=driver_service, options=options)
    driver.set_page_load_timeout(300)
    driver.implicitly_wait(30)
    return driver

# BBC scraping function
def scrap_articles_bbc(names_list):
    article_data = []

    def search_and_scrape(name, news_site="BBC"):
        driver = initialize_driver()
        try:
            search_query = f"{news_site} {name}"
            search_url = f"https://www.google.com/search?q={search_query}"

            driver.get(search_url)
            wait = WebDriverWait(driver, 60)

            results = driver.find_elements(By.CSS_SELECTOR, "div.g")
            found_link = False
            for result in results:
                try:
                    cite_element = result.find_element(By.TAG_NAME, "cite")
                    if "bbc.com" in cite_element.text:
                        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                        print(f"Found BBC link for '{name}': {link}")
                        driver.get(link)
                        found_link = True
                        break
                except NoSuchElementException:
                    continue

            if not found_link:
                print(f"No BBC link found for '{name}' on {news_site}.")
                return

            time.sleep(random.uniform(2, 4))
            title = driver.find_element(By.TAG_NAME, 'h1').text if driver.find_elements(By.TAG_NAME, 'h1') else 'NA'
            paragraphs = driver.find_elements(By.CSS_SELECTOR, 'article p')
            text = ' '.join([para.text for para in paragraphs if para.text])

            article_data.append({
                'Name': name,
                'Website': news_site,
                'Link': driver.current_url,
                'Title': title,
                'Text': text
            })

        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            print(f"Error for '{name}' on {news_site}: {e}")
        finally:
            driver.quit()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(search_and_scrape, name) for name in names_list]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

    return json.dumps(article_data, ensure_ascii=False, indent=4)

# CNN scraping function with unified structure
def scrap_articles_cnn(names_list):
    article_data = []

    def search_and_scrape(name):
        driver = initialize_driver(user_agent=random.choice(user_agents))
        wait = WebDriverWait(driver, 15)
        search_query = f"{name} site:cnn.com"
        search_url = f"https://www.google.com/search?q={search_query}"

        try:
            driver.get(search_url)
            time.sleep(random.uniform(8, 12))

            cnn_links = []
            results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
            for result in results:
                try:
                    cite_element = result.find_element(By.TAG_NAME, 'cite')
                    if "cnn.com" in cite_element.text:
                        link = result.find_element(By.TAG_NAME, "a").get_attribute('href')
                        if link not in cnn_links:
                            cnn_links.append(link)
                except NoSuchElementException:
                    continue

            if not cnn_links:
                print(f"No CNN links found for '{name}'.")
                return

            for link in cnn_links:
                driver.get(link)
                time.sleep(random.uniform(8, 12))

                try:
                    title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
                    article_title = title_element.text
                    text_elements = driver.find_elements(By.CSS_SELECTOR, 'article p')
                    article_text = ' '.join([element.text for element in text_elements if element.text])

                    article_data.append({
                        'Name': name,
                        'Website': "CNN",
                        'Link': link,
                        'Title': article_title,
                        'Text': article_text
                    })

                except Exception as e:
                    print(f"Error extracting details from '{link}': {e}")

        except Exception as e:
            print(f"Error processing '{name}': {e}")
        finally:
            driver.quit()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(search_and_scrape, name) for name in names_list]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

    return json.dumps(article_data, ensure_ascii=False, indent=4)

# Main function to scrape articles from either BBC or CNN
def scrape_articles(names_list, source="BBC"):
    if source == "BBC":
        return scrap_articles_bbc(names_list)
    elif source == "CNN":
        return scrap_articles_cnn(names_list)
    else:
        print(f"Unknown source: {source}")
        return json.dumps([])


