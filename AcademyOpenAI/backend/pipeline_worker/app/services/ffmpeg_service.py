"""FFmpeg service for video and audio processing."""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class FFmpegService:
    """Service for video and audio processing using FFmpeg."""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """Initialize the FFmpeg service.
        
        Args:
            ffmpeg_path: Path to FFmpeg executable. If None, will use 'ffmpeg' from PATH.
        """
        self.ffmpeg_path = ffmpeg_path or 'ffmpeg'
        self._validate_ffmpeg()
    
    def _validate_ffmpeg(self):
        """Validate that FFmpeg is available and executable."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, '-version'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            logger.debug(f"FFmpeg version: {result.stdout.splitlines()[0] if result.stdout else 'Unknown'}")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"FFmpeg validation failed: {e}")
            raise RuntimeError(f"FFmpeg not found or not executable at {self.ffmpeg_path}")
    
    async def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """Extract audio from a video file.
        
        Args:
            video_path: Path to the video file
            output_path: Path for the output audio file. If None, will use video filename with .mp3 extension.
            
        Returns:
            Path to the extracted audio file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if output_path is None:
            video_file = Path(video_path)
            output_path = str(video_file.with_suffix('.mp3'))
        
        logger.info(f"Extracting audio from {video_path} to {output_path}")
        
        try:
            # Run FFmpeg to extract audio
            subprocess.run(
                [
                    self.ffmpeg_path,
                    '-i', video_path,
                    '-q:a', '0',  # High quality
                    '-map', 'a',   # Extract audio only
                    '-y',          # Overwrite output file if exists
                    output_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            logger.info(f"Audio extraction completed: {output_path}")
            return output_path
            
        except subprocess.SubprocessError as e:
            logger.error(f"Audio extraction failed: {e}")
            raise RuntimeError(f"Failed to extract audio from {video_path}: {e}")
    
    async def preprocess_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        """Preprocess video for optimal processing (resize, compress, etc.).
        
        Args:
            video_path: Path to the video file
            output_path: Path for the processed video file. If None, will use video filename with _processed suffix.
            
        Returns:
            Path to the processed video file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if output_path is None:
            video_file = Path(video_path)
            output_path = str(video_file.with_stem(f"{video_file.stem}_processed"))
        
        logger.info(f"Preprocessing video {video_path} to {output_path}")
        
        try:
            # Run FFmpeg to preprocess video (example: resize to 720p and compress)
            subprocess.run(
                [
                    self.ffmpeg_path,
                    '-i', video_path,
                    '-vf', 'scale=-1:720',  # Resize to 720p height, maintain aspect ratio
                    '-c:v', 'libx264',      # H.264 codec
                    '-crf', '23',           # Compression quality (lower = better quality, higher file size)
                    '-preset', 'medium',     # Encoding speed/compression tradeoff
                    '-c:a', 'aac',          # AAC audio codec
                    '-b:a', '128k',         # Audio bitrate
                    '-y',                    # Overwrite output file if exists
                    output_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            logger.info(f"Video preprocessing completed: {output_path}")
            return output_path
            
        except subprocess.SubprocessError as e:
            logger.error(f"Video preprocessing failed: {e}")
            raise RuntimeError(f"Failed to preprocess video {video_path}: {e}")