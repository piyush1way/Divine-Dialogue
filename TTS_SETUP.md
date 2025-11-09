# 🔊 Text-to-Speech Setup Guide

## Overview

The Divine Dialogue app now supports streaming text-to-speech with randomized speaker order! Mentors' responses are converted to audio and played automatically as they speak.

## Features

✅ **Randomized Speaker Order** - Each question gets a different speaking order  
✅ **Streaming Audio** - Audio plays automatically as mentors speak  
✅ **Natural Pauses** - Brief pauses between speakers for conversational flow  
✅ **Multiple TTS Engines** - Supports pyttsx3 (local) and gTTS (Google)  
✅ **Zero Latency Option** - pyttsx3 processes locally, no API calls needed  

## Installation

### Option 1: pyttsx3 (Recommended for Hackathon)

**Pros:**
- ✅ Completely free
- ✅ Zero latency (local processing)
- ✅ Works offline
- ✅ No API keys needed

**Install:**
```bash
pip install pyttsx3
```

**Windows:** Works out of the box  
**Mac:** May require `brew install portaudio`  
**Linux:** May require `sudo apt-get install espeak` or `sudo apt-get install festival`

### Option 2: gTTS (Google TTS)

**Pros:**
- ✅ Better voice quality
- ✅ Free (no API key needed)
- ✅ Multiple languages

**Cons:**
- ⚠️ Requires internet connection
- ⚠️ ~2-3 second latency per request

**Install:**
```bash
pip install gtts
```

### Option 3: Both (Recommended)

Install both for flexibility:
```bash
pip install pyttsx3 gtts
```

## Usage

1. **Enable TTS in Sidebar:**
   - Check "Enable Text-to-Speech" checkbox
   - Optionally enable "Use Google TTS" for better quality

2. **Ask a Question:**
   - Type your question and click "Begin Divine Dialogue"
   - Mentors will speak in random order
   - Audio will play automatically

3. **Audio Controls:**
   - Each mentor's response has an audio player
   - Click play to replay any response
   - First audio autoplays (browser dependent)

## How It Works

1. **Randomization:**
   - Speaker order is randomized for each new question
   - Order is stored in session state for consistency
   - Same question = same order (until cleared)

2. **Audio Generation:**
   - Text is cleaned (HTML removed, formatted)
   - Converted to speech using selected TTS engine
   - Saved to `temp_audio/` directory
   - Audio player displayed for each response

3. **Natural Flow:**
   - Brief pause indicators between speakers
   - Audio format detected automatically (WAV/MP3)
   - Error handling with fallback to text display

## File Structure

```
temp_audio/
  ├── mentor_Krishna_1234567890.wav
  ├── mentor_Buddha_1234567891.wav
  └── mentor_Jesus_1234567892.wav
```

Audio files are automatically created in the `temp_audio/` directory.

## Troubleshooting

### No Audio Playing

1. **Check TTS Engine Status:**
   - Look at sidebar "TTS Engine Status"
   - Ensure at least one engine is available

2. **Install Missing Libraries:**
   ```bash
   pip install pyttsx3  # or gtts
   ```

3. **Check Browser Audio:**
   - Ensure browser allows autoplay
   - Some browsers block autoplay by default
   - Click play button manually if needed

### pyttsx3 Not Working on Mac/Linux

**Mac:**
```bash
brew install portaudio
pip install pyttsx3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install espeak
pip install pyttsx3
```

**Linux (Alternative):**
```bash
sudo apt-get install festival
pip install pyttsx3
```

### gTTS Not Working

- Check internet connection
- Ensure firewall allows outbound connections
- Try using pyttsx3 instead (local, no internet needed)

## Customization

### Change Speaking Rate

Edit `app.py`, line ~210:
```python
engine.setProperty('rate', 150)  # Change 150 to desired WPM
```

### Change Volume

Edit `app.py`, line ~211:
```python
engine.setProperty('volume', 0.9)  # Change 0.9 to 0.0-1.0
```

### Change Voice

Edit `app.py`, lines ~217-224:
```python
# Modify voice selection logic
# Prefer different voice characteristics
```

## Notes

- Audio files are stored in `temp_audio/` directory
- Files are named with timestamps to avoid conflicts
- Consider cleaning up old audio files periodically
- First audio autoplays (browser/Streamlit dependent)
- Subsequent audios require manual play (browser limitation)

## Future Enhancements

- [ ] ElevenLabs integration (premium voices)
- [ ] Voice differentiation per mentor
- [ ] Background audio playback
- [ ] Audio download option
- [ ] Automatic cleanup of old audio files

