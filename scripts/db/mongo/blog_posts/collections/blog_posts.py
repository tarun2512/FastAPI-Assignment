from typing import Any, Dict, List, Optional


from scripts.constants.db_constants import DBConstants, DatabaseNames
from pydantic import BaseModel
from scripts.utils.mongo_util import MongoCollectionBaseClass


class BlogPostSchema(BaseModel):
    """
    This is the Schema for the Mongo DB Collection.
    All datastore and general responses will be following the schema.
    """
    post_id: Optional[int] = None  # ID will be assigned automatically
    title: str
    meta: Optional[dict] = {}
    content: Optional[str] = ""
    is_delete: bool = False


class BlogPostCollection(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(mongo_client, database=DatabaseNames.blog_posts, collection=DBConstants.collection_blog_posts)

    @property
    def key_post_id(self):
        return "post_id"

    def insert_one_post(self, data):
        """
        The following function will insert one tag in the
        tags collections
        :param self:
        :param data:
        :return:
        """
        return self.insert_one(data)

    def update_one_post(self, data, upsert=False, **query):
        """
        The following function will update one step in
        steps collection based on the given query
        :param data:
        :param upsert:
        :param query:
        :return:
        """
        return self.update_one(data=data, upsert=upsert, query=query)

    def delete_one_post(self, **query):
        """
        The following function will delete one tag in
        tags collection based on the given query
        :param query:
        :return:
        """
        return self.delete_one(query=query)

    def find_many(self, query):
        """
        The following function will give one process for a given set of
        search parameters as keyword arguments
        :return:
        """
        many_posts = self.find(query=query)
        if not many_posts:
            return []
        return list(many_posts)

    def find_by_id(self, post_id: str):
        query = {self.key_post_id: post_id}
        record = self.find_one(query)
        if not record:
            return BlogPostSchema(**{})
        return BlogPostSchema(**record)

    def fetch_post_details(self, post_id):
        query = {self.key_post_id: post_id}
        one_post = self.find_one(query=query)
        if not one_post:
            return BlogPostSchema(**{})
        return BlogPostSchema(**one_post)

    def fetch_post_details_by_title(self, title):
        query = {"title": title}
        one_post = self.find_one(query=query)
        if not one_post:
            return BlogPostSchema(**{})
        return BlogPostSchema(**one_post)
