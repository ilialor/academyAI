"""LLM Service for interacting with Google's Gemini 2.5 Pro API."""

import os
from typing import Dict, Any, Optional, List

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class LLMService:
    """Service for interacting with Google's Gemini 2.5 Pro API for course generation."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM service with API key.
        
        Args:
            api_key: Google AI API key. If None, will try to get from environment variable.
        """
        self.api_key = api_key or os.environ.get("GOOGLE_AI_API_KEY")
        if not self.api_key:
            raise ValueError("Google AI API key is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-pro",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
    
    async def generate_course_from_video(self, video_path: str, language: str = "ru") -> Dict[str, Any]:
        """Generate a structured course directly from video using Gemini 2.5 Pro's multimodal capabilities.
        
        Args:
            video_path: Path to the video file
            language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing structured course data
        """
        # Read video file as bytes
        with open(video_path, "rb") as f:
            video_data = f.read()
        
        # Construct prompt for Gemini
        prompt = f"""Analyze the provided English video lecture. Generate a structured interactive course in {language} based on its content. The course should include:
        - Logical modules/sections with titles.
        - Key takeaways/summaries for each module.
        - Identification and definition of key technical terms (English and {language}).
        - 3-5 multiple-choice questions (MCQs) per module with correct answers indicated.
        - 1-2 open-ended questions for self-reflection per module.
        
        Return the result as a structured JSON object with the following format:
        {{"title": "Course Title",
         "description": "Course Description",
         "modules": [
            {{"title": "Module Title",
              "summary": "Module summary text",
              "keywords": [{{"term": "Term in English", "translation": "Term in {language}", "definition": "Definition in {language}"}}],
              "mcqs": [{{"question": "Question text", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_index": 0}}],
              "reflection_questions": ["Question 1", "Question 2"]
            }}
          ]
        }}
        """
        
        # Call Gemini API with video data and prompt
        response = await self.model.generate_content_async(
            contents=[{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "video/mp4", "data": video_data}}]}]
        )
        
        # Parse and return the structured course data
        try:
            course_data = response.text
            # TODO: Add proper JSON parsing and validation
            return course_data
        except Exception as e:
            raise Exception(f"Failed to parse course data from Gemini response: {e}")
    
    async def generate_course_from_text(self, text_content: str, language: str = "ru") -> Dict[str, Any]:
        """Generate a structured course from text content using Gemini 2.5 Pro.
        
        Args:
            text_content: English text content to process
            language: Target language for the course (default: Russian)
            
        Returns:
            Dict containing structured course data
        """
        # Construct prompt for Gemini
        prompt = f"""Analyze the provided English text content. Generate a structured interactive course in {language} based on its content. The course should include:
        - Logical modules/sections with titles.
        - Key takeaways/summaries for each module.
        - Identification and definition of key technical terms (English and {language}).
        - 3-5 multiple-choice questions (MCQs) per module with correct answers indicated.
        - 1-2 open-ended questions for self-reflection per module.
        
        Here is the text content to analyze:
        
        {text_content}
        
        Return the result as a structured JSON object with the following format:
        {{"title": "Course Title",
         "description": "Course Description",
         "modules": [
            {{"title": "Module Title",
              "summary": "Module summary text",
              "keywords": [{{"term": "Term in English", "translation": "Term in {language}", "definition": "Definition in {language}"}}],
              "mcqs": [{{"question": "Question text", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_index": 0}}],
              "reflection_questions": ["Question 1", "Question 2"]
            }}
          ]
        }}
        """
        
        # Call Gemini API with text prompt
        response = await self.model.generate_content_async(prompt)
        
        # Parse and return the structured course data
        try:
            course_data = response.text
            # TODO: Add proper JSON parsing and validation
            return course_data
        except Exception as e:
            raise Exception(f"Failed to parse course data from Gemini response: {e}")