# Microsoft Teams Integration

Surya can now schedule meetings and reply to individual chats on Microsoft Teams using voice commands!

## Features

### 1. Schedule Teams Meetings
Create Teams meetings with attendees, time, and agenda.

**Voice Commands:**
- "Schedule a meeting tomorrow at 2 PM"
- "Set up a Teams meeting with John at 3 PM"
- "Create a meeting called 'Project Review' on Monday at 10 AM"
- "कल दोपहर 2 बजे मीटिंग शेड्यूल करो"

**What it does:**
- Creates online Teams meeting
- Adds attendees by email
- Sets meeting duration
- Generates Teams meeting link
- Sends calendar invites

### 2. Reply to Individual Chats
Read and respond to your Teams chats (individual only, not group chats).

**Voice Commands:**
- "Reply to my latest Teams message"
- "Send a message to John on Teams"
- "What are my recent Teams chats?"
- "मेरे लेटेस्ट मैसेज का जवाब दो"

**What it does:**
- Reads recent individual chats
- Sends replies to specific people
- Finds chats by person name
- **Note:** Only works with individual (one-on-one) chats, NOT group chats

## Setup Required

### Step 1: Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in:
   - **Name**: "Surya Voice Assistant"
   - **Supported account types**: "Accounts in this organizational directory only"
   - **Redirect URI**: Leave blank for now
5. Click **Register**

### Step 2: Get Application Credentials

1. On the app overview page, copy:
   - **Application (client) ID**
   - **Directory (tenant) ID**

