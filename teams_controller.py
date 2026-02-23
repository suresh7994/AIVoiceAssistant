import requests
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeamsController:
    """Controller for Microsoft Teams operations - meetings and chats"""
    
    def __init__(self):
        self.access_token = None
        self.token_expiry = None
        self.client_id = os.getenv("TEAMS_CLIENT_ID")
        self.client_secret = os.getenv("TEAMS_CLIENT_SECRET")
        self.tenant_id = os.getenv("TEAMS_TENANT_ID")
        self.base_url = "https://graph.microsoft.com/v1.0"
        
    def authenticate(self) -> Dict[str, Any]:
        """Authenticate with Microsoft Graph API using client credentials flow"""
        try:
            if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
                return {"success": True, "message": "Already authenticated"}
            
            if not all([self.client_id, self.client_secret, self.tenant_id]):
                return {
                    "success": False,
                    "error": "Teams credentials not configured. Set TEAMS_CLIENT_ID, TEAMS_CLIENT_SECRET, and TEAMS_TENANT_ID environment variables."
                }
            
            token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://graph.microsoft.com/.default",
                "grant_type": "client_credentials"
            }
            
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                expires_in = token_data.get("expires_in", 3600)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
                
                return {"success": True, "message": "Authenticated with Microsoft Teams"}
            else:
                return {"success": False, "error": f"Authentication failed: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers for API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def schedule_meeting(
        self,
        subject: str,
        start_time: str,
        duration_minutes: int = 60,
        attendees: List[str] = None,
        description: str = ""
    ) -> Dict[str, Any]:
        """Schedule a Teams meeting
        
        Args:
            subject: Meeting title
            start_time: ISO format datetime string (e.g., "2026-02-24T14:00:00")
            duration_minutes: Meeting duration in minutes
            attendees: List of email addresses
            description: Meeting description
        """
        try:
            auth_result = self.authenticate()
            if not auth_result["success"]:
                return auth_result
            
            # Parse start time
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = start_dt + timedelta(minutes=duration_minutes)
            
            # Build attendees list
            attendee_list = []
            if attendees:
                for email in attendees:
                    attendee_list.append({
                        "emailAddress": {
                            "address": email,
                            "name": email.split('@')[0]
                        },
                        "type": "required"
                    })
            
            # Create meeting payload
            meeting_data = {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": description
                },
                "start": {
                    "dateTime": start_dt.isoformat(),
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_dt.isoformat(),
                    "timeZone": "UTC"
                },
                "attendees": attendee_list,
                "isOnlineMeeting": True,
                "onlineMeetingProvider": "teamsForBusiness"
            }
            
            # Create the meeting
            url = f"{self.base_url}/me/events"
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=meeting_data
            )
            
            if response.status_code in [200, 201]:
                meeting = response.json()
                return {
                    "success": True,
                    "message": f"Meeting '{subject}' scheduled successfully",
                    "meeting_id": meeting.get("id"),
                    "join_url": meeting.get("onlineMeeting", {}).get("joinUrl"),
                    "start_time": start_time
                }
            else:
                return {"success": False, "error": f"Failed to create meeting: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_recent_chats(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent individual chats (not group chats)"""
        try:
            auth_result = self.authenticate()
            if not auth_result["success"]:
                return auth_result
            
            url = f"{self.base_url}/me/chats"
            params = {
                "$top": limit,
                "$filter": "chatType eq 'oneOnOne'",
                "$expand": "lastMessagePreview"
            }
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            
            if response.status_code == 200:
                chats_data = response.json()
                chats = []
                
                for chat in chats_data.get("value", []):
                    chat_info = {
                        "chat_id": chat.get("id"),
                        "topic": chat.get("topic", "Direct Chat"),
                        "last_message": chat.get("lastMessagePreview", {}).get("body", {}).get("content", ""),
                        "last_updated": chat.get("lastUpdatedDateTime")
                    }
                    chats.append(chat_info)
                
                return {
                    "success": True,
                    "chats": chats,
                    "count": len(chats)
                }
            else:
                return {"success": False, "error": f"Failed to get chats: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_chat_messages(self, chat_id: str, limit: int = 20) -> Dict[str, Any]:
        """Get messages from a specific chat"""
        try:
            auth_result = self.authenticate()
            if not auth_result["success"]:
                return auth_result
            
            url = f"{self.base_url}/chats/{chat_id}/messages"
            params = {"$top": limit}
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            
            if response.status_code == 200:
                messages_data = response.json()
                messages = []
                
                for msg in messages_data.get("value", []):
                    message_info = {
                        "message_id": msg.get("id"),
                        "from": msg.get("from", {}).get("user", {}).get("displayName", "Unknown"),
                        "content": msg.get("body", {}).get("content", ""),
                        "created": msg.get("createdDateTime")
                    }
                    messages.append(message_info)
                
                return {
                    "success": True,
                    "messages": messages,
                    "count": len(messages)
                }
            else:
                return {"success": False, "error": f"Failed to get messages: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_chat_message(self, chat_id: str, message: str) -> Dict[str, Any]:
        """Send a message to an individual chat"""
        try:
            auth_result = self.authenticate()
            if not auth_result["success"]:
                return auth_result
            
            url = f"{self.base_url}/chats/{chat_id}/messages"
            
            message_data = {
                "body": {
                    "content": message,
                    "contentType": "text"
                }
            }
            
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=message_data
            )
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message": "Message sent successfully"
                }
            else:
                return {"success": False, "error": f"Failed to send message: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def reply_to_latest_chat(self, message: str) -> Dict[str, Any]:
        """Reply to the most recent individual chat"""
        try:
            # Get recent chats
            chats_result = self.get_recent_chats(limit=1)
            
            if not chats_result["success"]:
                return chats_result
            
            if not chats_result.get("chats"):
                return {"success": False, "error": "No recent chats found"}
            
            latest_chat = chats_result["chats"][0]
            chat_id = latest_chat["chat_id"]
            
            # Send the message
            return self.send_chat_message(chat_id, message)
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_chat_by_person(self, person_name: str) -> Dict[str, Any]:
        """Find a chat with a specific person"""
        try:
            auth_result = self.authenticate()
            if not auth_result["success"]:
                return auth_result
            
            # Get all one-on-one chats
            url = f"{self.base_url}/me/chats"
            params = {
                "$filter": "chatType eq 'oneOnOne'",
                "$expand": "members"
            }
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            
            if response.status_code == 200:
                chats_data = response.json()
                
                for chat in chats_data.get("value", []):
                    members = chat.get("members", [])
                    for member in members:
                        display_name = member.get("displayName", "")
                        if person_name.lower() in display_name.lower():
                            return {
                                "success": True,
                                "chat_id": chat.get("id"),
                                "person": display_name
                            }
                
                return {
                    "success": False,
                    "error": f"No chat found with {person_name}"
                }
            else:
                return {"success": False, "error": f"Failed to search chats: {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}


# Tool definitions for OpenAI function calling
TEAMS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "schedule_teams_meeting",
            "description": "Schedule a Microsoft Teams meeting. Use this when user wants to schedule, set up, or create a meeting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Meeting title/subject"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Meeting start time in ISO format (YYYY-MM-DDTHH:MM:SS)"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Meeting duration in minutes (default: 60)"
                    },
                    "attendees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of attendee email addresses"
                    },
                    "description": {
                        "type": "string",
                        "description": "Meeting description or agenda"
                    }
                },
                "required": ["subject", "start_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_teams_chats",
            "description": "Get recent individual Teams chats (not group chats). Use this when user asks about recent messages or chats.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of chats to retrieve (default: 10)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_teams_message",
            "description": "Send a message to a Teams chat. Use this when user wants to reply or send a message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "The ID of the chat to send message to"
                    },
                    "message": {
                        "type": "string",
                        "description": "The message content to send"
                    }
                },
                "required": ["chat_id", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reply_to_latest_teams_chat",
            "description": "Reply to the most recent individual Teams chat. Use this when user says 'reply to my latest message' or similar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The reply message to send"
                    }
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_teams_chat_by_person",
            "description": "Find a chat with a specific person by name. Use this when user wants to message someone specific.",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_name": {
                        "type": "string",
                        "description": "Name of the person to find chat with"
                    }
                },
                "required": ["person_name"]
            }
        }
    }
]
