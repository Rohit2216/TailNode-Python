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


# Function to scrape and store book data
def scrape_and_store_books(page_num):
    page_url = f"{BASE_URL}/catalogue/page-{page_num}.html"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("h3")
    prices = soup.select(".price_color")
    availabilities = soup.select(".availability")
    ratings = soup.select(".star-rating")

    for i in range(len(books)):
        title = books[i].find("a")["title"]
        price = prices[i].get_text()
        availability = availabilities[i].get_text().strip()
        rating = ratings[i]["class"][1]

        book_data = {
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating
        }

        # Store book data in the 'books' collection
        books_collection = db['books']
        books_collection.insert_one(book_data)

# Loop through all 50 pages and scrape books data
for page_num in range(1, 51):
    scrape_and_store_books(page_num)

print("Books data has been successfully scraped and stored in MongoDB.")

# Close the MongoDB client connection
client.close()