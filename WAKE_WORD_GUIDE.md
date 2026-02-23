# Wake Word Activation - Surya

Your voice assistant is now named **Surya** and uses wake word activation for hands-free operation.

## How It Works

### Wake Word Mode (Default)
When you start the application, Surya is in **wake word mode** - passively listening for the activation phrase.

**Activation Phrases:**
- "Hello Surya" (English)
- "Hi Surya" (English)
- "हैलो सूर्या" (Hindi)
- "सूर्या" (Hindi)

### Activation Flow

1. **Start Application**: Surya starts in wake word mode
   - Status: "Say 'Hello Surya' to activate"
   - Microphone is on, listening only for wake word

2. **Say Wake Word**: "Hello Surya" or "Hi Surya"
   - Status changes to: "Activating..."
   - Surya responds: "Yes, I'm listening"
   - Automatically switches to active listening mode after speaking

3. **Active Listening**: After confirmation speech finishes
   - Status: "Listening..."
   - Now ready to receive your command

4. **Give Command**: Speak your request
   - Example: "Open Windsurf IDE"
   - Example: "Create a new file"
   - Example: "विंडसर्फ खोलो"

5. **Surya Responds**: Processes and responds to your command

6. **Continues Listening**: After completing the task
   - Stays in active listening mode
   - Status: "Listening..."
   - Ready for your next command immediately
   - No need to say wake word again

7. **End Conversation**: Say exit command to close
   - "Bye" / "Goodbye" / "Exit"
   - Returns to wake word mode on next start

## Conversation Flow

**Once activated with wake word:**
- Surya stays in active listening mode
- You can have a continuous conversation
- No need to repeat "Hello Surya" for each command
- Just speak naturally, one command after another

**To end conversation:**
- Say "Bye" or "Exit"
- Or click the 🎤 microphone button to manually stop

## Toggle Modes

Click the **🎤 microphone button** to:
- **Stop listening**: Returns to wake word mode
- **Start listening**: Activates without wake word

## Wake Word Detection

The system detects these variations:
- `surya` (lowercase)
- `Surya` (capitalized)
- `सूर्या` (Hindi - Sūryā)
- `सूर्य` (Hindi - Sūrya)

Works in phrases like:
- "Hello Surya"
- "Hi Surya"
- "Hey Surya"
- "Surya, open the file"

## Benefits

1. **Privacy**: Only activates when you want it to
2. **Battery Efficient**: Passive listening uses less resources
3. **Hands-Free**: No need to click buttons
4. **Natural**: Just say the name like calling a person

## Exit Commands

To close Surya, say:
- "Bye" / "Goodbye" / "Exit" / "Shutdown"
- "बाय" / "गुडबाय" / "बंद करो"

Surya will say goodbye and close gracefully.

## Troubleshooting

**Wake word not detected?**
- Speak clearly and at normal volume
- Try different variations: "Hello Surya", "Hi Surya"
- Check microphone permissions
- Ensure Hindi language support is working

**Want continuous listening?**
- Click the microphone button to disable wake word mode
- Surya will listen continuously without requiring activation

## Example Session

```
[App starts]
Status: "Say 'Hello Surya' to activate"

You: "Hello Surya"
Surya: "Yes, I'm listening"
Status: "Listening..."

You: "Open Windsurf IDE"
Status: "Thinking..."
Surya: "Windsurf IDE launched successfully"
Status: "Speaking..."

[After response]
Status: "Say 'Hello Surya' to activate"

You: "Hi Surya"
Surya: "Yes, I'm listening"

You: "Create a new file called test.py"
Surya: "File created: test.py"

[Returns to wake word mode]
```

Enjoy your hands-free AI assistant! 🎤
