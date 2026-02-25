"""
YouTube Shorts Agent Tools for OpenAI Function Calling
"""

YOUTUBE_SHORTS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_youtube_short",
            "description": "Fully autonomous creation and upload of a YouTube Short from a topic. Generates viral script, voiceover, vertical video with subtitles, SEO metadata, and uploads to YouTube. Complete end-to-end automation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic or idea for the YouTube Short. Can be specific or general - the agent will optimize it for virality."
                    },
                    "privacy": {
                        "type": "string",
                        "enum": ["public", "private", "unlisted"],
                        "description": "YouTube privacy setting (default: public)"
                    },
                    "background_type": {
                        "type": "string",
                        "enum": ["gradient", "solid", "animated", "ai_images", "sora_video"],
                        "description": "Type of background visual. 'ai_images' generates AI images using DALL-E (default), 'sora_video' generates actual video clips using OpenAI Sora (gpt-video-1) matching the script content. Use 'gradient', 'solid', or 'animated' for simple colored backgrounds without visuals."
                    },
                    "visual_style": {
                        "type": "string",
                        "enum": ["cartoon", "animated", "realistic", "3d", "comic", "abstract"],
                        "description": "Visual style for AI-generated content. Used with 'ai_images' or 'sora_video'. Options: cartoon (vibrant illustrations/animation), animated (Pixar-style 3D), realistic (photorealistic), 3d (modern CGI), comic (comic book art), abstract (artistic visuals)"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_shorts_script",
            "description": "Generate a viral YouTube Shorts script optimized for high retention. Creates hook, body, and CTA with retention scoring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic for the short"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_shorts_voiceover",
            "description": "Generate natural human-like voiceover for a script using AI text-to-speech.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Script text to convert to speech"
                    }
                },
                "required": ["script"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_shorts_video",
            "description": "Create vertical video (9:16, 1080x1920) with synchronized subtitles and background visuals.",
            "parameters": {
                "type": "object",
                "properties": {
                    "audio_path": {
                        "type": "string",
                        "description": "Path to voiceover audio file"
                    },
                    "script": {
                        "type": "string",
                        "description": "Script text for subtitles"
                    },
                    "background_type": {
                        "type": "string",
                        "enum": ["gradient", "solid", "animated"],
                        "description": "Background visual type"
                    }
                },
                "required": ["audio_path", "script"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_shorts_metadata",
            "description": "Generate SEO-optimized title, description, and tags for YouTube Shorts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Original topic"
                    },
                    "script": {
                        "type": "string",
                        "description": "Generated script"
                    }
                },
                "required": ["topic", "script"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "upload_short_to_youtube",
            "description": "Upload a video to YouTube as a Short with metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to video file"
                    },
                    "title": {
                        "type": "string",
                        "description": "Video title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Video description"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags"
                    },
                    "privacy": {
                        "type": "string",
                        "enum": ["public", "private", "unlisted"],
                        "description": "Privacy setting"
                    }
                },
                "required": ["video_path", "title", "description"]
            }
        }
    }
]