2. Go to **Certificates & secrets**
3. Click **New client secret**
4. Add description: "Surya Voice Assistant Secret"
5. Set expiration (recommended: 24 months)
6. Click **Add**
7. **Copy the secret value immediately** (you won't see it again!)

### Step 3: Configure API Permissions

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions** (not Delegated)
5. Add these permissions:
   - `Calendars.ReadWrite` - For scheduling meetings
   - `Chat.Read.All` - For reading chats
   - `Chat.ReadWrite.All` - For sending messages
   - `User.Read.All` - For finding users
   - `OnlineMeetings.ReadWrite.All` - For Teams meeting links

6. Click **Add permissions**
7. Click **Grant admin consent** (requires admin)
8. Confirm the consent

### Step 4: Set Environment Variables

Add these to your `.env` file:

```bash
# Microsoft Teams Configuration
TEAMS_CLIENT_ID=your-application-client-id
TEAMS_CLIENT_SECRET=your-client-secret-value
TEAMS_TENANT_ID=your-directory-tenant-id
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

The `requests` library is now included for Teams API calls.

## Usage Examples

### Example 1: Schedule a Meeting

```
You: "Hello Surya"
Surya: "Yes, I'm listening"

You: "Schedule a meeting tomorrow at 2 PM with john@company.com"
Surya: "What should the meeting be about?"

You: "Project status review"
Surya: "Meeting 'Project status review' scheduled successfully for tomorrow at 2 PM"
```

### Example 2: Reply to Chat

```
You: "What are my recent Teams chats?"
Surya: "You have 3 recent chats: John Smith, Sarah Johnson, Mike Davis"

You: "Reply to John's message saying 'I'll review it today'"
Surya: "Message sent successfully to John Smith"
```

### Example 3: Quick Reply

```
You: "Reply to my latest Teams message"
Surya: "What would you like to say?"

You: "Thanks for the update, I'll get back to you soon"
Surya: "Message sent successfully"
```

## Voice Commands Reference

### Scheduling Meetings

**English:**
- "Schedule a meeting [time] with [attendees]"
- "Set up a Teams meeting called [subject]"
- "Create a meeting on [date] at [time]"
- "Book a meeting for [duration] minutes"

**Hindi:**
- "मीटिंग शेड्यूल करो [time] पर"
- "Teams मीटिंग सेट करो"
- "[date] को मीटिंग बनाओ"

**Parameters:**
- **Subject**: Meeting title
- **Time**: "tomorrow at 2 PM", "Monday at 10 AM", "2026-02-24T14:00:00"
- **Duration**: Default 60 minutes, can specify "30 minutes", "2 hours"
- **Attendees**: Email addresses "john@company.com, sarah@company.com"
- **Description**: Optional meeting agenda

### Managing Chats

**English:**
- "Show my recent Teams chats"
- "What are my latest messages?"
- "Reply to [person name]"
- "Send a message to [person]"
- "Reply to my latest chat"

**Hindi:**
- "मेरे Teams चैट दिखाओ"
- "लेटेस्ट मैसेज क्या हैं?"
- "[person] को रिप्लाई करो"
- "लेटेस्ट चैट का जवाब दो"

## How It Works

### Authentication
- Uses **OAuth 2.0 Client Credentials Flow**
- Application permissions (not user delegation)
- Token automatically refreshed when expired
- Secure token storage in memory

### API Integration
- **Microsoft Graph API v1.0**
- RESTful API calls
- JSON data format
- HTTPS encrypted communication

### Meeting Creation
1. Parses meeting details from voice command
2. Converts to ISO datetime format
3. Creates calendar event via Graph API
4. Generates Teams meeting link automatically
5. Sends invites to attendees

### Chat Management
1. Fetches one-on-one chats only (filters out group chats)
2. Reads recent messages
3. Identifies chat by person name
4. Sends message to specific chat ID
5. Confirms delivery

## Limitations

### Current Limitations
- **Individual chats only**: Cannot send to group chats or channels
- **Application permissions**: Requires admin consent
- **No real-time notifications**: Polls for new messages on request
- **Text messages only**: No support for attachments, emojis, or rich formatting
- **Meeting attendees**: Must provide email addresses
- **Time zones**: Uses UTC, converts based on system timezone

### Security Considerations
- Credentials stored in `.env` file (keep secure!)
- Never commit `.env` to version control
- Token expires and auto-refreshes
- Application has broad permissions (admin approved)
- All API calls are logged

## Troubleshooting

### Authentication Failed

**Error:** "Teams credentials not configured"

**Solution:**
- Check `.env` file has all three variables set
- Verify credentials are correct
- Ensure no extra spaces in values

### Permission Denied

**Error:** "Insufficient privileges to complete the operation"

**Solution:**
- Verify API permissions are added in Azure Portal
- Ensure admin consent is granted
- Wait a few minutes for permissions to propagate

### Meeting Not Created

**Error:** "Failed to create meeting"

**Solution:**
- Check time format is correct
- Ensure attendee emails are valid
- Verify you have calendar permissions
- Check meeting is not in the past

### Chat Not Found

**Error:** "No chat found with [person]"

**Solution:**
- Ensure you have an existing chat with that person
- Try using their full name
- Check spelling
- Person must be in your organization

### Group Chat Error

**Error:** "Only individual chats supported"

**Solution:**
- This is by design - group chats are not supported
- Use individual chats only
- For group communication, schedule a meeting instead

## Advanced Usage

### Custom Meeting Duration

```
You: "Schedule a 30-minute meeting with John tomorrow at 3 PM"
```

### Multiple Attendees

```
You: "Create a meeting with john@company.com and sarah@company.com on Friday at 2 PM"
```

### Meeting with Agenda

```
You: "Schedule a meeting called 'Sprint Planning' tomorrow at 10 AM with the team. The agenda is to review sprint goals and assign tasks."
```

### Find and Reply

```
You: "Find my chat with Sarah"
Surya: "Found chat with Sarah Johnson"

You: "Send her a message saying 'Meeting confirmed for tomorrow'"
Surya: "Message sent successfully"
```

## Technical Details

### TeamsController Methods

1. **`authenticate()`**
   - Gets OAuth token from Microsoft
   - Caches token until expiry
   - Auto-refreshes when needed

2. **`schedule_meeting(subject, start_time, duration, attendees, description)`**
   - Creates calendar event
   - Generates Teams meeting link
   - Sends invites

3. **`get_recent_chats(limit=10)`**
   - Fetches one-on-one chats
   - Filters out group chats
   - Returns chat metadata

4. **`send_chat_message(chat_id, message)`**
   - Sends text message to chat
   - Returns success confirmation

5. **`reply_to_latest_chat(message)`**
   - Gets most recent chat
   - Sends reply automatically

6. **`find_chat_by_person(person_name)`**
   - Searches chats by display name
   - Returns chat ID for messaging

### API Endpoints Used

- **Authentication**: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token`
- **Create Meeting**: `POST /me/events`
- **Get Chats**: `GET /me/chats?$filter=chatType eq 'oneOnOne'`
- **Send Message**: `POST /chats/{chat-id}/messages`
- **Get Messages**: `GET /chats/{chat-id}/messages`

### Data Flow

```
Voice Command
    ↓
Speech-to-Text (Hindi/English)
    ↓
OpenAI GPT (Intent Recognition)
    ↓
Tool Selection (schedule_teams_meeting / send_teams_message)
    ↓
TeamsController (API Call)
    ↓
Microsoft Graph API
    ↓
Teams Platform
    ↓
Response to User (Voice)
```

## Privacy & Compliance

- **Data Access**: Application can read your chats and calendar
- **Data Storage**: No chat data stored locally
- **Logging**: API calls are logged for debugging
- **Compliance**: Ensure your organization allows API access
- **Audit**: All actions are auditable in Microsoft 365 logs

## Future Enhancements

Potential additions:
- Group chat support (requires different permissions)
- Read unread messages only
- Meeting cancellation/rescheduling
- Attachment support
- Presence status updates
- Calendar availability checking
- Meeting transcription integration

## Support

For issues:
1. Check Azure Portal for permission errors
2. Verify credentials in `.env`
3. Review logs for API errors
4. Ensure Teams license is active
5. Contact IT admin for permission issues
