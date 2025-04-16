import requests
from bs4 import BeautifulSoup

url = "https://www.grocerybabu.com"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

sub_cat_links = []
for li in soup.select("ul.menu > li"):
    for sub_li in li.select("ul.submenu > li"):
        a_tag = sub_li.select_one("a")
        if a_tag and a_tag.text != "ALL":
            sub_cat_links.append(a_tag.get("href"))

print(sub_cat_links)