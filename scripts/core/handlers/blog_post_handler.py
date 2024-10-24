from scripts.db.mongo import mongo_client
from scripts.db.mongo.blog_posts.collections.blog_posts import BlogPostCollection
from scripts.logging import logger
from scripts.schemas.blog_post_schema import BlogPost
from scripts.utils.common_utils import CommonUtils


class BlogPostHandler:
    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all of its attributes.


        :param self: Represent the instance of the class
        :param : Pass the mongo client to the class
        :return: The following:
        """
        self.blog_post_conn = BlogPostCollection(mongo_client)
        self.common_utils = CommonUtils()

    def get_post_id_and_meta(self, blog_details, user_id):
        """
        The get_post_id_and_meta function is used to get the post_id and meta-data for a given step.
            If the request_data does not contain a post_id, then it will generate one using the common test_utils function
            get next id. It will also create meta-data for this new step using the common test_utils function get user meta.
            If there is an existing step with that name, then it raises an error saying so.

        :param self: Represent the instance of a class
        :param blog_details: Get the project_id and post_id from the request
        :param user_id: Get the user_meta
        :return: A tuple of post_id and meta
        """
        if not blog_details.post_id:
            post_id = "post_" + self.common_utils.get_next_id("post_id")
            meta = self.common_utils.get_user_meta(user_id, check_flag=True)
        else:
            post_data = self.blog_post_conn.fetch_post_details_by_title(title=blog_details.title)
            post_data["meta"].update(self.common_utils.get_user_meta(user_id, check_flag=False))
            meta = post_data["meta"]
            post_id = blog_details.post_id
        return post_id, meta

    def save_blog_post_details(self, blog_details: BlogPost, user_id, post_id=None):
        """
        Save or update blog post details in the database.

        This function retrieves the post ID and metadata for the blog post, then
        saves the blog post to the database. If a post_id is provided, the post
        is updated; otherwise, a new post is created.

        Args:
            blog_details (BlogPost): The blog post object containing the details to be saved.
            user_id (str): The ID of the user who is creating or updating the blog post.
            post_id (Optional[str]): The ID of the blog post to update (default is None for new posts).

        Raises:
            Exception: Logs and raises any exception that occurs during the save process.
        """
        try:
            blog_details.post_id, blog_details.meta = self.get_post_id_and_meta(blog_details, user_id)
            self.blog_post_conn.update_one_post(data=blog_details.dict(), upsert=True, post_id=post_id)
        except Exception as e:
            logger.exception(f"exception occurred while saving the blog post {str(e)}")

    def fetch_blog_post_details(self, post_id):
        """
        Retrieve details of a specific blog post from the database.

        Args:
            post_id (str): The ID of the blog post to be retrieved.

        Returns:
            dict: The blog post details if found, otherwise None.

        Raises:
            Exception: Logs and raises any exception that occurs during the fetch process.
        """
        try:
            return self.blog_post_conn.find_one({"post_id": post_id})
        except Exception as e:
            logger.exception(f"exception occurred while fetching the blog details {str(e)}")

    def fetch_all_blog_posts(self):
        """
        Retrieve a list of all non-deleted blog posts from the database.

        Returns:
            list: A list of blog post documents where `is_deleted` is False.

        Raises:
            Exception: Logs and raises any exception that occurs during the fetch process.
        """
        try:
            return self.blog_post_conn.find_many({"is_deleted": False})
        except Exception as e:
            logger.exception(f"exception occurred while fetching the blog posts {str(e)}")

    def delete_blog_post(self, post_id):
        """
        Delete a specific blog post from the database.

        Args:
            post_id (str): The ID of the blog post to be deleted.

        Raises:
            Exception: Logs and raises any exception that occurs during the deletion process.
        """
        try:
            self.blog_post_conn.delete_one_post(post_id=post_id)
        except Exception as e:
            logger.exception(f"exception occurred while deleting the post {str(e)}")
