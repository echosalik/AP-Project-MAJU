# Made By Salik Sadruddin Merani
# SP20-MSCS-0052
# https://github.com/echosalik/AP-Project-MAJU

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import matplotlib.pyplot as plt
import numpy as np

## Initializing Required Variables
items = 0
# Set this to 1 to get all the data from the API
total = 1000

top_sellers = []
top_played = []
platforms = ['win', 'mac', 'linux']
sleep_time = 3

tags = set()

## Reading API for Top Seller Games
while(items < total):
  print("Sending request for ", items, "items")
  data = requests.get("https://store.steampowered.com/contenthub/querypaginated/games/TopSellers/render/", {"query": "", "start": items, "count": 15, "cc": "PK", "l":"english", "v":"4", "tag": ""}).json()
  items += 15
  if(total == 1):
    total = data["total_count"]
  print("Total items:", total)
  soup = BeautifulSoup(data["results_html"], 'html.parser')
  print("Looping anchors")
  for g in soup.find_all("a", recursive=False):
    game = dict()
    game["name"] = g.find("div", class_="tab_item_name").text
    game["platforms"] = [plat for x in g.find_all("span", class_="platform_img") for plat in x["class"] if plat != "platform_img"]
    t = set({x.text.replace(" ", "").replace(",", "").lower() for x in g.find_all("span", class_="top_tag")})
    game["tags"] = list(t)
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
    top_sellers.append(game)
  print("Entering Sleep to avoid getting banned by server")
  time.sleep(sleep_time)

## Reading API for Top Played Games
items = 0
while(items < total):
  print("Sending request for ", items, "items")
  data = requests.get("https://store.steampowered.com/contenthub/querypaginated/games/ConcurrentUsers/render/", {"query": "", "start": items, "count": 15, "cc": "PK", "l":"english", "v":"4", "tag": ""}).json()
  items += 15
  if(total == 1):
    total = data["total_count"]
  print("Total items:", total)
  soup = BeautifulSoup(data["results_html"], 'html.parser')
  print("Looping anchors")
  for g in soup.find_all("a", recursive=False):
    game = dict()
    game["name"] = g.find("div", class_="tab_item_name").text
    game["platforms"] = [plat for x in g.find_all("span", class_="platform_img") for plat in x["class"] if plat != "platform_img"]
    t = set({x.text.replace(" ", "").replace(",", "").lower() for x in g.find_all("span", class_="top_tag")})
    game["tags"] = list(t)
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
    top_played.append(game)
  print("Entering Sleep to avoid getting banned by server")
  time.sleep(sleep_time)

## Initializing Dataframes
games_ts = pd.DataFrame(top_sellers)
games_tp = pd.DataFrame(top_played)

platform_ts = platforms
if(games_ts['platforms'].map(len).max() > len(platform_ts)):
  diff = games_ts['platforms'].map(len).max() - len(platform_ts)
  for i in range(0, diff):
    platform_ts.append("col"+i)

platform_tp = platforms
if(games_tp['platforms'].map(len).max() > len(platform_tp)):
  diff = games_tp['platforms'].map(len).max() - len(platform_tp)
  for i in range(0, diff):
    platform_tp.append("col"+i)

## All tags in Game list
for tg in games_ts["tags"]:
  tags = tags.union(set(tg))

for tg in games_tp["tags"]:
  tags = tags.union(set(tg))

