import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

def download_pdf(url, directory="."):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all anchor tags (<a>) that have href attribute ending with '.pdf'
        pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

        # Download PDF files
        for link in pdf_links:
            pdf_url = urljoin(url, link['href'])
            filename = os.path.join(directory, os.path.basename(pdf_url))
            with open(filename, 'wb') as f:
                f.write(requests.get(pdf_url).content)
            print(f"Downloaded: {filename}")
    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

def save_webpage_content(url, directory="."):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the title of the page
        title = soup.title.string.strip() if soup.title else "Untitled"

        # Generate a unique filename using the page title and current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(directory, f"{title}_{timestamp}_webpage_content.txt")

        # Save webpage content without HTML tags
        with open(filename, 'w', encoding='utf-8') as f:
            # Remove blank lines
            f.write('\n'.join(line for line in soup.get_text().splitlines() if line.strip()))
        print(f"Saved webpage content: {filename}")
    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

def scrape_website(url, directory="."):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Dictionary to keep track of visited URLs
    visited_urls = {}

    # Helper function to recursively scrape URLs
    def scrape_url_recursive(url):
        # Check if URL has been visited before
        if url in visited_urls:
            return
        visited_urls[url] = True

        # Save webpage content without HTML tags
        save_webpage_content(url, directory)

        # Download PDF files
        download_pdf(url, directory)

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all anchor tags (<a>) and recursively scrape their URLs
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                # Check if the URL belongs to the same domain
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    scrape_url_recursive(next_url)

    # Start recursive scraping
    scrape_url_recursive(url)


url = 'https://www.tsb.co.uk/'
scrape_website(url)
