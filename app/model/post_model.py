from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('DATABASE_URL'), int(os.getenv('DATABASE_PORT')))

db = client.kenzie


class Post():
    current_date_time = datetime.now().strftime('%d/%m/%Y %H:%M')
    length_collection = db.posts.count()


    def __init__(self, title: str, author: str, tags: str, content: str):
        self.title = title
        self.author = author
        self. tags = tags
        self.content = content
        self.created_at = self.current_date_time
        self.updated_at = self.current_date_time
        self._id = db.posts.count() + 1

    def save(self) -> dict:
        db.posts.insert_one(self.__dict__)
        return self.__dict__

    @staticmethod
    def show_all_posts() -> list:
        posts = list(db.posts.find())

        return posts

    @staticmethod
    def get_post_by_id(id: int) -> list:

        data = {'_id': id}

        post = db.posts.find_one(data)

        return post

    @classmethod
    def update_post(cls, id: int, new_data: dict) -> list:
        new_data['updated_at'] = cls.current_date_time
        update = {"$set": new_data}

        db.posts.update_one({"_id": id}, update)

        return list(db.posts.find({"_id": id}))

    @staticmethod
    def delete_post(id: int) -> dict:
        data = db.posts.find_one({'_id': id})

        db.posts.delete_one(data)
        return data

    def list_id() -> list:
        data = list(db.posts.find())
        item = [item['_id'] for item in data]

        return item