# Start of Copied Code from stackoverflow - coz shashke
def autolabel(rects, ax):
  """Attach a text label above each bar in *rects*, displaying its height."""
  for rect in rects:
    height = rect.get_height()
    ax.annotate('{}'.format(height),
      xy=(rect.get_x() + rect.get_width() / 2, height),
      xytext=(0, 3),  # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')
# End of Copied Code

## Top played games by plaform
tp_by_platforms = pd.DataFrame(games_tp['platforms'].to_list(), columns=platform_tp)
tp_by_platforms['win'] = np.where(tp_by_platforms['win'] == "win", 1, 0)
tp_by_platforms['mac'] = np.where(tp_by_platforms['mac'] == "mac", 1, 0)
tp_by_platforms['linux'] = np.where(tp_by_platforms['linux'] == "linux", 1, 0)
tp_by_platforms_sum = tp_by_platforms.sum().to_list()
fig1, ax1 = plt.subplots()
ax1.set_title("Top Played Games by Platform")
autolabel(ax1.bar(platforms, tp_by_platforms_sum), ax1)
# plt.show()

## Top selling games by plaform
ts_by_platforms = pd.DataFrame(games_ts['platforms'].to_list(), columns=platform_ts)
ts_by_platforms['win'] = np.where(ts_by_platforms['win'] == "win", 1, 0)
ts_by_platforms['mac'] = np.where(ts_by_platforms['mac'] == "mac", 1, 0)
ts_by_platforms['linux'] = np.where(ts_by_platforms['linux'] == "linux", 1, 0)
ts_by_platforms_sum = ts_by_platforms.sum().to_list()
fig0, ax0 = plt.subplots()
ax0.set_title("Top Selling Games by Platform")
autolabel(ax0.bar(platforms, ts_by_platforms_sum), ax0)
# plt.show()

## Top Played games stats
tp_free = games_tp[ games_tp['price'] == 0 ]
print("Top Play Free Games", tp_free['name'].count(), "out of", games_tp['name'].count())
tp_disc = games_tp[ games_tp['discount'] != 0 ]
print("Top Play Discounted Games", tp_disc['name'].count(), "out of", games_tp['name'].count())
tp_maxd = games_tp[games_tp['discount'] == games_tp['discount'].max()]
print("Top Play Max Discount", tp_maxd['discount'].item(), "% on", tp_maxd['name'].item())

## Top Selling games stats
ts_free = games_ts[ games_ts['price'] == 0 ]
print("Top Selling Free Games", ts_free['name'].count(), "out of", games_ts['name'].count())
ts_disc = games_ts[ games_ts['discount'] != 0 ]
print("Top Selling Discounted Games", ts_disc['name'].count(), "out of", games_ts['name'].count())
non_zero = games_ts[games_ts['original_price'] != 0]
ts_maxd = non_zero[non_zero['discount'] == non_zero['discount'].max()]
print("Top Selling Max Discount", ts_maxd['discount'].item(), "% on", ts_maxd['name'].item())

## Top Played games by tags
tp = {};
for tag in list(tags):
    tp[tag] = pd.Series([1 if tag in t else 0 for t in games_tp.tags])
tags_ds = pd.DataFrame(tp)
top20_bytags = tags_ds.sum().sort_values(ascending=False)[0:20]
fig2, ax2 = plt.subplots()
ax2.set_title("Top Played Games by tags")
ax2.pie(top20_bytags, labels=top20_bytags.index, autopct='%1.1f%%')
# plt.show()

## Top Selling games by tags
ts = {};
for tag in list(tags):
    ts[tag] = pd.Series([1 if tag in t else 0 for t in games_ts.tags])
tags_ds = pd.DataFrame(ts)
top20_bytags = tags_ds.sum().sort_values(ascending=False)[0:20]
fig3, ax3 = plt.subplots()
ax3.set_title("Top Selling Games by tags")
ax3.pie(top20_bytags, labels=top20_bytags.index, autopct='%1.1f%%')
# plt.show()

## Top Played games by Price range
tp_pr = {}
tp_pr['USD 0 - 10'] = games_tp[(games_tp['price'] >= 0) & (games_tp['price'] < 10)]['name'].count()
tp_pr['USD 10 - 30'] = games_tp[(games_tp['price'] >= 10) & (games_tp['price'] < 30)]['name'].count()
tp_pr['USD 30 - 50'] = games_tp[(games_tp['price'] >= 30) & (games_tp['price'] < 50)]['name'].count()
tp_pr['USD 50 - 70'] = games_tp[(games_tp['price'] >= 50) & (games_tp['price'] < 70)]['name'].count()
tp_pr['USD 70 +'] = games_tp[(games_tp['price'] >= 70)]['name'].count()
fig4, ax4 = plt.subplots()
ax4.set_title("Top Played games by Price range")
autolabel(ax4.bar(tp_pr.keys(), tp_pr.values()), ax4)
# plt.show()

## Top Selling games by Price range
tp_pr = {}
tp_pr['USD 0 - 10'] = games_ts[(games_ts['price'] >= 0) & (games_ts['price'] < 10)]['name'].count()
tp_pr['USD 10 - 30'] = games_ts[(games_ts['price'] >= 10) & (games_ts['price'] < 30)]['name'].count()
tp_pr['USD 30 - 50'] = games_ts[(games_ts['price'] >= 30) & (games_ts['price'] < 50)]['name'].count()
tp_pr['USD 50 - 70'] = games_ts[(games_ts['price'] >= 50) & (games_ts['price'] < 70)]['name'].count()
tp_pr['USD 70 +'] = games_ts[(games_ts['price'] >= 70)]['name'].count()
fig4, ax4 = plt.subplots()
ax4.set_title("Top Selling games by Price range")
autolabel(ax4.bar(tp_pr.keys(), tp_pr.values()), ax4)

# Show all plots
plt.show()