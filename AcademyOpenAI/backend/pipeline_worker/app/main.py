"""Main entry point for the pipeline worker service."""

import os
import logging
import asyncio
from typing import Dict, Any
from app.tasks import celery_app
from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import task handlers
from .tasks.process_content import ContentProcessingTasks

# This file is primarily used to run the Celery worker process.
# The tasks themselves are defined in app.tasks.py.

print(f"Starting Celery worker for {settings.APP_NAME}...")
print(f"Broker URL: {settings.CELERY_BROKER_URL}")
print(f"Result Backend: {settings.CELERY_RESULT_BACKEND}")

# Create local storage path if it doesn't exist and storage type is local
if settings.STORAGE_TYPE == "local":
    os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)
    print(f"Ensured local storage directory exists: {settings.LOCAL_STORAGE_PATH}")

# This would be replaced with proper message queue consumer in production
class MockMessageQueueConsumer:
    """Mock message queue consumer for development/testing."""
    
    def __init__(self):
        self.content_tasks = ContentProcessingTasks()
    
    async def start(self):
        """Start consuming messages from the queue."""
        logger.info("Starting mock message queue consumer")
        
        # In a real implementation, this would connect to RabbitMQ/Redis
        # and consume messages from the queue
        
        # For demonstration, we'll just log that we're ready
        logger.info("Mock consumer ready to process tasks")
        
        # Keep the service running
        while True:
            await asyncio.sleep(60)
    
    async def process_message(self, message: Dict[str, Any]):
        """Process a message from the queue.
        
        Args:
            message: Message data from the queue
        """
        logger.info(f"Processing message: {message}")
        
        try:
            task_type = message.get("task_type")
            
            if task_type == "process_video":
                result = await self.content_tasks.process_video_task(
                    course_id=message.get("course_id"),
                    video_path=message.get("video_path"),
                    target_language=message.get("target_language", "ru")
                )
                logger.info(f"Video processing completed for course {message.get('course_id')}")
                
            elif task_type == "process_text":
                result = await self.content_tasks.process_text_task(
                    course_id=message.get("course_id"),
                    text_content=message.get("text_content"),
                    target_language=message.get("target_language", "ru")
                )
                logger.info(f"Text processing completed for course {message.get('course_id')}")
                
            else:
                logger.error(f"Unknown task type: {task_type}")
                return
            
            # In a real implementation, we would update the course status in the database
            # and potentially publish a completion message to another queue
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # In a real implementation, we would update the course status to ERROR
            # and potentially retry the task or notify an admin

# In a real implementation, this would be replaced with FastStream/Celery worker
async def main():
    """Main entry point for the pipeline worker service."""
    try:
        consumer = MockMessageQueueConsumer()
        await consumer.start()
    except Exception as e:
        logger.error(f"Pipeline worker service failed: {e}")

# Entry point for running the service
if __name__ == "__main__":
    # This block is mainly for informational purposes or potential direct script execution,
    # but usually, you run Celery via its command-line interface.
    print("To run the worker, use the command:")
    print("  celery -A app.main.celery_app worker --loglevel=info -P gevent") # Added -P gevent for potential async tasks
    # The worker needs to be started externally.
    pass