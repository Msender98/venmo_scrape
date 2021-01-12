# Analyzing Social Networks Using Public Venmo Data
This repository holds tools written in python to scrape public venmo data. Thy can be use to download, map and analyze venmo user's behavior and networks. 

## Example:
The analysis ipython notebook above walks through an example analysis. It uses a little natural language processing to categorize transactions and the networkx library: https://networkx.github.io/ to rank similar users. 

## Results:
See my blog post using these tools: https://nycdatascience.com/blog/student-works/using-venmo-to-map-social-networks/
In short I was able to download over 100k transactions stemming from my account (transactions 3 steps from my account) and rank my closest friends (using a personalized pagerank algorithm from networkx). By combining this analysis with information about users insight can be drawn about the behavior of different consumers. In the above blog post an example of this is used to show the overlap in social networks between consumers who use Uber and Lyft. 

## Code:
my_scrape.py can be used to automatically scrape data. It will ask for input, start with a venmo username or just a name and pull transactions after a year a given distance from the initial users.

venmo_scrape.py defines an augmented Client class from a python library used to interact with venmo: https://github.com/mmohades/Venmo. The class includes functions for downloading the data and converting them to digestible dataframes. 


