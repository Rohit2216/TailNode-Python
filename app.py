
from decouple import config  
import requests  
import pymysql  
import json  
from datetime import datetime 

# Retrieve environment variables for MySQL connection

host = config('MYSQL_HOST')  # MySQL server address
user = config('MYSQL_USER')  # MySQL username
password = config('MYSQL_PASSWORD')  # MySQL password
database = config('MYSQL_DATABASE')  # MySQL database name

# Retrieve API key for making requests
app_id = config('APP_ID')  # API key for authentication

# API endpoints
users_api_url = 'https://dummyapi.io/data/v1/user'
user_posts_api_url = 'https://dummyapi.io/data/v1/user/{user_id}/post'

# Connect to MySQL database
connection = pymysql.connect(host=host, user=user, password=password, database=database)

# Function to fetch and save posts data
def fetch_and_save_posts(user_id):
    # Define API endpoint for fetching posts data for a specific user
    api_url = user_posts_api_url.format(user_id=user_id)
    response = requests.get(api_url, headers={'app-id': app_id})
    posts_data = response.json()

    # Loop through each post data
    with connection.cursor() as cursor:
        for post in posts_data['data']:
            # Convert tags to JSON string
            tags_json = json.dumps(post['tags'])
            # Convert date string to datetime format
            publish_date = datetime.strptime(post['publishDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # Define SQL query for inserting post data
            sql = "INSERT INTO posts (id, image, likes, tags, text, publishDate, owner) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (post['id'], post['image'], post['likes'], tags_json, post['text'], publish_date, user_id))

# Fetch users data from the API
response = requests.get(users_api_url, headers={'app-id': app_id})
users_data = response.json()

# Insert users data into the 'users' table
with connection.cursor() as cursor:
    for user in users_data['data']:
        sql = "INSERT INTO users (id, title, firstname, lastname, picture) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user['id'], user['title'], user['firstName'], user['lastName'], user['picture']))

# Retrieve user IDs from the database
with connection.cursor() as cursor:
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

# Fetch and save posts for each user
for user_id in user_ids:
    fetch_and_save_posts(user_id)

# Commit and close connection
connection.commit()
connection.close()

print("Users and posts data inserted into the database.")
