import asyncio
import pandas as pd
from urllib.parse import urlparse
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.allowed_domain = urlparse(seed_url).netloc.lower()
        self.data_frame = pd.DataFrame(columns=["url", "title", "text"])  # Initialize empty DataFrame

    async def crawl(self) -> None:
        crawler = PlaywrightCrawler()

        @crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            current_domain = urlparse(context.request.url).netloc.lower()

            # Skip processing if the current page is from an external domain
            if current_domain != self.allowed_domain and not current_domain.endswith(f".{self.allowed_domain}"):
                print(f"Skipping: {context.request.url} (outside allowed domain)")
                return

            # Extract the HTML content of the page
            page = context.page
            html_content = await page.content()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove script and style elements
            for script_or_style in soup(["script", "style"]):
                script_or_style.extract()  

            # Extract and clean visible text
            visible_text = ' '.join(soup.get_text(separator=' ', strip=True).split())

            # Collect data
            data = {
                "url": context.request.url,
                "title": await page.title(),
                "text": visible_text.replace(",", "")
            }

            # Append the data to the DataFrame
            self.data_frame = pd.concat([self.data_frame, pd.DataFrame([data])], ignore_index=True)

            # Log progress
            print(f"Processing: {context.request.url}")

            # Filter function to limit links to the allowed domain
            def filter_func(link):
                link_domain = urlparse(link.url).netloc.lower()
                if link_domain.startswith("www."):
                    link_domain = link_domain[4:]
                return link_domain == self.allowed_domain or link_domain.endswith(f".{self.allowed_domain}")

            # Enqueue links within the allowed domain
            await context.enqueue_links(filter_func=filter_func)

        # Start crawling from the initial seed URL
        await crawler.run([self.seed_url])

        # Save the data to a CSV file
        logfile = f"{urlparse(seed_url).netloc.lower()}.cvs"
        self.data_frame.to_csv(logfile, index=False)
        print(logfile)

# Usage example
if __name__ == "__main__":
    seed_url = "https://cnn.com/"
    crawler_instance = Crawler(seed_url)
    asyncio.run(crawler_instance.crawl())
