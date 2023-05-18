import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    # Step 2: Send a GET request to the URL
    response = requests.get(url)

    # Step 3: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 4: Find the specific elements with itemprop attributes
    headline_element = soup.find("h1", itemprop="headline")
    description_element = soup.find("h2", itemprop="description")
    content_element = soup.find("div", id="pcl-full-content")

    # Step 5: Extract the text content from the elements
    headline = headline_element.get_text().strip() if headline_element else "Headline not found"
    description = description_element.get_text().strip() if description_element else "Description not found"
    content = content_element.get_text().strip() if content_element else "Content not found"

    # Step 6: Return the extracted headline, description, and content
    return (headline+description+content)

# scrape_article("https://indianexpress.com/article/india/manipur-looted-weapons-pose-big-security-concern-talks-with-kukis-in-jeopardy-8615364/")