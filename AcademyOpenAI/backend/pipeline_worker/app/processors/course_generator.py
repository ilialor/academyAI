"""Course generator for structuring and formatting course data."""

import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class CourseGenerator:
    """Generator for structuring and formatting course data."""
    
    def __init__(self):
        """Initialize the course generator."""
        pass
    
    async def format_course_data(self, raw_course_data: str) -> Dict[str, Any]:
        """Format and validate raw course data from LLM.
        
        Args:
            raw_course_data: Raw course data from LLM (typically JSON string)
            
        Returns:
            Dict containing properly formatted course data
        """
        logger.info("Formatting and validating course data")
        
        try:
            # Parse JSON data
            if isinstance(raw_course_data, str):
                course_data = json.loads(raw_course_data)
            else:
                course_data = raw_course_data
                
            # Validate required fields
            self._validate_course_structure(course_data)
            
            # Format and clean data if needed
            formatted_data = self._clean_course_data(course_data)
            
            logger.info("Course data successfully formatted and validated")
            return formatted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse course data as JSON: {e}")
            raise ValueError(f"Invalid course data format: {e}")
        except Exception as e:
            logger.error(f"Error formatting course data: {e}")
            raise
    
    def _validate_course_structure(self, course_data: Dict[str, Any]) -> None:
        """Validate the structure of course data.
        
        Args:
            course_data: Course data to validate
            
        Raises:
            ValueError: If course data structure is invalid
        """
        # Check required top-level fields
        required_fields = ["title", "description", "modules"]
        for field in required_fields:
            if field not in course_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check modules structure
        if not isinstance(course_data["modules"], list) or not course_data["modules"]:
            raise ValueError("Modules must be a non-empty list")
        
        # Check each module structure
        for i, module in enumerate(course_data["modules"]):
            module_required_fields = ["title", "summary", "keywords", "mcqs", "reflection_questions"]
            for field in module_required_fields:
                if field not in module:
                    raise ValueError(f"Module {i+1} missing required field: {field}")
            
            # Check keywords structure
            if not isinstance(module["keywords"], list):
                raise ValueError(f"Module {i+1}: keywords must be a list")
            
            # Check MCQs structure
            if not isinstance(module["mcqs"], list):
                raise ValueError(f"Module {i+1}: mcqs must be a list")
            
            for j, mcq in enumerate(module["mcqs"]):
                mcq_required_fields = ["question", "options", "correct_index"]
                for field in mcq_required_fields:
                    if field not in mcq:
                        raise ValueError(f"Module {i+1}, MCQ {j+1} missing required field: {field}")
    
    def _clean_course_data(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and format course data.
        
        Args:
            course_data: Course data to clean
            
        Returns:
            Cleaned course data
        """
        # Create a deep copy to avoid modifying the original
        cleaned_data = course_data.copy()
        
        # Clean title and description
        cleaned_data["title"] = cleaned_data["title"].strip()
        cleaned_data["description"] = cleaned_data["description"].strip()
        
        # Clean modules
        for module in cleaned_data["modules"]:
            module["title"] = module["title"].strip()
            module["summary"] = module["summary"].strip()
            
            # Clean keywords
            for keyword in module["keywords"]:
                if "term" in keyword:
                    keyword["term"] = keyword["term"].strip()
                if "translation" in keyword:
                    keyword["translation"] = keyword["translation"].strip()
                if "definition" in keyword:
                    keyword["definition"] = keyword["definition"].strip()
            
            # Clean MCQs
            for mcq in module["mcqs"]:
                mcq["question"] = mcq["question"].strip()
                mcq["options"] = [option.strip() for option in mcq["options"]]
                
                # Ensure correct_index is an integer
                if isinstance(mcq["correct_index"], str):
                    try:
                        mcq["correct_index"] = int(mcq["correct_index"])
                    except ValueError:
                        # If conversion fails, find the correct answer by other means
                        # (e.g., if it's marked with an asterisk or "correct" label)
                        pass
            
            # Clean reflection questions
            module["reflection_questions"] = [q.strip() for q in module["reflection_questions"]]
        
        return cleaned_data
    
    async def enrich_course_data(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich course data with additional information (optional).
        
        This could include adding metadata, generating additional content,
        or enhancing existing content.
        
        Args:
            course_data: Course data to enrich
            
        Returns:
            Enriched course data
        """
        # TODO: Implement course data enrichment if needed
        # This could include:
        # - Adding difficulty levels
        # - Generating additional resources/references
        # - Adding estimated completion time
        # - Adding tags/categories
        
        return course_data