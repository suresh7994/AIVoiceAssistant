# Testing Wake Word Activation

## How to Test

1. **Start the application:**
   ```bash
   python3 main.py
   ```

2. **Check initial status:**
   - Should show: "Say 'Hello Surya' to activate"

3. **Say wake word:**
   - Say: "Hello Surya" or "Hi Surya"
   - Watch the logs in terminal

4. **Expected log sequence:**
   ```
   INFO:__main__:Wake word check: सूर्य
   INFO:__main__:Surya activated!
   INFO:__main__:Wake word activation sequence started
   INFO:__main__:Delayed activation triggered...
   [TTS speaks: "Yes, I'm listening"]
   [Wait 2.5 seconds]
   INFO:__main__:Activating listening mode after wake word...
   INFO:__main__:State: is_listening=True, wake_word_mode=False, auto_listen=True
   INFO:__main__:Active listening started - ready for commands
   ```
   
   **Note:** You should NOT see "QObject::startTimer: Timers cannot be started from another thread"

5. **Status should change to:**
   - "Activating..." (during TTS)
   - "Listening..." (after activation)

6. **Give a command:**
   - Say: "What can you do?"
   - Watch for: `INFO:__main__:on_speech_recognized called with: [your text]`

7. **Expected behavior:**
   - Command should be recognized
   - AI should process and respond
   - After response, **stays in "Listening..." mode**
   - Ready for next command immediately
   
8. **Give another command:**
   - No need to say "Hello Surya" again
   - Just speak your next command
   - Continuous conversation mode

## Debug Checklist

If "Listening..." appears but commands aren't recognized:

- [ ] Check logs for `on_speech_recognized called with:`
- [ ] Verify `is_processing` is False
- [ ] Verify `wake_word_mode` is False
- [ ] Check if microphone is actually listening (audio input indicator)
- [ ] Try speaking louder or clearer

## Common Issues

### Issue: Status shows "Listening..." but no response to commands

**Check logs for:**
1. Is `on_speech_recognized` being called?
   - YES → Check if `is_processing=True` is blocking
   - NO → Speech-to-text might not be working

2. Is speech being recognized at all?
   - Check for "Recognized: [text]" in logs
   - If missing, microphone might not be active

### Issue: Wake word detected but activation doesn't happen

**Check logs for:**
- "Activating listening mode after wake word..." should appear after 2.5 seconds
- If missing, timer might not be firing

### Issue: Commands recognized but not processed

**Check logs for:**
- "Current state - is_processing: [value]"
- If `is_processing=True`, previous command might still be running

## Manual Override

If wake word mode isn't working:
- Click the 🎤 microphone button
- This toggles to always-on listening mode
- No wake word needed in this mode
