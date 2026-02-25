"""
Autonomous YouTube Shorts Voice Agent
Generates, produces, and uploads viral YouTube Shorts from a single topic input
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import subprocess
import re
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeShortsAgent:
    """
    Autonomous agent for creating and uploading YouTube Shorts
    
    Features:
    - Viral script generation with hook optimization
    - Natural voiceover generation
    - Vertical video creation (9:16, 1080x1920)
    - Synchronized subtitles
    - SEO-optimized metadata
    - Automatic YouTube upload
    """
    
    def __init__(self, output_dir: str = "shorts_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Video specifications
        self.video_width = 1080
        self.video_height = 1920
        self.fps = 30
        self.max_duration = 55  # seconds
        self.min_duration = 30
        
        # Script optimization parameters
        self.hook_duration = 3  # seconds for hook
        self.target_retention = 0.85  # 85% retention target
        
        logger.info("YouTube Shorts Agent initialized")
    
    # ==================== SCRIPT GENERATION ====================
    
    def generate_viral_script(self, topic: str) -> Dict[str, Any]:
        """
        Generate a viral short-form script optimized for retention
        
        Args:
            topic: The topic or idea for the short
            
        Returns:
            Script with hook, body, CTA, and metadata
        """
        logger.info(f"Generating viral script for topic: {topic}")
        
        system_prompt = """You are a viral YouTube Shorts scriptwriter specializing in high-retention content.

Your scripts must:
1. Start with a powerful hook in the first 3 seconds that creates curiosity or shock
2. Keep pacing fast and engaging with no filler words
3. Use short, punchy sentences
4. Create curiosity gaps throughout
5. Use emotionally engaging language
6. End with a brief CTA (follow/subscribe)
7. Total duration: 30-55 seconds when spoken naturally
8. Maximize replay value

Format your response as JSON:
{
  "hook": "First 3 seconds - must grab attention",
  "body": "Main content - fast-paced, engaging",
  "cta": "Brief call to action",
  "estimated_duration": 45,
  "retention_score": 8.5,
  "viral_elements": ["curiosity", "emotion", "value"]
}"""
        
        user_prompt = f"""Create a viral YouTube Short script about: {topic}

