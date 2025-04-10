"""Text processor for handling text content and generating interactive courses."""

import logging
from typing import Dict, Any, Optional

from ..services.llm_service import LLMService

logger = logging.getLogger(__name__)

class TextProcessor:
    """Processor for text content to generate interactive courses."""
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """Initialize the text processor.
        
        Args:
            llm_service: LLM service for course generation
        """
        self.llm_service = llm_service or LLMService()
    
    async def process_text(self, text_content: str, course_id: str, target_language: str = "ru") -> Dict[str, Any]:
        """Process text content to generate an interactive course.
        
        Args:
            text_content: Text content to process
            course_id: ID of the course being created
            target_language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing the generated course data
        """
        logger.info(f"Processing text for course {course_id}")
        
        # Validate text content
        if not text_content or not text_content.strip():
            raise ValueError("Text content cannot be empty")
        
        try:
            # Generate course from text using Gemini 2.5 Pro
            course_data = await self.llm_service.generate_course_from_text(
                text_content=text_content,
                language=target_language
            )
            
            logger.info(f"Successfully generated course data for {course_id}")
            return course_data
            
        except Exception as e:
            logger.error(f"Failed to process text for course {course_id}: {e}")
            raise