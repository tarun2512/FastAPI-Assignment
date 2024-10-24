from fastapi import APIRouter

from scripts.services.blog_post_manager import blog_post_router

router = APIRouter()

router.include_router(blog_post_router)
