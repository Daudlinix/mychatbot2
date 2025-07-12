import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

base_url = "https://redstartravels.co"
visited = set()
headers = {"User-Agent": "Mozilla/5.0"}
data = ""

def is_valid(url):
    parsed = urlparse(url)
    return parsed.netloc == urlparse(base_url).netloc

def crawl(url):
    global data
    if url in visited:
        return
    visited.add(url)
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        data += f"\n\nPAGE: {url}\n{text}"

        # Crawl all internal links on the page
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if is_valid(full_url):
                crawl(full_url)

    except Exception as e:
        data += f"\n\nPAGE: {url}\nError: {str(e)}"

# Start crawling from home page
crawl(base_url)

# Save to file
with open("travel_data.txt", "w", encoding="utf-8") as f:
    f.write(data)

print("✅ Scraping complete.")
