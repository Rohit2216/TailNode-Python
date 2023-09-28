import requests
import mysql.connector
from bs4 import BeautifulSoup
from decouple import config

# Replace these values with your MySQL connection details
mysql_host = config('MYSQL_HOST')
mysql_user = config('MYSQL_USER')
mysql_password = config('MYSQL_PASSWORD')
mysql_database = config('MYSQL_DATABASE')

# Initialize a connection to MySQL
connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

cursor = connection.cursor()

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

        # Define the SQL INSERT statement
        insert_query = """
        INSERT INTO books (title, price, availability, rating)
        VALUES (%s, %s, %s, %s)
        """

        # Execute the INSERT statement
        book_data = (title, price, availability, rating)
        cursor.execute(insert_query, book_data)

        # Commit the changes
        connection.commit()

# Loop through all 50 pages and scrape books data
for page_num in range(1, 51):
    scrape_and_store_books(page_num)

print("Books data has been successfully scraped and stored in MySQL.")

# Close the MySQL connection
cursor.close()
connection.close()
