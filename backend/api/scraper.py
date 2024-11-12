import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from selenium.webdriver.edge.options import Options
from urllib.parse import urlparse

# Path to Microsoft Edge WebDriver
msedgedriver_path = r'C:\\Users\\mouns\\Documents\\fiverr\\Orders\\Order 16\\scrapping tool\\msedgedriver.exe'

# Function to initialize the WebDriver
def initialize_driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for better performance
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")

    driver_service = Service(msedgedriver_path)
    driver = webdriver.Edge(service=driver_service, options=options)
    driver.set_page_load_timeout(300)  # Increase to 300 seconds
    driver.implicitly_wait(30)  # Set implicit wait to 30 seconds

    return driver

# Function to safely load a URL with retries
def safe_get(driver, url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            driver.get(url)
            return True
        except TimeoutException:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("Failed to load after multiple attempts.")
                return False

# Function to check if a URL is a topic/list page
def is_topic_page(url):
    parsed_url = urlparse(url)
    return '/topics/' in parsed_url.path

# Function to get article links from a topic page
def get_article_links_from_topic_page(driver, max_links=5):
    article_links = []
    try:
        article_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/news/"]')  # Adjust selector as needed
        for elem in article_elements:
            link = elem.get_attribute('href')
            if link and '/news/' in link and link not in article_links:
                article_links.append(link)
            if len(article_links) >= max_links:
                break
    except NoSuchElementException:
        print("No articles found on topic page.")
    return article_links

# Function to scrape articles from BBC
def scrap_articles_bbc(names_list):
    article_data = []

    def search_and_scrape(name, news_site="BBC"):
        driver = initialize_driver()
        try:
            search_query = f"{news_site} {name}"
            search_url = f"https://www.google.com/search?q={search_query}"

            if not safe_get(driver, search_url):
                print(f"Failed to load search page for '{name}'.")
                return

            wait = WebDriverWait(driver, 60)  # Increased timeout to 60 seconds

            # Locate the results and find "bbc.com" link
            results = driver.find_elements(By.CSS_SELECTOR, "div.g")
            found_link = False
            for result in results:
                try:
                    cite_element = result.find_element(By.TAG_NAME, "cite")
                    if "bbc.com" in cite_element.text:
                        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                        print(f"Found BBC link for '{name}': {link}")
                        if safe_get(driver, link):
                            found_link = True
                            break
                except NoSuchElementException:
                    continue

            if not found_link:
                print(f"No BBC link found for '{name}' on {news_site}.")
                return

            # Check if the page is a topic page and extract article links if so
            if is_topic_page(driver.current_url):
                article_links = get_article_links_from_topic_page(driver, max_links=5)
                if not article_links:
                    print(f"No articles found on topic page for '{name}'.")
                    return

                for article_link in article_links:
                    if safe_get(driver, article_link):
                        time.sleep(random.uniform(2, 4))
                        try:
                            title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text
                        except TimeoutException:
                            title = 'NA'

                        paragraphs = driver.find_elements(By.CSS_SELECTOR, 'article p')
                        text = ' '.join([para.text for para in paragraphs if para.text])

                        article_data.append({
                            'Name': name,
                            'Website': news_site,
                            'Link': driver.current_url,
                            'Title': title,
                            'Text': text
                        })
            else:
                # Scrape the single article if not a topic page
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

    # Main function to process each name
    def process_names(names):
        max_threads = min(5, len(names))  # Adjust thread count based on the number of names
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(search_and_scrape, name) for name in names]
            for future in as_completed(futures):
                try:
                    future.result()  # Collect exceptions if any
                except Exception as e:
                    print(f"An error occurred: {e}")

    # Run the script
    process_names(names_list)

    # Return the collected article data in JSON format
    return json.dumps(article_data, ensure_ascii=False, indent=4)
