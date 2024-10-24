from fastapi import APIRouter, Depends
import traceback
from scripts.schemas.blog_post_schema import BlogPost
from typing import Union, Any
from scripts.constants.app_constants import APIEndpoints
from scripts.core.handlers.blog_post_handler import BlogPostHandler
from scripts.logging import logger
from scripts.schemas.response_models import (
    DefaultFailureResponse,
    DefaultSuccessResponse, DefaultResponse,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from scripts.utils.security_utils.project_decorator import MetaInfoCookie, MetaInfoSchema
from scripts.utils.security_utils.rbac import RBAC

get_cookies = MetaInfoCookie()
entity_name = "blog_post"
blog_post_router = APIRouter(prefix=APIEndpoints.proxy_api, tags=["App Related Services"])


# POST /api/posts - Create a new blog post
@blog_post_router.post(APIEndpoints.api_posts, dependencies=[Depends(RBAC(entity_name=entity_name, operation=["view", "create", "edit"]))])
async def create_post(post: BlogPost, meta: MetaInfoSchema = Depends(get_cookies)):
    """
    Create a new blog post.

    This endpoint creates a new blog post and saves it to the database.

    Args:
        post (BlogPost): The blog post object containing the post details.
        meta (MetaInfoSchema): User's metadata (automatically populated from cookies).

    Returns:
        JSONResponse: Success response if the blog post is created successfully, or
                      validation errors and failure response in case of exceptions.

    Raises:
        PydanticValidationError: If input validation fails for the blog post data.
        Exception: Logs and raises any other general exception.
    """
    try:
        BlogPostHandler().save_blog_post_details(post, meta.user_id)
        return DefaultSuccessResponse(status="success", message="Blog Created Successfully", data=None)
    except PydanticValidationError as validation_error:
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(validation_error.errors())},
        )
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception(tb)
        return DefaultFailureResponse(error=e.args, message=e.args)


# PUT /api/posts/{id} - Update an existing blog post
@blog_post_router.put(APIEndpoints.api_posts, dependencies=[Depends(RBAC(entity_name=entity_name, operation=["view", "create", "edit"]))])
async def update_post(post_id: str, updated_post: BlogPost):
    """
    Update an existing blog post.

    This endpoint updates an existing blog post based on the post ID.

    Args:
        post_id (str): The ID of the blog post to update.
        updated_post (BlogPost): The blog post object containing updated post details.

    Returns:
        JSONResponse: Success response if the blog post is updated successfully, or
                      validation errors and failure response in case of exceptions.

    Raises:
        PydanticValidationError: If input validation fails for the updated post data.
        Exception: Logs and raises any other general exception.
    """
    try:
        BlogPostHandler().save_blog_post_details(updated_post, post_id)
        return DefaultSuccessResponse(status="success", message="Blog Got Updated Successfully", data=None)
    except PydanticValidationError as validation_error:
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(validation_error.errors())},
        )
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception(tb)
        return DefaultFailureResponse(error=e.args, message=e.args)


# GET /api/posts/{id} - Retrieve details of a specific blog post
@blog_post_router.get(APIEndpoints.api_posts, dependencies=[Depends(RBAC(entity_name=entity_name, operation=["view"]))])
async def get_post(post_id: str):
    """
    Retrieve details of a specific blog post by its ID.

    This endpoint fetches and returns the details of the specified blog post.

    Args:
        post_id (str): The ID of the blog post to retrieve.

    Returns:
        JSONResponse: Success response with the blog post details, or failure response if the post is not found.

    Raises:
        PydanticValidationError: If input validation fails for the post ID.
        Exception: Logs and raises any other general exception.
    """
    try:
        response = BlogPostHandler().fetch_blog_post_details(post_id)
        if response:
            return DefaultSuccessResponse(status="success", message="Post Details", data=response)
        else:
            return DefaultResponse(status="Failed", message="Post not found", data=response)
    except PydanticValidationError as validation_error:
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(validation_error.errors())},
        )
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception(tb)
        return DefaultFailureResponse(error=e.args, message=e.args)


# GET /api/posts - Retrieve a list of blog posts
@blog_post_router.get(APIEndpoints.api_fetch_all_posts, dependencies=[Depends(RBAC(entity_name=entity_name, operation=["view"]))])
async def get_posts():
    """
    Retrieve a list of all blog posts.

    This endpoint fetches and returns a list of all non-deleted blog posts.

    Returns:
        JSONResponse: Success response with the list of blog posts, or failure response in case of exceptions.

    Raises:
        PydanticValidationError: If input validation fails.
        Exception: Logs and raises any other general exception.
    """
    try:
        response = BlogPostHandler().fetch_all_blog_posts()
        return DefaultSuccessResponse(status="success", message="success", data=response)
    except PydanticValidationError as validation_error:
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(validation_error.errors())},
        )
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception(tb)
        return DefaultFailureResponse(error=e.args, message=e.args)


# DELETE /api/posts/{id} - Delete a blog post
@blog_post_router.delete(APIEndpoints.api_posts, dependencies=[Depends(RBAC(entity_name=entity_name, operation=["view", "delete"]))])
async def delete_post(post_id: str):
    """
    Delete a blog post by its ID.

    This endpoint deletes the specified blog post from the database.

    Args:
        post_id (str): The ID of the blog post to delete.

    Returns:
        JSONResponse: Success response if the blog post is deleted, or failure response in case of exceptions.

    Raises:
        PydanticValidationError: If input validation fails for the post ID.
        Exception: Logs and raises any other general exception.
    """
    try:
        BlogPostHandler().delete_blog_post(post_id)
        return DefaultSuccessResponse(status="success", message="Post Deleted Successfully", data=None)
    except PydanticValidationError as validation_error:
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(validation_error.errors())},
        )
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception(tb)
        return DefaultFailureResponse(error=e.args, message=e.args)
