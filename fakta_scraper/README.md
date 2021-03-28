# Fakta scraper <a name="fakta-scraper"></a>
The Fakta scraper can scrape discounts from this week discounts. <br/>
**OBS: Fakta scraper can not run in Linux as it uses the Firefox webdriver which is a .exe file.**

## Scrape discounts <a name="scrape-discounts"></a>
For now you can only search for keywords and get the discounts that match the keywords.
To scrape for discounts about for example Kellogg products, you only have to add the keyword "Kellogg" as a argument when running the fakta_scraper.py script:
```
python3 fakta_scraper.py kellogg
```

You can search for multiple keyword by just adding them as arguments, as such:
```
python fakta_scraper.py <keyword_1> <keyword_2> <keyword_3>
```

The discounts is printed in the terminal.
