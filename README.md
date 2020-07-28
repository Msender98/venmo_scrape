# venmo_scrape
Tools written in python to scrape public venmo data. venmo_scrape.py defines an augmented Client class from a python library used to interact with venmo: https://github.com/mmohades/Venmo. The class includes functions for taking the data and adding them to panda's dataframes.

my_scrape.py can be used to automatically scrape data. It will ask for input, start with a venmo username or just a name and pull transactions after a year a given distance from the initial users. Note it is not efficient right now, needs to be improved to handle larger numbers of users and transactions (works well with tens of thousands for now) 

The analysis ipython notebook walks through an example analysis. It uses a little natural language processing to categorize transactions and the networkx library: https://networkx.github.io/ to rank similar users. 
