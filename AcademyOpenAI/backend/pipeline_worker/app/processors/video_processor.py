"""Video processor for handling video content and generating interactive courses."""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from ..services.llm_service import LLMService
from ..services.ffmpeg_service import FFmpegService

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Processor for video content to generate interactive courses."""
    
    def __init__(self, llm_service: Optional[LLMService] = None, ffmpeg_service: Optional[FFmpegService] = None):
        """Initialize the video processor.
        
        Args:
            llm_service: LLM service for course generation
            ffmpeg_service: FFmpeg service for video processing
        """
        self.llm_service = llm_service or LLMService()
        self.ffmpeg_service = ffmpeg_service or FFmpegService()
    
    async def process_video(self, video_path: str, course_id: str, target_language: str = "ru") -> Dict[str, Any]:
        """Process a video file to generate an interactive course.
        
        This implementation uses Option A from the technical documentation:
        Direct Generation with Gemini 2.5 Pro (multimodal approach).
        
        Args:
            video_path: Path to the video file
            course_id: ID of the course being created
            target_language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing the generated course data
        """
        logger.info(f"Processing video for course {course_id}: {video_path}")
        
        # Validate video file
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Optional: Preprocess video if needed (e.g., format conversion, compression)
        # processed_video_path = await self.ffmpeg_service.preprocess_video(video_path)
        
        try:
            # Generate course directly from video using Gemini 2.5 Pro
            course_data = await self.llm_service.generate_course_from_video(
                video_path=video_path,
                language=target_language
            )
            
            logger.info(f"Successfully generated course data for {course_id}")
            return course_data
            
        except Exception as e:
            logger.error(f"Failed to process video for course {course_id}: {e}")
            raise
    
    async def process_video_option_b(self, video_path: str, course_id: str, target_language: str = "ru") -> Dict[str, Any]:
        """Process a video file to generate an interactive course using multi-step approach.
        
        This implementation uses Option B from the technical documentation:
        Multi-Step Processing with separate STT, Translation, and Course Generation.
        
        Note: This is a placeholder for the alternative approach and would require
        additional services (STT, Translation) to be implemented.
        
        Args:
            video_path: Path to the video file
            course_id: ID of the course being created
            target_language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing the generated course data
        """
        logger.info(f"Processing video (multi-step) for course {course_id}: {video_path}")
        
        # TODO: Implement Option B with the following steps:
        # 1. Extract audio from video using FFmpegService
        # 2. Transcribe audio to text using STTService
        # 3. Translate text using TranslationService
        # 4. Generate course structure using LLMService.generate_course_from_text()
        
        raise NotImplementedError("Option B (multi-step processing) is not yet implemented")