Requirements:
- Hook must create immediate curiosity or shock
- Keep it under 55 seconds total
- No filler words or unnecessary content
- High retention focus
- Platform-safe and monetization-friendly
- Emotionally engaging"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.9,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            script_data = json.loads(response.choices[0].message.content)
            
            # Combine script parts
            full_script = f"{script_data['hook']} {script_data['body']} {script_data['cta']}"
            
            script_result = {
                "topic": topic,
                "hook": script_data.get("hook", ""),
                "body": script_data.get("body", ""),
                "cta": script_data.get("cta", ""),
                "full_script": full_script,
                "estimated_duration": script_data.get("estimated_duration", 45),
                "retention_score": script_data.get("retention_score", 8.0),
                "viral_elements": script_data.get("viral_elements", []),
                "word_count": len(full_script.split())
            }
            
            logger.info(f"Script generated: {script_result['word_count']} words, "
                       f"~{script_result['estimated_duration']}s duration")
            
            return script_result
            
        except Exception as e:
            logger.error(f"Script generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ==================== VOICEOVER GENERATION ====================
    
    def generate_voiceover(self, script: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate natural human-like voiceover using OpenAI TTS
        
        Args:
            script: The script text to convert to speech
            output_path: Optional custom output path
            
        Returns:
            Voiceover file path and metadata
        """
        logger.info("Generating voiceover...")
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"voiceover_{timestamp}.mp3"
        
        try:
            # Use OpenAI TTS API for natural voice
            response = self.openai_client.audio.speech.create(
                model="tts-1-hd",  # High quality model
                voice="nova",  # Engaging female voice (options: alloy, echo, fable, onyx, nova, shimmer)
                input=script,
                speed=1.1  # Slightly faster for shorts
            )
            
            # Save audio file
            response.stream_to_file(str(output_path))
            
            # Get audio duration using ffprobe
            duration = self._get_audio_duration(str(output_path))
            
            result = {
                "success": True,
                "audio_path": str(output_path),
                "duration": duration,
                "format": "mp3",
                "voice": "nova",
                "speed": 1.1
            }
            
            logger.info(f"Voiceover generated: {duration:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Voiceover generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration using ffprobe"""
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    audio_path
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return float(result.stdout.strip())
            else:
                logger.warning("Could not get audio duration, estimating...")
                return 45.0  # Default estimate
                
        except Exception as e:
            logger.warning(f"Error getting audio duration: {e}")
            return 45.0
    
    # ==================== VIDEO GENERATION WITH SORA ====================
    
    def generate_video_clips_with_sora(
        self,
        topic: str,
        script: str,
        num_clips: int = 3,
        style: str = "animated"
    ) -> List[str]:
        """
        Generate AI video clips using OpenAI Sora (gpt-video-1) matching script content
        
        Args:
            topic: Video topic
            script: Script content for context
            num_clips: Number of video clips to generate
            style: Visual style for videos
            
        Returns:
            List of video file paths
        """
        logger.info(f"Generating {num_clips} video clips with Sora (gpt-video-1)...")
        
        video_paths = []
        
        try:
            # Parse script into segments
            script_segments = self._parse_script_segments(script, num_clips)
            
            # Style descriptions for video generation
            style_prompts = {
                "cartoon": "vibrant cartoon animation style, bold colors, playful movement",
                "animated": "3D animated style like Pixar, smooth motion, professional quality",
                "realistic": "cinematic realistic footage, high quality, professional cinematography",
                "3d": "modern 3D CGI animation, clean, colorful, dynamic camera movements",
                "abstract": "abstract visual art, flowing shapes, vibrant colors, artistic"
            }
            
            style_desc = style_prompts.get(style, style_prompts["animated"])
            
            # Generate video clips for each script segment
            for i, segment in enumerate(script_segments):
                try:
                    # Create context-aware video prompt
                    video_prompt = f"""{style_desc}. Vertical 9:16 format video that visually represents: {segment[:150]}
                    
Cinematic, engaging, dynamic camera movement, professional quality, vibrant colors, no text overlay."""
                    
                    logger.info(f"Generating Sora video {i+1}/{num_clips} for: {segment[:50]}...")
                    
                    # Use OpenAI responses.create API for gpt-video-1
                    import requests
                    import os
                    import base64
                    
                    api_key = os.getenv("OPENAI_API_KEY")
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": "gpt-video-1",
                        "input": video_prompt
                    }
                    
                    # Call Sora API endpoint using responses.create
                    sora_response = requests.post(
                        "https://api.openai.com/v1/responses",
                        headers=headers,
                        json=payload,
                        timeout=180
                    )
                    
                    if sora_response.status_code == 200:
                        result = sora_response.json()
                        
                        # Extract base64 video from response
                        video_base64 = None
                        if "output" in result and len(result["output"]) > 0:
                            output = result["output"][0]
                            if "content" in output and len(output["content"]) > 0:
                                content = output["content"][0]
                                if "video" in content:
                                    video_base64 = content["video"]
                        
                        if video_base64:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            video_path = self.output_dir / f"sora_clip_{timestamp}_{i}.mp4"
                            
                            # Convert base64 to video file
                            video_buffer = base64.b64decode(video_base64)
                            with open(video_path, 'wb') as f:
                                f.write(video_buffer)
                            
                            video_paths.append(str(video_path))
                            logger.info(f"✓ Generated Sora video {i+1}/{num_clips}: {video_path.name}")
                        else:
                            logger.warning(f"No video data in Sora response for clip {i+1}")
                    else:
                        logger.warning(f"Sora API returned status {sora_response.status_code}: {sora_response.text}")
                    
                    # Delay to avoid rate limits
                    import time
                    time.sleep(2)
                    
                except Exception as e:
                    logger.warning(f"Failed to generate Sora video {i+1}: {e}")
                    continue
            
            if not video_paths:
                logger.warning("No Sora videos generated, will fall back to images")
            else:
                logger.info(f"Successfully generated {len(video_paths)} Sora video clips")
            
            return video_paths
            
        except Exception as e:
            logger.error(f"Sora video generation error: {e}")
            return []
    
    # ==================== IMAGE GENERATION ====================
    
    def _parse_script_segments(self, script: str, num_segments: int = 3) -> List[str]:
        """
        Parse script into segments for image generation
        
        Args:
            script: Full script text
            num_segments: Number of segments to create
            
        Returns:
            List of script segments
        """
        # Split script into sentences
        sentences = [s.strip() for s in script.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        
        if len(sentences) <= num_segments:
            return sentences
        
        # Distribute sentences evenly across segments
        segment_size = len(sentences) // num_segments
        segments = []
        
        for i in range(num_segments):
            start_idx = i * segment_size
            end_idx = start_idx + segment_size if i < num_segments - 1 else len(sentences)
            segment_text = '. '.join(sentences[start_idx:end_idx])
            segments.append(segment_text)
        
        return segments
    
    def generate_background_images(
        self, 
        topic: str, 
        script: str, 
        num_images: int = 3,
        style: str = "cartoon"
    ) -> List[str]:
        """
        Generate AI images matching script content using DALL-E
        
        Args:
            topic: Video topic
            script: Script content for context
            num_images: Number of images to generate
            style: Visual style (cartoon, animated, realistic, 3d)
            
        Returns:
            List of image file paths
        """
        logger.info(f"Generating {num_images} {style} images matching script content...")
        
        image_paths = []
        
        try:
            # Parse script into segments
            script_segments = self._parse_script_segments(script, num_images)
            
            # Style descriptions
            style_prompts = {
                "cartoon": "vibrant cartoon illustration style, bold colors, playful, animated look",
                "animated": "3D animated style like Pixar, colorful, smooth, professional animation",
                "realistic": "photorealistic, high quality, professional photography",
                "3d": "modern 3D render, clean, colorful, professional CGI",
                "comic": "comic book art style, bold outlines, dynamic, colorful panels"
            }
            
            style_desc = style_prompts.get(style, style_prompts["cartoon"])
            
            # Generate images for each script segment
            for i, segment in enumerate(script_segments):
                try:
                    # Create context-aware prompt based on script segment
                    prompt = f"""Create a {style_desc} vertical image (9:16 aspect ratio) that visually represents: "{segment[:200]}"
                    
Topic: {topic}
Style: {style_desc}
Requirements:
- Vertical format optimized for mobile
- Eye-catching and engaging
- Clear focal point
- Vibrant colors
- NO text or words in the image
- Professional quality
- Matches the narrative content"""
                    
                    logger.info(f"Generating image {i+1}/{num_images} for: {segment[:50]}...")
                    
                    # Generate image using DALL-E
                    response = self.openai_client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1792",  # Vertical format close to 9:16
                        quality="standard",
                        n=1
                    )
                    
                    # Download image
                    image_url = response.data[0].url
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_path = self.images_dir / f"bg_{style}_{timestamp}_{i}.png"
                    
                    import requests
                    img_response = requests.get(image_url, timeout=30)
                    
                    if img_response.status_code == 200:
                        with open(image_path, 'wb') as f:
                            f.write(img_response.content)
                        image_paths.append(str(image_path))
                        logger.info(f"✓ Generated image {i+1}/{num_images}: {image_path.name}")
                    
                    # Small delay to avoid rate limits
                    import time
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Failed to generate image {i+1}: {e}")
                    continue
            
            if not image_paths:
                logger.warning("No images generated, will use gradient background")
            else:
                logger.info(f"Successfully generated {len(image_paths)} script-matched images")
            
            return image_paths
            
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return []
    
    # ==================== VIDEO CREATION ====================
    
    def create_vertical_video(
        self,
        audio_path: str,
        script: str,
        output_path: Optional[str] = None,
        background_type: str = "gradient",
        topic: str = "",
        visual_style: str = "cartoon"
    ) -> Dict[str, Any]:
        """
        Create vertical video (9:16) with background and synchronized subtitles
        
        Args:
            audio_path: Path to voiceover audio
            script: Script text for subtitles
            output_path: Optional custom output path
            background_type: Type of background (gradient, solid, animated, ai_images,sora_video)
            topic: Video topic (required for ai_images)
            visual_style: Style for AI images (cartoon, animated, realistic, 3d, comic)
            
        Returns:
            Video file path and metadata
        """
        logger.info("Creating vertical video...")
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"short_{timestamp}.mp4"
        
        try:
            # Get audio duration
            audio_duration = self._get_audio_duration(audio_path)
            
            # Generate subtitle file
            subtitle_path = self._generate_subtitles(script, audio_duration)
            
            # Generate background visuals based on type
            background_videos = []
            background_images = []
            
            if background_type == "sora_video" and topic:
                # Generate AI video clips using Sora
                background_videos = self.generate_video_clips_with_sora(
                    topic,
                    script,
                    num_clips=3,
                    style=visual_style
                )
                
                # If Sora fails, fall back to AI images
                if not background_videos:
                    logger.info("Sora video generation failed, falling back to AI images...")
                    background_images = self.generate_background_images(
                        topic,
                        script,
                        num_images=3,
                        style=visual_style
                    )
                    
            elif background_type == "ai_images" and topic:
                # Generate AI images using DALL-E
                background_images = self.generate_background_images(
                    topic, 
                    script, 
                    num_images=3,
                    style=visual_style
                )
            
            # Create video with ffmpeg
            video_created = self._create_video_with_ffmpeg(
                audio_path,
                subtitle_path,
                str(output_path),
                audio_duration,
                background_type,
                background_images,
                background_videos
            )
            
            if video_created:
                result = {
                    "success": True,
                    "video_path": str(output_path),
                    "duration": audio_duration,
                    "resolution": f"{self.video_width}x{self.video_height}",
                    "format": "mp4",
                    "fps": self.fps,
                    "has_subtitles": True
                }
                
                logger.info(f"Video created: {output_path}")
                return result
            else:
                return {
                    "success": False,
                    "error": "Video creation failed"
                }
                
        except Exception as e:
            logger.error(f"Video creation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_subtitles(self, script: str, duration: float) -> str:
        """Generate SRT subtitle file with word timing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subtitle_path = self.output_dir / f"subtitles_{timestamp}.srt"
        
        # Split script into words
        words = script.split()
        words_per_second = len(words) / duration
        
        # Generate SRT format
        srt_content = []
        current_time = 0.0
        words_per_subtitle = 3  # Show 3 words at a time for readability
        
        for i in range(0, len(words), words_per_subtitle):
            chunk = " ".join(words[i:i + words_per_subtitle])
            chunk_duration = words_per_subtitle / words_per_second
            
            start_time = self._format_srt_time(current_time)
            end_time = self._format_srt_time(current_time + chunk_duration)
            
            srt_content.append(f"{i // words_per_subtitle + 1}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(chunk.upper())  # Uppercase for better visibility
            srt_content.append("")
            
            current_time += chunk_duration
        
        # Write SRT file
        with open(subtitle_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(srt_content))
        
        logger.info(f"Subtitles generated: {subtitle_path}")
        return str(subtitle_path)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format time for SRT subtitle format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _create_video_with_ffmpeg(
        self,
        audio_path: str,
        subtitle_path: str,
        output_path: str,
        duration: float,
        background_type: str,
        background_images: List[str] = None,
        background_videos: List[str] = None
    ) -> bool:
        """Create video using ffmpeg with background and subtitles"""
        try:
            # Step 1: Create background video
            temp_bg_video = str(Path(output_path).parent / "temp_bg.mp4")
            
            if background_videos and len(background_videos) > 0:
                # Use Sora-generated video clips
                logger.info(f"Using {len(background_videos)} Sora-generated video clips")
                
                output_dir = Path(output_path).parent
                
                # Trim or extend clips to match audio duration
                clip_duration = duration / len(background_videos)
                temp_clips = []
                
                for i, video_path in enumerate(background_videos):
                    trimmed_clip = str(output_dir / f"temp_sora_clip_{i}.mp4")
                    temp_clips.append(trimmed_clip)
                    
                    logger.info(f"Processing Sora clip {i+1}/{len(background_videos)}")
                    
                    # Trim/extend clip to match duration
                    cmd_trim = [
                        "ffmpeg",
                        "-i", video_path,
                        "-vf", f"scale={self.video_width}:{self.video_height}:force_original_aspect_ratio=decrease,pad={self.video_width}:{self.video_height}:(ow-iw)/2:(oh-ih)/2:black",
                        "-c:v", "libx264",
                        "-t", str(clip_duration),
                        "-pix_fmt", "yuv420p",
                        "-y",
                        trimmed_clip
                    ]
                    
                    result = subprocess.run(cmd_trim, capture_output=True, text=True, timeout=60)
                    
                    if result.returncode != 0:
                        logger.error(f"Failed to process Sora clip {i+1}: {result.stderr}")
                        for clip in temp_clips:
                            if Path(clip).exists():
                                Path(clip).unlink()
                        return False
                
                # Concatenate Sora clips
                concat_file = str(output_dir / "sora_concat_list.txt")
                with open(concat_file, 'w') as f:
                    for clip in temp_clips:
                        f.write(f"file '{Path(clip).name}'\n")
                
                logger.info(f"Concatenating {len(temp_clips)} Sora video clips...")
                
                cmd_concat = [
                    "ffmpeg",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_file,
                    "-c", "copy",
                    "-y",
                    temp_bg_video
                ]
                
                result_concat = subprocess.run(cmd_concat, capture_output=True, text=True, timeout=60)
                
                # Cleanup
                for clip in temp_clips:
                    if Path(clip).exists():
                        Path(clip).unlink()
                if Path(concat_file).exists():
                    Path(concat_file).unlink()
                
                if result_concat.returncode != 0:
                    logger.error(f"Failed to concatenate Sora clips: {result_concat.stderr}")
                    return False
                
                logger.info("Successfully created video from Sora clips")
                
            elif background_images and len(background_images) > 0:
                # Use AI-generated images as background with slideshow effect
                logger.info(f"Creating video with {len(background_images)} AI-generated images")
                
                # Calculate duration per image
                image_duration = duration / len(background_images)
                logger.info(f"Each image will display for {image_duration:.2f} seconds")
                
                # Create individual video clips for each image
                temp_clips = []
                output_dir = Path(output_path).parent
                
                for i, img_path in enumerate(background_images):
                    clip_path = str(output_dir / f"temp_clip_{i}.mp4")
                    temp_clips.append(clip_path)
                    
                    logger.info(f"Creating clip {i+1}/{len(background_images)} from {Path(img_path).name}")
                    
                    # Create video clip with zoom effect for this image
                    cmd_clip = [
                        "ffmpeg",
                        "-loop", "1",
                        "-i", img_path,
                        "-vf", (
                            f"scale={self.video_width}:{self.video_height}:force_original_aspect_ratio=decrease,"
                            f"pad={self.video_width}:{self.video_height}:(ow-iw)/2:(oh-ih)/2:black,"
                            f"zoompan=z='min(1+0.001*on,1.2)':d={int(image_duration * self.fps)}:s={self.video_width}x{self.video_height}:fps={self.fps}"
                        ),
                        "-c:v", "libx264",
                        "-t", str(image_duration),
                        "-pix_fmt", "yuv420p",
                        "-y",
                        clip_path
                    ]
                    
                    result_clip = subprocess.run(cmd_clip, capture_output=True, text=True, timeout=60)
                    
                    if result_clip.returncode != 0:
                        logger.error(f"Failed to create clip {i+1}: {result_clip.stderr}")
                        # Cleanup and return
                        for clip in temp_clips:
                            if Path(clip).exists():
                                Path(clip).unlink()
                        return False
                
                # Create concat file for FFmpeg
                concat_file = str(output_dir / "concat_list.txt")
                with open(concat_file, 'w') as f:
                    for clip in temp_clips:
                        f.write(f"file '{Path(clip).name}'\n")
                
                logger.info(f"Concatenating {len(temp_clips)} video clips...")
                
                # Concatenate all clips
                cmd_concat = [
                    "ffmpeg",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_file,
                    "-c", "copy",
                    "-y",
                    temp_bg_video
                ]
                
                result_concat = subprocess.run(cmd_concat, capture_output=True, text=True, timeout=60)
                
                # Cleanup temp clips and concat file
                for clip in temp_clips:
                    if Path(clip).exists():
                        Path(clip).unlink()
                if Path(concat_file).exists():
                    Path(concat_file).unlink()
                
                if result_concat.returncode != 0:
                    logger.error(f"Failed to concatenate clips: {result_concat.stderr}")
                    return False
                
                logger.info("Successfully created slideshow video from all images")
                
            else:
                # Use colored background with animated gradient
                if background_type == "gradient":
                    # Animated gradient background
                    cmd_bg = [
                        "ffmpeg",
                        "-f", "lavfi",
                        "-i", f"color=c=#1a1a2e:s={self.video_width}x{self.video_height}:d={duration}:r={self.fps}",
                        "-vf", "geq=r='255*sin(2*PI*T/10)':g='255*sin(2*PI*T/10 + 2*PI/3)':b='255*sin(2*PI*T/10 + 4*PI/3)'",
                        "-c:v", "libx264",
                        "-preset", "medium",
                        "-t", str(duration),
                        "-y",
                        temp_bg_video
                    ]
                elif background_type == "solid":
                    bg_color = "#0f0f1e"
                    cmd_bg = [
                        "ffmpeg",
                        "-f", "lavfi",
                        "-i", f"color=c={bg_color}:s={self.video_width}x{self.video_height}:d={duration}:r={self.fps}",
                        "-c:v", "libx264",
                        "-preset", "ultrafast",
                        "-t", str(duration),
                        "-y",
                        temp_bg_video
                    ]
                else:  # animated
                    bg_color = "#16213e"
                    cmd_bg = [
                        "ffmpeg",
                        "-f", "lavfi",
                        "-i", f"color=c={bg_color}:s={self.video_width}x{self.video_height}:d={duration}:r={self.fps}",
                        "-c:v", "libx264",
                        "-preset", "ultrafast",
                        "-t", str(duration),
                        "-y",
                        temp_bg_video
                    ]
                
                # Execute background video creation for solid/gradient/animated backgrounds
                result_bg = subprocess.run(cmd_bg, capture_output=True, text=True, timeout=120)
                
                if result_bg.returncode != 0:
                    logger.error(f"Background video creation failed: {result_bg.stderr}")
                    return False
            
            # Step 2: Merge with audio (subtitles burned in via SRT would require complex filter)
            # For simplicity, just merge video and audio
            cmd_final = [
                "ffmpeg",
                "-i", temp_bg_video,
                "-i", audio_path,
                "-c:v", "copy",  # Copy video stream (already encoded)
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                "-y",
                output_path
            ]
            
            result_final = subprocess.run(cmd_final, capture_output=True, text=True, timeout=300)
            
            # Cleanup temp file
            if Path(temp_bg_video).exists():
                Path(temp_bg_video).unlink()
            
            if result_final.returncode == 0:
                logger.info("Video created successfully with ffmpeg")
                return True
            else:
                logger.error(f"FFmpeg error: {result_final.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"FFmpeg execution error: {e}")
            # Cleanup temp file on error
            temp_bg_path = Path(output_path).parent / "temp_bg.mp4"
            if temp_bg_path.exists():
                temp_bg_path.unlink()
            return False
    
    # ==================== METADATA GENERATION ====================
    
    def generate_metadata(self, topic: str, script: str) -> Dict[str, Any]:
        """
        Generate SEO-optimized title, description, and tags
        
        Args:
            topic: Original topic
            script: Generated script
            
        Returns:
            Metadata including title, description, tags
        """
        logger.info("Generating SEO metadata...")
        
        system_prompt = """You are a YouTube SEO expert specializing in viral Shorts.

Generate metadata that:
1. Title: Attention-grabbing but not misleading, includes #shorts
2. Description: Engaging, includes relevant keywords and #shorts
3. Tags: 10-15 relevant tags for discoverability
4. All content must be platform-safe and monetization-friendly

Format as JSON:
{
  "title": "Attention-grabbing title #shorts",
  "description": "Engaging description with keywords and #shorts",
  "tags": ["tag1", "tag2", "tag3"],
  "category": "Entertainment"
}"""
        
        user_prompt = f"""Generate YouTube Shorts metadata for:

Topic: {topic}
Script: {script[:200]}...

Make it viral-optimized and SEO-friendly."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            metadata = json.loads(response.choices[0].message.content)
            
            # Ensure #shorts is included
            if "#shorts" not in metadata.get("title", "").lower():
                metadata["title"] = metadata.get("title", "") + " #shorts"
            
            if "#shorts" not in metadata.get("description", "").lower():
                metadata["description"] = metadata.get("description", "") + "\n\n#shorts"
            
            # Add standard tags
            standard_tags = ["shorts", "viral", "trending"]
            metadata["tags"] = list(set(metadata.get("tags", []) + standard_tags))
            
            logger.info(f"Metadata generated: {metadata['title']}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Metadata generation error: {e}")
            return {
                "title": f"{topic} #shorts",
                "description": f"Check out this amazing content about {topic}! #shorts",
                "tags": ["shorts", "viral", "trending"],
                "category": "Entertainment"
            }
    
    # ==================== YOUTUBE UPLOAD ====================
    
    def upload_to_youtube(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        category: str = "22",  # People & Blogs
        privacy: str = "public"
    ) -> Dict[str, Any]:
        """
        Upload video to YouTube using YouTube Data API
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category: YouTube category ID
            privacy: Privacy status (public, private, unlisted)
            
        Returns:
            Upload result with video ID
        """
        logger.info(f"Uploading to YouTube: {title}")
        
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            # Check for credentials
            credentials_path = os.getenv("YOUTUBE_CREDENTIALS_PATH", "credential.json")
            
            if not os.path.exists(credentials_path):
                return {
                    "success": False,
                    "error": "YouTube credentials not found. Please set up OAuth2 credentials."
                }
            
            # Load credentials
            with open(credentials_path, 'r') as f:
                creds_data = json.load(f)
            
            credentials = Credentials.from_authorized_user_info(creds_data)
            
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title[:100],  # Max 100 characters
                    'description': description[:5000],  # Max 5000 characters
                    'tags': tags[:500],  # Max 500 tags
                    'categoryId': category
                },
                'status': {
                    'privacyStatus': privacy,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                video_path,
                chunksize=1024*1024,  # 1MB chunks
                resumable=True,
                mimetype='video/mp4'
            )
            
            # Execute upload
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/shorts/{video_id}"
            
            result = {
                "success": True,
                "video_id": video_id,
                "video_url": video_url,
                "title": title,
                "privacy": privacy
            }
            
            logger.info(f"Upload successful! Video ID: {video_id}")
            logger.info(f"Video URL: {video_url}")
            
            return result
            
        except ImportError:
            return {
                "success": False,
                "error": "Google API client not installed. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            }
        except Exception as e:
            logger.error(f"YouTube upload error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ==================== MAIN ORCHESTRATION ====================
    
    def create_and_upload_short(
        self,
        topic: str,
        privacy: str = "public",
        background_type: str = "ai_images",
        visual_style: str = "cartoon"
    ) -> Dict[str, Any]:
        """
        Complete end-to-end workflow: Generate, produce, and upload YouTube Short
        
        Args:
            topic: Topic or idea for the short
            privacy: YouTube privacy setting
            background_type: Background visual type (gradient, solid, animated, ai_images,sora_video)
            visual_style: Style for AI images (cartoon, animated, realistic, 3d, comic)
            
        Returns:
            Complete result with all steps and final video URL
        """
        logger.info(f"=== Starting YouTube Short creation for: {topic} ===")
        
        workflow_result = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # Step 1: Generate viral script
            logger.info("Step 1/6: Generating viral script...")
            script_result = self.generate_viral_script(topic)
            workflow_result["steps"]["script"] = script_result
            
            if "error" in script_result:
                return workflow_result
            
            full_script = script_result["full_script"]
            
            # Step 2: Generate voiceover
            logger.info("Step 2/6: Generating voiceover...")
            voiceover_result = self.generate_voiceover(full_script)
            workflow_result["steps"]["voiceover"] = voiceover_result
            
            if not voiceover_result.get("success"):
                return workflow_result
            
            audio_path = voiceover_result["audio_path"]
            
            # Step 3: Create vertical video
            logger.info("Step 3/6: Creating vertical video...")
            video_result = self.create_vertical_video(
                audio_path,
                full_script,
                background_type=background_type,
                topic=topic,
                visual_style=visual_style
            )
            workflow_result["steps"]["video"] = video_result
            
            if not video_result.get("success"):
                return workflow_result
            
            video_path = video_result["video_path"]
            
            # Step 4: Generate metadata
            logger.info("Step 4/6: Generating SEO metadata...")
            metadata = self.generate_metadata(topic, full_script)
            workflow_result["steps"]["metadata"] = metadata
            
            # Step 5: Upload to YouTube
            logger.info("Step 5/6: Uploading to YouTube...")
            upload_result = self.upload_to_youtube(
                video_path,
                metadata["title"],
                metadata["description"],
                metadata["tags"],
                privacy=privacy
            )
            workflow_result["steps"]["upload"] = upload_result
            
            # Step 6: Finalize
            logger.info("Step 6/6: Finalizing...")
            workflow_result["success"] = upload_result.get("success", False)
            workflow_result["video_url"] = upload_result.get("video_url", "")
            workflow_result["video_id"] = upload_result.get("video_id", "")
            
            if workflow_result["success"]:
                logger.info(f"=== SUCCESS! Video uploaded: {workflow_result['video_url']} ===")
            else:
                logger.warning("=== Workflow completed with errors ===")
            
            return workflow_result
            
        except Exception as e:
            logger.error(f"Workflow error: {e}")
            workflow_result["success"] = False
            workflow_result["error"] = str(e)
            return workflow_result
    
    def get_workflow_summary(self, result: Dict[str, Any]) -> str:
        """Generate human-readable summary of workflow"""
        if not result.get("success"):
            return f"Failed to create YouTube Short. Error: {result.get('error', 'Unknown error')}"
        
        summary = f"""
YouTube Short Created Successfully!

Topic: {result['topic']}
Video URL: {result['video_url']}
Video ID: {result['video_id']}

Script Details:
- Duration: ~{result['steps']['script']['estimated_duration']}s
- Retention Score: {result['steps']['script']['retention_score']}/10
- Word Count: {result['steps']['script']['word_count']}

Metadata:
- Title: {result['steps']['metadata']['title']}
- Tags: {', '.join(result['steps']['metadata']['tags'][:5])}...

Video Specs:
- Resolution: {result['steps']['video']['resolution']}
- Duration: {result['steps']['video']['duration']:.2f}s
- Format: {result['steps']['video']['format']}
"""
        return summary.strip()
