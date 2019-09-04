# scraping_project

This project scrapes company registrar data from the North Dakota Secretary of State website using Scrapy and Pandas and visualizes the data using networkx and matplotlib.


Usage Guide:

1. Clone this repo to your local machine.

2. Start up a virtual environment and pip install the requirements.txt file.

3. CD into the scraping_project/north_dakota/north_dakota/spiders directory and run nd_spider.py from the commandline. This should run the scraper and save all the scraped data as a csv file.

4. Run network_viz.py from the commandline to generate a network graph of the data.
