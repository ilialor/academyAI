"""Task definitions for the pipeline worker service."""

from celery import Celery
from app.core.config import settings
from .process_content import ContentProcessingTasks  # Import existing task handlers
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

# Configure Celery
celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.tasks'] # Point to this module to find tasks
)

# Optional Celery configuration (timeouts, retries, etc.)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # task_soft_time_limit=600, # Example: 10 minutes soft limit
    # task_time_limit=720,      # Example: 12 minutes hard limit
)

# Instantiate the content tasks handler
content_tasks = ContentProcessingTasks()

# --- Celery Tasks (wrappers around the async functions) --- 

@celery_app.task(name="process_video_task", bind=True)
def process_video_task(self, course_id: str, video_path: str, target_language: str = "ru"):
    """Celery task to process an uploaded video file."""
    logger.info(f"[TASK_VIDEO] Received task for course {course_id}, Task ID: {self.request.id}")
    
    try:
        # ContentProcessingTasks has async methods, so we need to run them in an event loop
        result = asyncio.run(content_tasks.process_video_task(
            course_id=course_id,
            video_path=video_path,
            target_language=target_language
        ))
        
        logger.info(f"[TASK_VIDEO] Task completed for course {course_id}")
        return result
    except Exception as e:
        logger.exception(f"[TASK_VIDEO] Task failed for course {course_id}: {e}")
        # Re-raise to let Celery handle the failure
        raise

@celery_app.task(name="process_text_task", bind=True)
def process_text_task(self, course_id: str, text_content: str, target_language: str = "ru"):
    """Celery task to process uploaded text content."""
    logger.info(f"[TASK_TEXT] Received task for course {course_id}, Task ID: {self.request.id}")
    
    try:
        # ContentProcessingTasks has async methods, so we need to run them in an event loop
        result = asyncio.run(content_tasks.process_text_task(
            course_id=course_id,
            text_content=text_content,
            target_language=target_language
        ))
        
        logger.info(f"[TASK_TEXT] Task completed for course {course_id}")
        return result
    except Exception as e:
        logger.exception(f"[TASK_TEXT] Task failed for course {course_id}: {e}")
        raise 