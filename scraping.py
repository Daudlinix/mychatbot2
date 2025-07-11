from bs4 import BeautifulSoup
import requests

urls = [
    "https://redstartravels.co/services",
    "https://redstartravels.co/about",
    "https://redstartravels.co/contact",
    "https://redstartravels.co/packages"
]

headers = {"User-Agent": "Mozilla/5.0"}
data = ""

for url in urls:
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        data += f"\n\nPAGE: {url}\n{text}"
    except Exception as e:
        data += f"\n\nPAGE: {url}\nError: {str(e)}"

# Save data to file
with open("travel_data.txt", "w", encoding="utf-8") as f:
    f.write(data)
