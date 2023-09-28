import requests
import pymongo
from decouple import config


# Replace these values with your MongoDB connection details
mongo_uri = config('MONGO_URI')
database_name = config('DATABASE_NAME')

# Replace with your actual app ID
app_id = config('APP_ID')

# API URLs
users_api_url = "https://dummyapi.io/data/v1/user"
user_posts_api_url = "https://dummyapi.io/data/v1/user/{user_id}/post"

def main():
    # Establish a connection to MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db = client[database_name]

    # Headers for API requests
    headers = {
        "app-id": app_id
    }

    # Fetch users data from the API
    response = requests.get(users_api_url, headers=headers)
    users_data = response.json()

    # Store users data in the 'users' collection
    users_collection = db['users']
    users_collection.insert_many(users_data['data'])

    print("Users data has been successfully fetched and stored in MongoDB.")

    # Fetch users from the database
    users = users_collection.find()

    # Iterate through each user and fetch their posts
    for user in users:
        user_id = user['id']
        user_posts_url = user_posts_api_url.replace("{user_id}", user_id)

        # Fetch user's posts data from the API
        response = requests.get(user_posts_url, headers=headers)
        user_posts_data = response.json()

        # Store user's posts data in the 'posts' collection
        posts_collection = db['posts']
        posts_collection.insert_many(user_posts_data['data'])

    print("Users' posts data has been successfully fetched and stored in MongoDB.")

if __name__ == "__main__":
    main()
