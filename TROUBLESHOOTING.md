# Troubleshooting Guide - Surya Voice Assistant

## Common Issues and Solutions

### 1. QTimer Threading Error

**Error Message:**
```
QObject::startTimer: Timers cannot be started from another thread
```

**Cause:** Speech recognition callback runs in a separate thread, cannot directly use QTimer

**Solution:** ✅ Fixed - Now using Qt signals for thread-safe communication
- `activate_signal` emitted from STT thread
- Signal connected to `delayed_activate_listening()` slot in main thread
- QTimer.singleShot() called safely from main thread

---

### 2. TTS Feedback Loop

**Symptom:** 
- Wake word detection picks up Surya's own voice
- Logs show: "Wake word check: एस आई एम लिसनिंग" (recognizing "Yes I'm listening")
- Assistant doesn't activate properly

**Cause:** Microphone was still listening while TTS was speaking

**Solution:** ✅ Fixed - Microphone is now stopped before TTS speaks confirmation

**How it works now:**
1. Wake word detected → Stop listening immediately
2. Speak confirmation: "Yes, I'm listening"
3. Wait 2.5 seconds for TTS to finish
4. Start active listening for commands

---

### 3. Wake Word Not Activating

**Symptoms:**
- Says "Yes, I'm listening" but doesn't actually listen
- Status doesn't change to "Listening..."

**Solution:** ✅ Fixed
- Flags are now set immediately when wake word is detected
- Proper state transition from wake word mode to active listening
- Timer properly reconnects to correct callback functions

---

### 4. Microphone Not Working

**Check:**
- System Preferences → Security & Privacy → Microphone
- Grant Terminal/Python microphone access
- Restart application after granting permissions

---

### 5. Hindi Voice Not Speaking Properly

**Issue:** Reading punctuation instead of Hindi words

**Solution:** ✅ Fixed - Changed voice from "Samantha" to "Lekha"
- Lekha is the Hindi female voice on macOS
- Properly pronounces Hindi text

---

### 6. Wake Word Not Detected

**Try these variations:**
- "Hello Surya"
- "Hi Surya"
- "Hey Surya"
- "हैलो सूर्या"
- "सूर्या"

**Tips:**
- Speak clearly at normal volume
- Ensure you're in a quiet environment
- Check microphone input levels in System Preferences

---

### 7. Application Won't Exit

**Exit commands:**
- "Bye" / "Goodbye"
- "Exit" / "Quit"
- "Shutdown" / "Shut down"
- "बाय" / "गुडबाय"
- "बंद करो" / "शट डाउन"

**If stuck:** Press `Ctrl+C` in terminal

---

### 8. OpenAI API Errors

**Check:**
- Verify API key is set: `echo $OPENAI_API_KEY`
- Check API quota/billing at platform.openai.com
- Ensure internet connection is active

**Error:** "I apologize, but I encountered an error processing your request"
- Check logs for specific error
- Verify OpenAI API key is valid
- Check network connectivity

---

### 9. Windsurf IDE Not Opening

**Issue:** Voice command to open Windsurf doesn't work

**Solutions:**
- Ensure Windsurf is installed in Applications folder
- Try: "Open Windsurf IDE"
- Try: "Launch Windsurf"
- Check if Windsurf app name is correct on your system

---

## Debug Mode

To see detailed logs, the application already runs with `INFO` level logging.

**Check logs for:**
- `Wake word check:` - Shows what text was detected
- `Recognized:` - Shows speech-to-text output
- `Response:` - Shows AI response
- `Executing tool:` - Shows which Windsurf tools are being called

---

## Performance Tips

1. **Reduce background noise** for better wake word detection
2. **Speak clearly** with pauses between commands
3. **Wait for status change** before giving next command
4. **Use wake word mode** to save battery/resources

---

## Getting Help

If issues persist:
1. Check the logs in terminal
2. Verify all dependencies are installed
3. Ensure Python 3.8+ is being used
4. Check microphone permissions
5. Restart the application

---

## Known Limitations

- Wake word detection works best in quiet environments
- Hindi speech recognition accuracy depends on accent and clarity
- Windsurf IDE operations require Windsurf to be installed
- Internet connection required for OpenAI API calls
