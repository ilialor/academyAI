"""Task handlers for processing content and generating courses."""

import logging
from typing import Dict, Any, Optional

from ..processors.video_processor import VideoProcessor
from ..processors.text_processor import TextProcessor
from ..processors.course_generator import CourseGenerator

logger = logging.getLogger(__name__)

class ContentProcessingTasks:
    """Task handlers for processing content and generating courses."""
    
    def __init__(self):
        """Initialize content processing tasks."""
        self.video_processor = VideoProcessor()
        self.text_processor = TextProcessor()
        self.course_generator = CourseGenerator()
    
    async def process_video_task(self, course_id: str, video_path: str, target_language: str = "ru") -> Dict[str, Any]:
        """Process a video to generate an interactive course.
        
        Args:
            course_id: ID of the course being created
            video_path: Path to the video file
            target_language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing the processed course data
        """
        logger.info(f"Starting video processing task for course {course_id}")
        
        try:
            # Process video to get raw course data
            raw_course_data = await self.video_processor.process_video(
                video_path=video_path,
                course_id=course_id,
                target_language=target_language
            )
            
            # Format and validate course data
            formatted_course_data = await self.course_generator.format_course_data(raw_course_data)
            
            # Optional: Enrich course data with additional information
            enriched_course_data = await self.course_generator.enrich_course_data(formatted_course_data)
            
            logger.info(f"Video processing task completed for course {course_id}")
            return enriched_course_data
            
        except Exception as e:
            logger.error(f"Video processing task failed for course {course_id}: {e}")
            raise
    
    async def process_text_task(self, course_id: str, text_content: str, target_language: str = "ru") -> Dict[str, Any]:
        """Process text content to generate an interactive course.
        
        Args:
            course_id: ID of the course being created
            text_content: Text content to process
            target_language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing the processed course data
        """
        logger.info(f"Starting text processing task for course {course_id}")
        
        try:
            # Process text to get raw course data
            raw_course_data = await self.text_processor.process_text(
                text_content=text_content,
                course_id=course_id,
                target_language=target_language
            )
            
            # Format and validate course data
            formatted_course_data = await self.course_generator.format_course_data(raw_course_data)
            
            # Optional: Enrich course data with additional information
            enriched_course_data = await self.course_generator.enrich_course_data(formatted_course_data)
            
            logger.info(f"Text processing task completed for course {course_id}")
            return enriched_course_data
            
        except Exception as e:
            logger.error(f"Text processing task failed for course {course_id}: {e}")
            raise