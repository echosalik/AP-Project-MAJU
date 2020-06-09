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
with open("./topsellers.json", "w") as fp:
  while(items < total):
    print("Sending request for ", items, "items")
    data = requests.get("https://store.steampowered.com/contenthub/querypaginated/games/TopSellers/render/", {"query": "", "start": items, "count": 15, "cc": "PK", "l":"english", "v":"4", "tag": ""}).json()
    items += 15
    total = data["total_count"]
    print("Total items:", total)
    soup = BeautifulSoup(data["results_html"], 'html.parser')
    print("Looping anchors")
    for g in soup.find_all("a", recursive=False):
      game = dict()
      game["name"] = g.find("div", class_="tab_item_name").text
      game["platforms"] = [plat for x in g.find_all("span", class_="platform_img") for plat in x["class"] if plat != "platform_img"]
      t = set({x.text.replace(" ", "").replace(",", "").lower() for x in g.find_all("span", class_="top_tag")})
      tags.union(t)
      game["tags"] = list(t)
      platforms.union(set(game["platforms"]))
      discount = g.find("div", class_="discount_pct")
      game["discount"] = float(discount.text.replace("-", "").replace("%", "")) if discount != None  else 0
      price_raw = g.find("div", class_="discount_final_price")
      if price_raw == None:
        game["price"] = 0
        game["original_price"] = 0
      elif "free" in price_raw.text.lower():
        game["price"] = 0
        game["original_price"] = 0
      elif game["discount"] == 0:
        price_raw = g.find("div", class_="discount_final_price").text
        game["price"] = float(price_raw.replace("$", ""))
        game["original_price"] = game["price"]
      else:
        price_raw = g.find("div", class_="discount_final_price").text
        game["price"] = float(price_raw.replace("$", ""))
        game["original_price"] = float(g.find("div", class_="discount_original_price").text.replace("$", ""))
      print("adding game to list")
      games.append(game)
    print("Entering Sleep to avoid getting banned by server")
    time.sleep(10)
  print("Dumping JSON")
  json.dump({"games": games, "tags": list(tags), "platforms": list(platforms)}, fp)