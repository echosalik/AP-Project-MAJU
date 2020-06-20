# Code Flow

## scrap.py
Run `scrap.py` it will scrap data from Steam's site. This process takes time as I had to add a sleep to avoid getting banned by the server. I ran it on a VPS, hence made it a `py` file instead of `ipnyb`.
This will create two json files. topplayed.json and topsellers.json.

## Plot.ipynb
This Notebook has all the graphs and panda's utilization. It shows thew following stats after loading data from JSON

- Top Played by Platform
- Top Selling by Platform
- Top Played Stats
- Top Selling Stats
- Top Played by Tags
- Top Selling by Tags
- Top Played by Price range
- Top Selling by Price range

Project Hosted at [Github](https://github.com/echosalik/AP-Project-MAJU)