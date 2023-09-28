import requests
import pymongo
from bs4 import BeautifulSoup
from decouple import config


# Replace these values with your MongoDB connection details
mongo_uri = config('MONGO_URI')
database_name = config('DATABASE_NAME')


# Initialize a connection to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[database_name]

# URL to scrape
BASE_URL = "http://books.toscrape.com"

