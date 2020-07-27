# venmo_scrape
Tools written in python to scrape public venmo data. venmo_scrape.py defines an augmented Client class from a python library used to interact with: https://github.com/mmohades/Venmo

An updated version of the above library handles an additional semi-common transaction type, useful when scraping a lot of transaction data.

The venmo_scrape_client class includes functions for taking the data and adding them to panda's dataframes.

my_scrape.py can be used to automatically scrape data. It will ask for input, start with a venmo username or just a name. 

The analysis ipython notebook walks through an example analysis. It uses a little natural language processing to categorize transactions and the networkx library: https://networkx.github.io/ to 
rank similar users. 
