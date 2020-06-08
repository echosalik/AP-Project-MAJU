import requests
import json
from bs4 import BeautifulSoup
import time

items = 0
total = 1

games = []
tags = set()
platforms = set()

# Free to play games
with open("./games.json", "w") as fp:
  while(items < total):
    data = requests.get("https://store.steampowered.com/contenthub/querypaginated/games/TopSellers/render/", {"query": "", "start": items, "count": 15, "cc": "PK", "l":"english", "v":"4", "tag": ""}).json()
    # data = requests.get("https://store.steampowered.com/contenthub/querypaginated/freetoplay/TopSellers/render/", {"query": "", "start": items, "count": 15, "cc": "PK", "l":"english", "v":"4", "tag": ""}).json()
    items += 15
    total = data["total_count"]
    soup = BeautifulSoup(data["results_html"], 'html.parser')
    for g in soup.find_all("a", recursive=False):
      game = dict()
      game["name"] = g.find("div", class_="tab_item_name").text
      game["platforms"] = [plat for x in g.find_all("span", class_="platform_img") for plat in x["class"] if plat != "platform_img"]
      game["tags"] = set({x.text.replace(" ", "").replace(",", "").lower() for x in g.find_all("span", class_="top_tag")})
      tags.union(game["tags"])
      platforms.union(set(game["platforms"]))
      try:
        price_raw = g.find("div", class_="discount_final_price").text
        price = price_raw if "free" not in price_raw.lower() else "$0"
        game["price"] = float(price[1:])
      except:
        print(items / 15)
        game["price"] = 0.0
      games.append(game)
    time.sleep(5)
  json.dump({"games": games, "tags": tags}, fp)