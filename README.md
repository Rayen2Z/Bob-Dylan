# Bob Dylan
 A deep dive into Bob Dylan's lyrics

## Songs' selection:
The list of songs was scrapped from [Bob Dylan's fandom page](https://bobdylan.fandom.com/wiki/List_of_Bob_Dylan_songs). It includes all the songs performed by, performed on, or written by Bob Dylan. This list is only music officially released. The Best Hits' albums, Live performances and The Bootleg series have been excluded. 

For scrapping, a simple web scraping tool was used : [Web Scraper](https://www.webscraper.io/).

## Lyrics retrieving:
To retrieve the lyrics for each song, the Genuis API was used. Check the get_data.py file.
The results were preprocessed to keep only the lyrics and get rid of the trailing whitespaces and newline characters.