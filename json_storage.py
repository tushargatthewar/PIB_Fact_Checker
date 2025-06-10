import requests
from bs4 import BeautifulSoup
import json

# URL of the PIB RSS feed
url = "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"

# Fetch the RSS feed
response = requests.get(url)
response.raise_for_status()  

# Parse the XML data
soup = BeautifulSoup(response.content, 'xml')

# Extract all items
items = soup.find_all('item')

# Create JSON structure
press_releases = []
for item in items:
    press_releases.append({
        "title": item.title.text.strip(),
        "link": item.link.text.strip(),
        "pubDate": item.pubDate.text.strip() if item.pubDate else None,
        "description": item.description.text.strip() if item.description else None
    })

# Create final JSON object
json_output = {
    "channel": {
        "title": soup.channel.title.text.strip(),
        "description": soup.channel.description.text.strip(),
        "copyright": soup.channel.copyright.text.strip() if soup.channel.copyright else None,
        "lastBuildDate": soup.channel.lastBuildDate.text.strip() if soup.channel.lastBuildDate else None
    },
    "press_releases": press_releases
}

# Convert to JSON string
json_data = json.dumps(json_output, indent=2, ensure_ascii=False)

# Save to file
with open('pib_rss_feed.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print("Data successfully saved to pib_rss_feed.json")