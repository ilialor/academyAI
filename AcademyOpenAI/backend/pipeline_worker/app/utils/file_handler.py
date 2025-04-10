"""File handling utilities for the pipeline worker service."""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, Union, BinaryIO

from ..core.config import settings

logger = logging.getLogger(__name__)

class FileHandler:
    """Utility class for handling files in the pipeline worker service."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """Initialize the file handler.
        
        Args:
            storage_path: Path to the storage directory. If None, will use the configured path.
        """
        self.storage_path = storage_path or settings.LOCAL_STORAGE_PATH
        self._ensure_storage_path_exists()
    
    def _ensure_storage_path_exists(self):
        """Ensure the storage path exists."""
        os.makedirs(self.storage_path, exist_ok=True)
        logger.debug(f"Storage path ensured: {self.storage_path}")
    
    def get_temp_directory(self, course_id: str) -> str:
        """Get a temporary directory for a specific course.
        
        Args:
            course_id: ID of the course
            
        Returns:
            Path to the temporary directory
        """
        temp_dir = os.path.join(self.storage_path, "temp", course_id)
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir
    
    def save_uploaded_file(self, file_data: Union[bytes, BinaryIO], filename: str, course_id: str) -> str:
        """Save an uploaded file to the storage.
        
        Args:
            file_data: File data as bytes or file-like object
            filename: Name of the file
            course_id: ID of the course
            
        Returns:
            Path to the saved file
        """
        temp_dir = self.get_temp_directory(course_id)
        file_path = os.path.join(temp_dir, filename)
        
        logger.info(f"Saving uploaded file to {file_path}")
        
        try:
            if isinstance(file_data, bytes):
                with open(file_path, "wb") as f:
                    f.write(file_data)
            else:
                # Assume file-like object
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(file_data, f)
            
            logger.info(f"File saved successfully: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise
    
    def cleanup_temp_files(self, course_id: str):
        """Clean up temporary files for a specific course.
        
        Args:
            course_id: ID of the course
        """
        temp_dir = os.path.join(self.storage_path, "temp", course_id)
        
        if os.path.exists(temp_dir):
            logger.info(f"Cleaning up temporary files for course {course_id}")
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Temporary files cleaned up for course {course_id}")
            except Exception as e:
                logger.error(f"Failed to clean up temporary files: {e}")
    
    def move_to_permanent_storage(self, temp_file_path: str, course_id: str, file_type: str) -> str:
        """Move a file from temporary storage to permanent storage.
        
        Args:
            temp_file_path: Path to the temporary file
            course_id: ID of the course
            file_type: Type of the file (e.g., 'video', 'audio', 'transcript')
            
        Returns:
            Path to the file in permanent storage
        """
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"Temporary file not found: {temp_file_path}")
        
        # Create permanent storage directory
        perm_dir = os.path.join(self.storage_path, "courses", course_id, file_type)
        os.makedirs(perm_dir, exist_ok=True)
        
        # Get filename from path
        filename = os.path.basename(temp_file_path)
        perm_file_path = os.path.join(perm_dir, filename)
        
        logger.info(f"Moving file to permanent storage: {perm_file_path}")
        
        try:
            shutil.copy2(temp_file_path, perm_file_path)
            logger.info(f"File moved to permanent storage: {perm_file_path}")
            return perm_file_path
            
        except Exception as e:
            logger.error(f"Failed to move file to permanent storage: {e}")
            raise