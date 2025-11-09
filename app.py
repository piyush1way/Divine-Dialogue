#!/usr/bin/env python3
"""
🎭 Divine Dialogue - Multi-Perspective Spiritual Debate
Enhanced Streamlit Web Interface with all Phase 2 features
"""

import streamlit as st
import os
import html
import random
import time
import threading
import base64
from datetime import datetime
from pathlib import Path
from divine_dialogue_langgraph import run_divine_dialogue, run_follow_up, load_rag_database

# TTS imports (try multiple options)
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    import io
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Gyan Samvad",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS
dark_theme_css = """
<style>
    /* Dark theme background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        background-attachment: fixed;
    }

    [data-testid="stMainBlockContainer"] {
        background-color: transparent;
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #2a3f5f 100%);
        border-right: 2px solid #3a4f7f;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }

    .stTextInput > div > div > input {
        background-color: #1a1f3a;
        color: #ffffff;
        border: 2px solid #3a4f7f;
        border-radius: 8px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }

    .stTextArea > div > div > textarea {
        background-color: #1a1f3a;
        color: #ffffff;
        border: 2px solid #3a4f7f;
        border-radius: 8px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }

    .stSelectbox > div > div > select {
        background-color: #1a1f3a;
        color: #ffffff;
        border: 2px solid #3a4f7f;
        border-radius: 8px;
    }

    /* Ensure text is readable on dark background */
    .stMarkdown, .stText {
        color: #ffffff;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    p {
        color: #e0e0e0;
        line-height: 1.6;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Card animations */
    .krishna-card, .buddha-card, .jesus-card {
        animation: fadeInUp 0.5s ease-out;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1f3a;
    }

    ::-webkit-scrollbar-thumb {
        background: #3a4f7f;
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #4a5f8f;
    }
</style>
"""
st.markdown(dark_theme_css, unsafe_allow_html=True)

# Custom CSS with mentor-specific colors
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Mentor-specific card colors */
    .krishna-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1a1a1a;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 12px rgba(255,215,0,0.3);
        border-left: 5px solid #FF8C00;
    }
    
    .buddha-card {
        background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 12px rgba(74,144,226,0.3);
        border-left: 5px solid #4169E1;
    }
    
    .jesus-card {
        background: linear-gradient(135deg, #F8F8FF 0%, #E6E6FA 100%);
        color: #1a1a1a;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 12px rgba(230,230,250,0.5);
        border-left: 5px solid #9370DB;
    }
    
    .synthesis-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .citation-box {
        background: rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    
    .verse-text {
        font-style: italic;
        padding-left: 1rem;
        border-left: 3px solid rgba(255,255,255,0.5);
        margin: 0.5rem 0;
    }
    
    .agreement-meter {
        background: linear-gradient(90deg, #FF6B6B 0%, #FFD93D 50%, #6BCF7F 100%);
        height: 30px;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 1rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .question-display {
        background: linear-gradient(135deg, #1a1f3a 0%, #2a3f5f 100%);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .question-display h3 {
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .question-display p {
        color: #e0e0e0;
    }
    
    /* Bullet point styling */
    .bullet-point {
        margin: 0.8rem 0;
        padding-left: 0.5rem;
        line-height: 1.8;
    }
    
    .bullet-main {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    
    .bullet-sub {
        margin-left: 1.5rem;
        color: #d0d0d0;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'dialogue_history' not in st.session_state:
        st.session_state.dialogue_history = []
    if 'rag_loaded' not in st.session_state:
        st.session_state.rag_loaded = False
    if 'current_dialogue' not in st.session_state:
        st.session_state.current_dialogue = None
    if 'follow_up_mode' not in st.session_state:
        st.session_state.follow_up_mode = False
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    if 'displayed_question' not in st.session_state:
        st.session_state.displayed_question = None
    # Recursive conversation state management
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []  # Full conversation history for follow-ups
    if 'initial_responses' not in st.session_state:
        st.session_state.initial_responses = {}  # Store initial mentor responses
    if 'user_background' not in st.session_state:
        st.session_state.user_background = ""  # Store user background
    if 'user_background_stored' not in st.session_state:
        st.session_state.user_background_stored = ''  # Store user background for follow-ups
    if 'selected_mentor' not in st.session_state:
        st.session_state.selected_mentor = None
    if 'follow_up_responses' not in st.session_state:
        st.session_state.follow_up_responses = []  # Store follow-up responses
    # # TTS SESSION STATE COMMENTED OUT
    # if 'audio_enabled' not in st.session_state:
    #     st.session_state.audio_enabled = True
    # if 'use_gtts' not in st.session_state:
    #     st.session_state.use_gtts = False
    # if 'speaker_order' not in st.session_state:
    #     st.session_state.speaker_order = None


def load_rag_once():
    """Load RAG database once per session"""
    if not st.session_state.rag_loaded:
        with st.spinner("📚 Loading sacred texts database (4,903 verses)..."):
            load_rag_database()
            st.session_state.rag_loaded = True


# # TTS FUNCTION COMMENTED OUT
# def stream_mentor_response_tts(mentor_name: str, text: str, use_gtts: bool = False) -> str:
#     """
#     Convert mentor response to speech and save as audio file.
#     
#     Args:
#         mentor_name: Name of the mentor (Krishna, Buddha, Jesus)
#         text: Text to convert to speech
#         use_gtts: If True, use gTTS instead of pyttsx3
#     
#     Returns:
#         Path to the generated audio file, or None if TTS fails
#     """
#     # Create temp directory for audio files
#     audio_dir = Path("temp_audio")
#     audio_dir.mkdir(exist_ok=True)
#     
#     # Clean text for TTS (remove HTML tags, special characters)
#     clean_text = html.unescape(text)
#     clean_text = clean_text.replace('\n', '. ')
#     clean_text = clean_text[:500]  # Limit length for TTS
#     
#     timestamp = int(time.time() * 1000)
#     
#     try:
#         # Option 1: Use gTTS (Google TTS) - better quality, requires internet
#         if use_gtts and GTTS_AVAILABLE:
#             audio_filename = audio_dir / f"mentor_{mentor_name}_{timestamp}.mp3"
#             tts = gTTS(text=clean_text, lang='en', slow=False)
#             tts.save(str(audio_filename))
#             return str(audio_filename) if audio_filename.exists() else None
#         
#         # Option 2: Use pyttsx3 (local, zero latency) - primary choice
#         elif PYTTSX3_AVAILABLE:
#             # pyttsx3 saves as .wav by default
#             audio_filename = audio_dir / f"mentor_{mentor_name}_{timestamp}.wav"
#             engine = pyttsx3.init()
#             
#             # Set voice properties for natural speech
#             engine.setProperty('rate', 150)  # Speaking rate (words per minute)
#             engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
#             
#             # Try to set a pleasant voice
#             try:
#                 voices = engine.getProperty('voices')
#                 if voices:
#                     # Prefer female voices if available (often sound more natural)
#                     for voice in voices:
#                         if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
#                             engine.setProperty('voice', voice.id)
#                             break
#                     else:
#                         # Use first available voice
#                         engine.setProperty('voice', voices[0].id)
#             except:
#                 pass  # Use default voice if voice selection fails
#             
#             # Save to file
#             engine.save_to_file(clean_text, str(audio_filename))
#             engine.runAndWait()
#             
#             return str(audio_filename) if audio_filename.exists() else None
#             
#     except Exception as e:
#         st.warning(f"⚠️ TTS generation failed for {mentor_name}: {str(e)}")
#         return None
#     
#     return None


def play_audio_with_pause(audio_file: str, pause_duration: float = 2.0):
    """
    Play audio file and wait for natural pause.
    
    Args:
        audio_file: Path to audio file
        pause_duration: Seconds to pause after audio finishes
    """
    if audio_file and os.path.exists(audio_file):
        time.sleep(pause_duration)


def format_response_with_bullets(text):
    """Format response text to HTML with proper bullet point styling - ensures each bullet is on a new line"""
    if not text:
        return ""
    
    import re
    
    main_bullet_emojis = '✨🌟💡🧘❤️🕉️☸️✝️🎯🔴🟡🟢🆘🌱🚨💫'
    
    # CRITICAL: Split inline bullet points that are in the same paragraph
    # Pattern 1: Split " - Action:" or " - Practice:" that appear after text
    text = re.sub(r'(\S)(\s+-\s+)(Action:|Practice:)', r'\1\n💡 \3', text)
    
    # Pattern 2: Split multiple main bullets in same line (look for "• " that appears mid-sentence)
    text = re.sub(r'([^\n])(\s+)(•\s+)', r'\1\n\3', text)
    
    # Pattern 3: Split when we see "• point - Action:" pattern (all in one line)
    # This handles: "• Point 1 - Action: do this - Practice: do that"
    text = re.sub(r'(•[^•\n]+?)(\s+-\s+)(Action:|Practice:)', r'\1\n💡 \3', text)
    
    # Pattern 4: Split emoji-bullets that appear mid-sentence (but not at line start)
    for emoji in main_bullet_emojis:
        # Split if emoji appears after non-newline character
        text = re.sub(r'([^\n])(\s+)(' + re.escape(emoji) + r'\s)', r'\1\n\3', text)
    
    # Pattern 5: Split when Action/Practice appear without proper line breaks
    # Handle: "text Action: something Practice: something"
    text = re.sub(r'(\S)(\s+)(Action:|Practice:)', r'\1\n💡 \3', text)
    
    # Pattern 6: Split mentor teachings in WISDOM FROM THE MASTERS section
    # Handle: "🕉️ Krishna teaches: ... ☸️ Buddha teaches: ... ✝️ Jesus teaches: ..."
    # Split when one mentor emoji pattern is followed by another mentor emoji
    # More aggressive: split before any mentor emoji that appears after text
    mentor_patterns = [
        (r'([🕉️][^\n🕉️☸️✝️]+?)(\s+)([☸️])', r'\1\n\n\3'),  # Krishna then Buddha
        (r'([🕉️][^\n🕉️☸️✝️]+?)(\s+)([✝️])', r'\1\n\n\3'),  # Krishna then Jesus
        (r'([☸️][^\n🕉️☸️✝️]+?)(\s+)([✝️])', r'\1\n\n\3'),  # Buddha then Jesus
    ]
    for pattern, replacement in mentor_patterns:
        text = re.sub(pattern, replacement, text)
    
    # Also split "teaches:" patterns that might be concatenated
    text = re.sub(r'(\w+ teaches:[^\n]+?)(\s+)([🕉️☸️✝️])', r'\1\n\n\3', text)
    
    # Split text into lines
    lines = text.split('\n')
    html_parts = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue  # Skip empty lines
        
        # FIRST: Handle Action/Practice lines (check these before main bullets)
        if line.startswith('💡') and 'Action:' in line:
            action_text = line.replace('Action:', '').strip().lstrip('💡').strip()
            html_parts.append(f'<div style="margin: 0.5rem 0 0.5rem 3rem; font-size: 1rem; color: #d0d0d0; line-height: 1.7; padding: 0.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 6px; border-left: 2px solid #667eea;">💡 <strong style="color: #FFD700;">Action:</strong> {html.escape(action_text)}</div>')
            continue
        elif line.startswith('📅') and 'Practice:' in line:
            practice_text = line.replace('Practice:', '').strip().lstrip('📅').strip()
            html_parts.append(f'<div style="margin: 0.5rem 0 0.5rem 3rem; font-size: 1rem; color: #d0d0d0; line-height: 1.7; padding: 0.5rem; background: rgba(118, 75, 162, 0.1); border-radius: 6px; border-left: 2px solid #764ba2;">📅 <strong style="color: #FFD700;">Practice:</strong> {html.escape(practice_text)}</div>')
            continue
        elif 'Action:' in line and not line.startswith('•') and line[0] not in main_bullet_emojis:
            # Action line that doesn't start with bullet marker
            if line.startswith('💡'):
                action_text = line.replace('Action:', '').strip().lstrip('💡').strip()
            else:
                action_text = line.replace('Action:', '').strip()
            html_parts.append(f'<div style="margin: 0.5rem 0 0.5rem 3rem; font-size: 1rem; color: #d0d0d0; line-height: 1.7; padding: 0.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 6px; border-left: 2px solid #667eea;">💡 <strong style="color: #FFD700;">Action:</strong> {html.escape(action_text)}</div>')
            continue
        elif 'Practice:' in line and not line.startswith('•') and line[0] not in main_bullet_emojis:
            # Practice line that doesn't start with bullet marker
            if line.startswith('📅'):
                practice_text = line.replace('Practice:', '').strip().lstrip('📅').strip()
            else:
                practice_text = line.replace('Practice:', '').strip()
            html_parts.append(f'<div style="margin: 0.5rem 0 0.5rem 3rem; font-size: 1rem; color: #d0d0d0; line-height: 1.7; padding: 0.5rem; background: rgba(118, 75, 162, 0.1); border-radius: 6px; border-left: 2px solid #764ba2;">📅 <strong style="color: #FFD700;">Practice:</strong> {html.escape(practice_text)}</div>')
            continue
        
        # SECOND: Check if line contains multiple bullet points separated by " - "
        # Look for patterns like "• point1 - Action: action1 - Practice: practice1"
        if ' - ' in line and ('Action:' in line or 'Practice:' in line):
            # Split by " - " followed by Action: or Practice:
            parts = re.split(r'\s+-\s+(?=Action:|Practice:)', line)
            if len(parts) > 1:
                # First part is main bullet
                main_part = parts[0].strip()
                # Remove • if present
                if main_part.startswith('•'):
                    main_part = main_part[1:].strip()
                
                # Display main bullet with emoji
                if main_part:
                    # Check if emoji is already present
                    if main_part and main_part[0] in main_bullet_emojis:
                        html_parts.append(f'<div style="margin: 1.2rem 0 0.6rem 0; font-size: 1.15rem; font-weight: 600; line-height: 1.7; color: #ffffff;">{html.escape(main_part)}</div>')
                    else:
                        html_parts.append(f'<div style="margin: 1.2rem 0 0.6rem 0; font-size: 1.15rem; font-weight: 600; line-height: 1.7; color: #ffffff;">✨ {html.escape(main_part)}</div>')
                
                # Display action/practice sub-bullets
                for part in parts[1:]:
                    part = part.strip()
                    if 'Action:' in part:
                        content = part.replace('Action:', '').strip().lstrip('💡').strip()
                        html_parts.append(f'<div style="margin: 0.5rem 0 0.5rem 3rem; font-size: 1rem; color: #d0d0d0; line-height: 1.7; padding: 0.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 6px; border-left: 2px solid #667eea;">💡 <strong style="color: #FFD700;">Action:</strong> {html.escape(content)}</div>')
                    elif 'Practice:' in part:
                        content = part.replace('Practice:', '').strip().lstrip('📅').strip()
                        html_parts.append(f'<div style="margin: 0.5rem 0 0.5rem 3rem; font-size: 1rem; color: #d0d0d0; line-height: 1.7; padding: 0.5rem; background: rgba(118, 75, 162, 0.1); border-radius: 6px; border-left: 2px solid #764ba2;">📅 <strong style="color: #FFD700;">Practice:</strong> {html.escape(content)}</div>')
                continue
        
        # THIRD: Main bullet points (start with emoji or •)
        if line.startswith('•'):
            content = line[1:].strip()
            # Check if content has emoji at start
            if content and content[0] in main_bullet_emojis:
                html_parts.append(f'<div style="margin: 1.2rem 0 0.6rem 0; font-size: 1.15rem; font-weight: 600; line-height: 1.7; color: #ffffff;">{html.escape(content)}</div>')
            else:
                # Add default emoji
                html_parts.append(f'<div style="margin: 1.2rem 0 0.6rem 0; font-size: 1.15rem; font-weight: 600; line-height: 1.7; color: #ffffff;">✨ {html.escape(content)}</div>')
        elif len(line) > 0 and line[0] in main_bullet_emojis:
            # Main bullet with emoji - larger, bold, with spacing
            html_parts.append(f'<div style="margin: 1.2rem 0 0.6rem 0; font-size: 1.15rem; font-weight: 600; line-height: 1.7; color: #ffffff;">{html.escape(line)}</div>')
        
        # Sub-bullets (start with - or have Action/Practice)
        elif line.startswith('-') or line.startswith('  -') or line.startswith('  💡') or line.startswith('  📅') or line.startswith('  🌱') or line.startswith('  🚨'):
            # Remove leading dashes and spaces
            content = line.lstrip('-').strip()
            if content.startswith('  '):
                content = content[2:]
            
            # Check if it's Action or Practice
            if content.startswith('💡') or 'Action:' in content:
                if 'Action:' in content:
                    action_text = content.replace('Action:', '').strip().lstrip('💡').strip()
                    html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">💡 <strong>Action:</strong> {html.escape(action_text)}</div>')
                else:
                    html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">{html.escape(content)}</div>')
            elif content.startswith('📅') or 'Practice:' in content:
                if 'Practice:' in content:
                    practice_text = content.replace('Practice:', '').strip().lstrip('📅').strip()
                    html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">📅 <strong>Practice:</strong> {html.escape(practice_text)}</div>')
                else:
                    html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">{html.escape(content)}</div>')
            else:
                # Sub-bullet with indentation
                html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">{html.escape(content)}</div>')
        
        # Section headers (TODAY, THIS WEEK, etc.)
        elif line.startswith('🔴') or line.startswith('🟡') or line.startswith('🟢') or line.startswith('🆘'):
            html_parts.append(f'<div style="margin: 1.8rem 0 0.8rem 0; font-size: 1.3rem; font-weight: 700; color: #FFD700; text-transform: uppercase;">{html.escape(line)}</div>')
        
        # Mentor teachings (🕉️, ☸️, ✝️ with "teaches:")
        elif ('🕉️' in line and 'teaches:' in line.lower()) or ('☸️' in line and 'teaches:' in line.lower()) or ('✝️' in line and 'teaches:' in line.lower()):
            # Check if multiple mentor teachings are on same line - split them
            if '🕉️' in line and '☸️' in line:
                # Split Krishna and Buddha
                parts = re.split(r'([☸️])', line, 1)
                if len(parts) > 1:
                    html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(parts[0].strip())}</div>')
                    if len(parts) > 2:
                        html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(parts[1] + parts[2])}</div>')
                else:
                    html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(line)}</div>')
            elif ('🕉️' in line or '☸️' in line) and '✝️' in line:
                # Split first mentor and Jesus
                parts = re.split(r'([✝️])', line, 1)
                if len(parts) > 1:
                    html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(parts[0].strip())}</div>')
                    if len(parts) > 2:
                        html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(parts[1] + parts[2])}</div>')
                else:
                    html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(line)}</div>')
            else:
                # Single mentor teaching
                html_parts.append(f'<div style="margin: 0.8rem 0 0.5rem 0; font-size: 1.1rem; color: #ffffff; line-height: 1.7; padding: 0.5rem 0;">{html.escape(line)}</div>')
        
        # Special sections (YOUR FOCUS, REMEMBER, YOUR SITUATION, WISDOM FROM THE MASTERS)
        elif line.startswith('→') or 'YOUR FOCUS' in line.upper() or 'REMEMBER' in line.upper() or 'YOUR SITUATION' in line.upper() or 'WISDOM FROM' in line.upper() or 'YOUR ACTION PLAN' in line.upper():
            html_parts.append(f'<div style="margin: 1.5rem 0 0.6rem 0; font-size: 1.2rem; font-weight: 700; color: #FFD700;">{html.escape(line)}</div>')
        
        # Regular text
        else:
            # Check if it contains Action: or Practice: inline
            if 'Action:' in line or 'Practice:' in line:
                # Try to split it
                if 'Action:' in line:
                    parts = line.split('Action:', 1)
                    if parts[0].strip():
                        html_parts.append(f'<div style="margin: 0.5rem 0; line-height: 1.6; color: #e0e0e0;">{html.escape(parts[0].strip())}</div>')
                    if len(parts) > 1 and parts[1].strip():
                        html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">💡 <strong>Action:</strong> {html.escape(parts[1].strip())}</div>')
                elif 'Practice:' in line:
                    parts = line.split('Practice:', 1)
                    if parts[0].strip():
                        html_parts.append(f'<div style="margin: 0.5rem 0; line-height: 1.6; color: #e0e0e0;">{html.escape(parts[0].strip())}</div>')
                    if len(parts) > 1 and parts[1].strip():
                        html_parts.append(f'<div style="margin: 0.4rem 0 0.4rem 2.5rem; font-size: 1rem; color: #d0d0d0; line-height: 1.6;">📅 <strong>Practice:</strong> {html.escape(parts[1].strip())}</div>')
            else:
                html_parts.append(f'<div style="margin: 0.5rem 0; line-height: 1.6; color: #e0e0e0;">{html.escape(line)}</div>')
    
    return ''.join(html_parts)


def format_bullet_points(text):
    """Format bullet points with proper line breaks and styling - makes them visually attractive"""
    lines = text.split('\n')
    formatted_lines = []
    
    # Emojis that indicate main bullet points
    main_bullet_emojis = '✨🌟💡🧘❤️🕉️☸️✝️🎯🔴🟡🟢🆘🌱🚨💫'
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.strip()
        
        if not line:
            formatted_lines.append('')  # Preserve empty lines
            continue
        
        # Check if it's a main bullet point (starts with emoji or •)
        is_main_bullet = (line.startswith('•') or 
                         (len(line) > 0 and line[0] in main_bullet_emojis) or
                         line.startswith('🔴') or line.startswith('🟡') or 
                         line.startswith('🟢') or line.startswith('🆘'))
        
        if is_main_bullet:
            # Main bullet point - ensure it's on its own line with spacing
            if i > 0 and formatted_lines and formatted_lines[-1].strip():
                formatted_lines.append('')  # Add blank line before main bullet
            formatted_lines.append(line)
        elif line.startswith('-') or line.startswith('  -') or line.startswith('  💡') or line.startswith('  📅') or line.startswith('  🌱') or line.startswith('  🚨'):
            # Sub-bullet point - keep indentation
            formatted_lines.append(line)
        elif line.startswith('→') or line.startswith('YOUR FOCUS') or line.startswith('REMEMBER'):
            # Special sections - add spacing
            if formatted_lines and formatted_lines[-1].strip():
                formatted_lines.append('')
            formatted_lines.append(line)
        else:
            # Regular text
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


def parse_mentor_response(response_text):
    """Parse mentor response to extract principle, bullets, steps, and timeline"""
    import re
    
    lines = response_text.split('\n')
    principle = ""
    bullets = []
    steps = []
    timeline = {'start': 'Today', 'duration': 'Ongoing', 'review': 'Weekly'}
    
    # Collect all meaningful lines
    meaningful_lines = []
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
        meaningful_lines.append(line)
    
    # Extract principle from first main bullet point (starts with emoji like ✨, 🧘, ❤️)
    main_bullet_emojis = ['✨', '🌟', '🧘', '❤️', '🕉️', '☸️', '✝️', '💡', '🎯']
    for line in meaningful_lines:
        # Check if this is a main bullet point (starts with emoji)
        if line and len(line) > 0 and line[0] in main_bullet_emojis:
            # Extract principle from main bullet
            principle = re.sub(r'^[✨🌟💡🧘❤️🕉️☸️✝️🎯🔴🟡🟢🆘🌱🚨💫•\s-]+', '', line)
            principle = re.sub(r'\*\*([^*]+)\*\*', r'\1', principle)
            # Remove Action/Practice labels if present
            principle = re.sub(r'(Action:|Practice:)\s*', '', principle, flags=re.IGNORECASE)
            # Remove common prefixes
            principle = re.sub(r'^(As I|I say|Krishna|Buddha|Jesus|My friend|My child|Listen|Remember|You speak|I appreciate|I add)[,\s]+', '', principle, flags=re.IGNORECASE)
            # Remove " - " patterns (e.g., "point - explanation")
            principle = re.sub(r'\s+-\s+.*$', '', principle)
            # Clean up extra spaces
            principle = ' '.join(principle.split())
            # Capitalize first letter
            if principle:
                principle = principle[0].upper() + principle[1:] if len(principle) > 1 else principle.upper()
            # Extract first sentence or limit to 200 chars for better display
            if '.' in principle:
                sentences = principle.split('.')
                if len(sentences[0]) < 200:
                    principle = sentences[0] + '.'
                else:
                    principle = principle[:200].rsplit(' ', 1)[0] + '...'
            else:
                # No period found, limit to 200 chars
                if len(principle) > 200:
                    principle = principle[:200].rsplit(' ', 1)[0] + '...'
            break
    
    # Extract Action and Practice lines (💡 Action: and 📅 Practice:)
    for line in meaningful_lines:
        line_lower = line.lower().strip()
        
        # Check for Action lines (💡 Action:)
        if '💡' in line and 'action:' in line_lower:
            action_text = re.sub(r'^[💡\s]+', '', line, flags=re.IGNORECASE)
            action_text = re.sub(r'Action:\s*', '', action_text, flags=re.IGNORECASE)
            action_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', action_text)
            action_text = ' '.join(action_text.split())
            if action_text and len(action_text) > 10 and len(steps) < 3:
                action_text = action_text[0].upper() + action_text[1:] if len(action_text) > 1 else action_text.upper()
                steps.append(action_text[:200])
        
        # Check for Practice lines (📅 Practice:)
        elif '📅' in line and 'practice:' in line_lower:
            practice_text = re.sub(r'^[📅\s]+', '', line, flags=re.IGNORECASE)
            practice_text = re.sub(r'Practice:\s*', '', practice_text, flags=re.IGNORECASE)
            practice_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', practice_text)
            practice_text = ' '.join(practice_text.split())
            if practice_text and len(practice_text) > 10 and len(steps) < 3:
                practice_text = practice_text[0].upper() + practice_text[1:] if len(practice_text) > 1 else practice_text.upper()
                steps.append(practice_text[:200])
        
        # Extract main bullet points (explanations) - lines starting with emoji but not Action/Practice
        elif line and len(line) > 0 and line[0] in main_bullet_emojis and 'action:' not in line_lower and 'practice:' not in line_lower:
            bullet_text = re.sub(r'^[✨🌟💡🧘❤️🕉️☸️✝️🎯🔴🟡🟢🆘🌱🚨💫•\s-]+', '', line)
            bullet_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', bullet_text)
            # Remove " - " patterns
            bullet_text = re.sub(r'\s+-\s+.*$', '', bullet_text)
            bullet_text = ' '.join(bullet_text.split())
            # Skip if it's the same as principle or too short
            if bullet_text and len(bullet_text) > 20 and bullet_text[:50] != principle[:50] and len(bullets) < 3:
                bullet_text = bullet_text[0].upper() + bullet_text[1:] if len(bullet_text) > 1 else bullet_text.upper()
                bullets.append(bullet_text[:200])
    
    # If we don't have enough steps, look for any remaining actionable lines
    if len(steps) < 2:
        for line in meaningful_lines:
            if len(steps) >= 3:
                break
            line_lower = line.lower()
            # Skip if already used or if it's clearly a main bullet
            if line and len(line) > 0 and line[0] in main_bullet_emojis:
                continue
            if 'action:' in line_lower or 'practice:' in line_lower:
                continue
            
            # Look for actionable content
            action_words = ['begin', 'start', 'establish', 'practice', 'try', 'do', 'take', 'set', 'create']
            if any(word in line_lower[:30] for word in action_words):
                cleaned = re.sub(r'^[✨🌟💡🧘❤️🕉️☸️✝️🎯🔴🟡🟢🆘🌱🚨💫•\s-]+', '', line)
                cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
                cleaned = ' '.join(cleaned.split())
                if cleaned and len(cleaned) > 15 and cleaned not in [s[:50] for s in steps]:
                    cleaned = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()
                    steps.append(cleaned[:200])
    
    # If we don't have enough bullets, extract from other main points
    if len(bullets) < 2:
        for line in meaningful_lines:
            if len(bullets) >= 3:
                break
            if line and len(line) > 0 and line[0] in main_bullet_emojis:
                bullet_text = re.sub(r'^[✨🌟💡🧘❤️🕉️☸️✝️🎯🔴🟡🟢🆘🌱🚨💫•\s-]+', '', line)
                bullet_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', bullet_text)
                bullet_text = re.sub(r'\s+-\s+.*$', '', bullet_text)
                bullet_text = ' '.join(bullet_text.split())
                # Skip if it's the same as principle or already in bullets
                if bullet_text and len(bullet_text) > 20 and bullet_text[:50] != principle[:50]:
                    if bullet_text not in [b[:50] for b in bullets]:
                        bullet_text = bullet_text[0].upper() + bullet_text[1:] if len(bullet_text) > 1 else bullet_text.upper()
                        bullets.append(bullet_text[:200])
    
    # If still no bullets, use contextual information
    if len(bullets) < 2:
        if principle:
            bullets.append("This teaching directly addresses your situation")
            bullets.append("It offers a practical path forward")
        else:
            bullets.append("This wisdom addresses your core challenge")
            bullets.append("It connects deeply with your personal journey")
    
    # Extract timeline information
    timeline_text = response_text.lower()
    if 'today' in timeline_text or 'now' in timeline_text or 'immediate' in timeline_text:
        timeline['start'] = 'Today'
    elif 'this week' in timeline_text:
        timeline['start'] = 'This week'
    
    if 'daily' in timeline_text:
        timeline['duration'] = 'Daily practice'
        timeline['review'] = 'Daily'
    elif 'weekly' in timeline_text:
        timeline['duration'] = 'Weekly practice'
        timeline['review'] = 'Weekly'
    elif 'week' in timeline_text:
        timeline['duration'] = 'This week'
        timeline['review'] = 'Weekly'
    
    # Fallback: ensure we have content
    if not principle or len(principle) < 10:
        principle = "Applying timeless wisdom to your situation"
    
    if not bullets:
        bullets = [
            "This wisdom addresses the core of your challenge",
            "It offers a path forward that honors your journey"
        ]
    
    if not steps:
        steps = [
            "Begin with small, intentional actions today",
            "Establish a consistent daily practice",
            "Review and adjust weekly"
        ]
    
    return {
        'principle': principle,
        'bullets': bullets[:3],
        'steps': steps[:3],
        'timeline': timeline
    }


def display_mentor_response(response_data, mentor_color):
    """Display mentor response in simple, conversational format"""
    mentor = response_data['mentor']
    icon = response_data['icon']
    response = response_data['response']
    
    # Get citations
    citations = response_data.get('citations', response_data.get('verses', []))
    
    # Get scripture name
    scripture_names = {
        'krishna': 'Bhagavad Gita',
        'buddha': 'Dhammapada',
        'jesus': 'Gospels'
    }
    scripture_name = scripture_names.get(mentor.lower(), 'Sacred Text')
    
    # Display header with styling
    st.markdown(
        f'<div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); '
        f'border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;">'
        f'<h2 style="margin: 0 0 1rem 0; font-size: 1.5rem; color: #ffffff; font-weight: 600; border-bottom: 2px solid rgba(255, 255, 255, 0.2); padding-bottom: 0.5rem;">{icon} {mentor.upper()}\'S WISDOM</h2>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Display response text directly (wisdom paragraphs)
    st.markdown(response)
    
    # Show citations in expander
    if citations and len(citations) > 0:
        with st.expander(f"📖 {mentor}'s Sacred Source: {scripture_name} ({len(citations)} verses)"):
            for cite in citations:
                reference = cite.get('reference', 'Unknown')
                source = cite.get('source', scripture_name)
                verse_text = cite.get('text', '')
                
                st.markdown(f"**{reference}** - {source}")
                if verse_text:
                    display_text = verse_text[:300] + "..." if len(verse_text) > 300 else verse_text
                    st.info(display_text)
                if cite != citations[-1]:  # Don't add divider after last item
                    st.divider()
    else:
        with st.expander(f"📖 {mentor}'s Sacred Source: {scripture_name}"):
            st.info("No citations available for this response.")


def display_synthesis(synthesis_text):
    """Display the synthesis with enhanced styling"""
    # Escape HTML in synthesis text to prevent injection and display issues
    escaped_synthesis = html.escape(synthesis_text)
    # Convert line breaks to <br> for HTML display
    escaped_synthesis = escaped_synthesis.replace('\n', '<br>')
    
    st.markdown(f"""
    <div class="synthesis-card">
        <h1 style="margin-bottom: 1rem;">🌟 Synthesized Wisdom Across Traditions</h1>
        <p style="font-size: 1.3rem; line-height: 2; margin: 1.5rem 0;">{escaped_synthesis}</p>
        <p style="font-size: 0.95rem; opacity: 0.9; margin-top: 1.5rem;">
            ✨ This wisdom integrates insights from all three spiritual traditions ✨
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_moderator_answer(moderator_text):
    """Display the moderator's final answer with bullet format - synthesizes all three mentor responses"""
    # Format response to HTML with proper bullet styling
    formatted_html = format_response_with_bullets(moderator_text)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2.5rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 8px 16px rgba(0,0,0,0.2);">
        <h1 style="text-align: center; margin-bottom: 1.5rem; font-size: 2rem;">✨ Moderator's Synthesis</h1>
        <p style="text-align: center; font-size: 1rem; opacity: 0.9; margin-bottom: 1.5rem; font-style: italic;">
            Integrating wisdom from Krishna, Buddha, and Jesus based on your personal context
        </p>
        <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #FFD700; color: white;">
            {formatted_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def export_dialogue_text(question, responses, synthesis):
    """Export dialogue as formatted text"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🎭 DIVINE DIALOGUE                            ║
║              Multi-Perspective Spiritual Discussion                  ║
╚══════════════════════════════════════════════════════════════════╝

Date: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR QUESTION:
{question}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for response in responses:
        text += f"""
{response['icon']} {response['mentor'].upper()}:
{response['response']}

Referenced Verses:
"""
        for verse in response['verses'][:3]:
            text += f"  • {verse['reference']} (Similarity: {verse['similarity']:.1%})\n"
            text += f"    {verse['text'][:200]}...\n\n"
        
        text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    text += f"""
🌟 SYNTHESIZED WISDOM ACROSS TRADITIONS:
{synthesis}

✨ This wisdom integrates insights from all three spiritual traditions ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated by Divine Dialogue - Multi-Agent Spiritual Wisdom System
Powered by LangGraph, FAISS, and OpenRouter AI
"""
    
    return text


def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🎭 Divine Dialogue</h1>
        <h2 style="font-size: 1.5rem; font-weight: 300; margin-bottom: 1rem;">
            A Multi-Perspective Spiritual Debate
        </h2>
        <p style="font-size: 1.1rem; opacity: 0.95; max-width: 800px; margin: 0 auto;">
            Ask any spiritual question and receive wisdom from three enlightened masters:
            Krishna (🕉️), Buddha (☸️), and Jesus (✝️). Each mentor retrieves relevant 
            teachings from their sacred texts and engages in thoughtful dialogue.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About Divine Dialogue")
        st.markdown("""
        This system orchestrates conversations between three spiritual masters:
        
        - **🕉️ Krishna** - Bhagavad Gita (701 verses)
        - **☸️ Buddha** - Dhammapada (423 verses)
        - **✝️ Jesus** - Gospels (3,779 verses)
        
        Each mentor uses AI-powered semantic search to retrieve relevant teachings 
        from their sacred texts before responding.
        """)
        
        st.divider()
        
        # # TTS AUDIO SETTINGS COMMENTED OUT
        # st.header("🔊 Audio Settings")
        # audio_enabled = st.checkbox(
        #     "Enable Text-to-Speech", 
        #     value=st.session_state.audio_enabled,
        #     help="Play mentor responses as audio with natural pauses"
        # )
        # st.session_state.audio_enabled = audio_enabled
        # 
        # if not audio_enabled:
        #     # If audio is disabled, also disable gTTS
        #     st.session_state.use_gtts = False
        # 
        # if audio_enabled:
        #     use_gtts = st.checkbox(
        #         "Use Google TTS (Better Quality)", 
        #         value=st.session_state.get('use_gtts', False),
        #         help="Uses Google TTS for better voice quality (requires internet)"
        #     )
        #     st.session_state.use_gtts = use_gtts
        #     st.info("💡 Audio will play automatically as mentors speak")
        #     
        #     # TTS Status
        #     st.caption("**TTS Engine Status:**")
        #     if PYTTSX3_AVAILABLE:
        #         st.success("✅ pyttsx3 (Local) Available")
        #     else:
        #         st.warning("⚠️ pyttsx3 not installed")
        #     
        #     if GTTS_AVAILABLE:
        #         st.success("✅ gTTS (Google) Available")
        #     else:
        #         st.info("ℹ️ gTTS not installed")
        #     
        #     if not PYTTSX3_AVAILABLE and not GTTS_AVAILABLE:
        #         st.error("❌ No TTS engine available")
        #         st.caption("Install: `pip install pyttsx3` or `pip install gtts`")
        # 
        # st.divider()
        
        st.header("🎯 Sample Questions")
        sample_questions = [
            "How can I find inner peace?",
            "What is the purpose of life?",
            "How should I treat my enemies?",
            "What happens after death?",
            "How do I overcome suffering?",
            "What is true love?",
            "How can I be a better person?",
            "What is the nature of the soul?",
            "How do I find happiness?",
            "What is wisdom?"
        ]
        
        for q in sample_questions:
            if st.button(q, key=f"sample_{q}", use_container_width=True):
                st.session_state.selected_question = q
                st.rerun()
        
        st.divider()
        
        st.header("📊 System Statistics")
        st.metric("Total Sacred Verses", "4,903")
        st.metric("Spiritual Traditions", "3")
        st.metric("Vector Database", "FAISS")
        st.metric("Embedding Model", "all-MiniLM-L6-v2")
        
        st.divider()
        
        if st.button("🔄 Clear All History", use_container_width=True):
            st.session_state.dialogue_history = []
            st.session_state.current_dialogue = None
            st.session_state.last_result = None
            st.session_state.displayed_question = None
            st.session_state.speaker_order = None
            st.success("History cleared!")
            st.rerun()
    
    # Main content area
    st.header("💭 Ask Your Spiritual Question")
    
    # Check if a sample question was selected
    default_question = st.session_state.get('selected_question', '')
    if 'selected_question' in st.session_state:
        del st.session_state.selected_question
    
    # Voice input JavaScript component
    voice_input_js = """
    <script>
    (function() {
        // Speech Recognition setup
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech Recognition not supported in this browser');
            return;
        }
        
        let recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        let currentTextarea = null;
        let currentButton = null;
        let accumulatedText = '';
        
        function findTextarea(key) {
            // Wait for DOM to be ready and find textarea by key
            const allTextareas = Array.from(document.querySelectorAll('textarea'));
            
            // Try to find by data-testid first
            let textareas = Array.from(document.querySelectorAll('textarea[data-testid*="textarea"]'));
            
            if (key === 'question') {
                // First textarea is the question - find it by looking for the one near mic-question button
                const micButton = document.getElementById('mic-question');
                if (micButton) {
                    // Find the textarea in the same column or nearby
                    let parent = micButton.closest('[data-testid*="column"]') || micButton.parentElement;
                    while (parent && parent !== document.body) {
                        const nearbyTextarea = parent.querySelector('textarea');
                        if (nearbyTextarea) {
                            return nearbyTextarea;
                        }
                        parent = parent.previousElementSibling || parent.parentElement;
                    }
                }
                return textareas[0] || allTextareas[0];
            } else if (key === 'background') {
                // Second textarea is the background - find it by looking for the one near mic-background button
                const micButton = document.getElementById('mic-background');
                if (micButton) {
                    // Find the textarea in the same column or nearby
                    let parent = micButton.closest('[data-testid*="column"]') || micButton.parentElement;
                    while (parent && parent !== document.body) {
                        const nearbyTextarea = parent.querySelector('textarea');
                        if (nearbyTextarea) {
                            return nearbyTextarea;
                        }
                        parent = parent.previousElementSibling || parent.parentElement;
                    }
                }
                return textareas[1] || allTextareas[1];
            }
            return null;
        }
        
        function updateTextarea(textarea, text) {
            if (!textarea) return;
            
            const currentValue = textarea.value || '';
            const newValue = currentValue + text;
            textarea.value = newValue;
            
            // Trigger multiple events to ensure Streamlit picks it up
            const events = ['input', 'change', 'keyup', 'blur'];
            events.forEach(eventType => {
                const event = new Event(eventType, { bubbles: true, cancelable: true });
                textarea.dispatchEvent(event);
            });
            
            // Try React/Streamlit specific updates
            try {
                const descriptor = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value');
                if (descriptor && descriptor.set) {
                    descriptor.set.call(textarea, newValue);
                }
            } catch (e) {
                // Fallback if property descriptor access fails
                console.log('Using fallback textarea update');
            }
            
            // Trigger React onChange if available
            try {
                const reactEvent = new Event('input', { bubbles: true });
                Object.defineProperty(reactEvent, 'target', { value: textarea, enumerable: true });
                textarea.dispatchEvent(reactEvent);
            } catch (e) {
                // Fallback if React event creation fails
                console.log('Using fallback event dispatch');
            }
        }
        
        recognition.onresult = function(event) {
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                }
            }
            
            if (finalTranscript && currentTextarea) {
                accumulatedText += finalTranscript;
                updateTextarea(currentTextarea, finalTranscript);
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            if (event.error === 'no-speech') {
                // Auto-restart if still active
                if (currentButton && currentButton.classList.contains('mic-button-active')) {
                    setTimeout(() => {
                        if (currentButton.classList.contains('mic-button-active')) {
                            recognition.start();
                        }
                    }, 500);
                }
            } else if (event.error === 'not-allowed') {
                alert('Microphone access denied. Please allow microphone access in your browser settings.');
                if (currentButton) {
                    currentButton.classList.remove('mic-button-active');
                    currentButton.innerHTML = '🎤';
                    currentButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                }
            }
        };
        
        recognition.onend = function() {
            // Auto-restart if button is still active
            if (currentButton && currentButton.classList.contains('mic-button-active')) {
                setTimeout(() => {
                    if (currentButton.classList.contains('mic-button-active')) {
                        recognition.start();
                    }
                }, 100);
            }
        };
        
        // Handle microphone button clicks
        window.startVoiceInput = function(key, buttonId) {
            const button = document.getElementById(buttonId);
            if (!button) return;
            
            if (button.classList.contains('mic-button-active')) {
                // Stop recording
                recognition.stop();
                button.classList.remove('mic-button-active');
                button.innerHTML = '🎤';
                button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                currentTextarea = null;
                currentButton = null;
                accumulatedText = '';
            } else {
                // Stop any other active recording
                const activeButtons = document.querySelectorAll('.mic-button-active');
                activeButtons.forEach(btn => {
                    btn.classList.remove('mic-button-active');
                    btn.innerHTML = '🎤';
                    btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                });
                
                // Start recording - wait a bit for DOM to be ready
                setTimeout(() => {
                    currentTextarea = findTextarea(key);
                    currentButton = button;
                    accumulatedText = '';
                    
                    if (currentTextarea) {
                        recognition.start();
                        button.classList.add('mic-button-active');
                        button.innerHTML = '🔴';
                        button.style.background = '#ff4444';
                    } else {
                        console.error('Could not find textarea for key:', key);
                        alert('Could not find text input field. Please refresh the page.');
                    }
                }, 100);
            }
        };
        
        // Initialize on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Voice input ready');
            });
        } else {
            console.log('Voice input ready');
        }
    })();
    </script>
    
    <style>
    .mic-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        font-size: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        margin-left: 8px;
        vertical-align: middle;
    }
    .mic-button:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
    }
    .mic-button-active {
        background: #ff4444 !important;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .voice-input-container {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
    """
    st.markdown(voice_input_js, unsafe_allow_html=True)
    
    # User input - Question with voice input
    col_question, col_mic1 = st.columns([10, 1])
    with col_question:
        user_question = st.text_area(
            "Enter your question:",
            value=default_question,
            height=120,
            placeholder="Ask any spiritual question... (e.g., How can I find inner peace in times of suffering?)",
            help="Ask about life purpose, inner peace, relationships, suffering, wisdom, or any spiritual topic. Click the 🎤 button to use voice input.",
            key="question_textarea"
        )
    
    with col_mic1:
        st.markdown("<br>", unsafe_allow_html=True)  # Align button
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <button id="mic-question" class="mic-button" onclick="startVoiceInput('question', 'mic-question')" title="Click to start/stop voice input">
                🎤
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # User input - Background (NEW) with voice input
    st.write("### 📋 About You (This helps personalize the response)")
    col_background, col_mic2 = st.columns([10, 1])
    with col_background:
        user_background = st.text_area(
            "Tell us about yourself:",
            height=150,
            placeholder="E.g., I'm an M.Tech student at IIT struggling with anxiety. My family expects high grades, but I'm feeling overwhelmed by coursework. I value honesty and hard work, but I'm losing motivation...",
            help="Share your current situation, challenges, work/study context, personality, or values. This helps the mentors provide more relevant, personalized guidance. (200-300 words recommended). Click the 🎤 button to use voice input.",
            key="background_textarea"
        )
    
    with col_mic2:
        st.markdown("<br>", unsafe_allow_html=True)  # Align button
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <button id="mic-background" class="mic-button" onclick="startVoiceInput('background', 'mic-background')" title="Click to start/stop voice input">
                🎤
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        begin_button = st.button("🔥 Begin Divine Dialogue", type="primary", use_container_width=True)
    
    with col2:
        if st.button("❌ Clear", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.session_state.current_dialogue:
            if st.button("💾 Save", use_container_width=True):
                st.session_state.dialogue_history.append(st.session_state.current_dialogue)
                st.success("Saved!")
    
    # Process question
    if begin_button and user_question.strip():
        # Only run if this is a new question
        if st.session_state.displayed_question != user_question:
            # Clear previous results to prevent duplication
            st.session_state.last_result = None
            
            # Load RAG database
            load_rag_once()
            
            # Display question with dark background
            st.markdown(f"""
            <div class="question-display">
                <h3 style="color: #ffffff;">📝 Your Question:</h3>
                <p style="font-size: 1.2rem; font-style: italic; color: #e0e0e0;">"{user_question}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Run the dialogue with spinner
            with st.spinner("🌟 The mentors are considering your question... This may take 15-30 seconds..."):
                try:
                    # Pass user_background to the dialogue function
                    result = run_divine_dialogue(user_question, user_background=user_background.strip() if user_background else '')
                    
                    if 'error' not in result:
                        # Store result and mark question as displayed
                        st.session_state.last_result = result
                        st.session_state.displayed_question = user_question
                        st.session_state.user_background_stored = user_background.strip() if user_background else ''
                        
                        # Build comprehensive conversation history for follow-ups
                        conversation_history = []
                        conversation_history.append(f"User Question: {user_question}")
                        # Store initial responses
                        for response in result['mentor_responses']:
                            mentor_name = response['mentor']
                            mentor_response = response['response']
                            conversation_history.append(f"{mentor_name}: {mentor_response}")
                            # Store in initial_responses for reference
                            st.session_state.initial_responses[mentor_name] = {
                                'response': mentor_response,
                                'citations': response.get('citations', [])
                            }
                        conversation_history.append(f"Moderator: {result['synthesis']}")
                        st.session_state.conversation_history = conversation_history
                        
                        # Clear follow-up state
                        st.session_state.selected_mentor = None
                        st.session_state.follow_up_responses = []
                        
                        st.rerun()  # Rerun to display results cleanly
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.exception(e)
        
    # Display results if available
    if st.session_state.last_result and st.session_state.displayed_question:
        result = st.session_state.last_result
        
        st.markdown(f"""
        <div class="question-display">
            <h3 style="color: #ffffff;">📝 Your Question:</h3>
            <p style="font-size: 1.2rem; font-style: italic; color: #e0e0e0;">"{st.session_state.displayed_question}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ Divine Dialogue Complete!")
        
        st.divider()
        
        # Display mentor responses
        st.header("💬 The Mentors Speak")
        
        mentor_colors = {
            'Krishna': '#FFD700',
            'Buddha': '#4A90E2',
            'Jesus': '#E6E6FA'
        }
        
        mentor_emojis = {
            'Krishna': '🕉️',
            'Buddha': '☸️',
            'Jesus': '✝️'
        }
        
        # Get mentor responses in FIXED ORDER: Krishna → Buddha → Jesus (no randomization)
        mentor_responses = result['mentor_responses'].copy()
        
        # Remove duplicates (ensure unique mentors)
        seen_mentors = {}
        for response in mentor_responses:
            mentor_name = response.get('mentor', 'Unknown')
            if mentor_name not in seen_mentors:
                seen_mentors[mentor_name] = response
        
        # Enforce FIXED ORDER: Krishna → Buddha → Jesus
        fixed_order = ['Krishna', 'Buddha', 'Jesus']
        ordered_responses = []
        for mentor_name in fixed_order:
            if mentor_name in seen_mentors:
                ordered_responses.append(seen_mentors[mentor_name])
        
        mentor_responses = ordered_responses
        
        # # TTS FUNCTIONALITY COMMENTED OUT
        # # Generate all audio files first (before display)
        # audio_files = {}
        # if st.session_state.audio_enabled:
        #     with st.spinner("🎤 Generating audio for all mentors..."):
        #         for response in mentor_responses:
        #             mentor_name = response.get('mentor', 'Unknown')
        #             response_text = response.get('response', '')
        #             if response_text:
        #                 try:
        #                     audio_file = stream_mentor_response_tts(
        #                         mentor_name, 
        #                         response_text, 
        #                         use_gtts=st.session_state.get('use_gtts', False)
        #                     )
        #                     if audio_file and os.path.exists(audio_file):
        #                         audio_files[mentor_name] = audio_file
        #                 except Exception as e:
        #                     st.warning(f"⚠️ Audio generation failed for {mentor_name}: {str(e)}")
        
        # Display mentor responses in FIXED ORDER
        st.markdown("### 🎭 Divine Dialogue Begins...")
        st.markdown("---")
        
        # Display each mentor's response (TTS commented out)
        for i, response in enumerate(mentor_responses):
            mentor_name = response.get('mentor', 'Unknown')
            response_text = response.get('response', '')
            icon = mentor_emojis.get(mentor_name, '✨')
            
            # Create container for this mentor's response
            with st.container():
                # Display mentor header
                st.markdown(f"#### {icon} {mentor_name} speaks:")
                
                # # TTS AUDIO PLAYER COMMENTED OUT
                # # Display audio player if enabled
                # if st.session_state.audio_enabled and mentor_name in audio_files:
                #     audio_file = audio_files[mentor_name]
                #     audio_format = "audio/wav" if audio_file.endswith('.wav') else "audio/mp3"
                #     
                #     # Display audio with autoplay for first one
                #     st.audio(audio_file, format=audio_format, autoplay=(i == 0))
                #     
                #     # Show status
                #     if i == 0:
                #         st.success("🔊 **Auto-playing now...**")
                #     else:
                #         st.info(f"🔊 **Queued:** Plays automatically after previous speaker")
                
                # Display response text (shows immediately) - bullet points are handled in display_mentor_response
                display_mentor_response(response, mentor_colors.get(mentor_name, '#FFFFFF'))
                
                # Citations are now handled inside display_mentor_response function (single dropdown)
                
                # Natural pause between speakers
                if i < len(mentor_responses) - 1:
                    st.markdown("---")
                    st.markdown("")
        
        # # TTS JAVASCRIPT COMMENTED OUT
        # # Add JavaScript for sequential playback AFTER all audio widgets are rendered
        # if st.session_state.audio_enabled and len(audio_files) > 1:
        #     num_audios = len([r for r in mentor_responses if r.get('mentor') in audio_files])
        #     if num_audios > 1:
        #         # Simplified JavaScript that works with Streamlit's audio elements
        #         js_sequential = f"""
        #         <script>
        #         (function() {{
        #             function setupSequentialPlayback() {{
        #                 // Find all audio elements (Streamlit creates them)
        #                 const allAudios = Array.from(document.querySelectorAll('audio'));
        #                 // Filter to only get audio elements that are visible (not hidden)
        #                 const visibleAudios = allAudios.filter(function(audio) {{
        #                     return audio.offsetParent !== null;
        #                 }});
        #                 
        #                 if (visibleAudios.length >= {num_audios}) {{
        #                     // Setup sequential playback with proper closure
        #                     for (let idx = 0; idx < visibleAudios.length - 1; idx++) {{
        #                         (function(currentIdx) {{
        #                             const currentAudio = visibleAudios[currentIdx];
        #                             const nextAudio = visibleAudios[currentIdx + 1];
        #                             
        #                             if (currentAudio && nextAudio) {{
        #                                 currentAudio.addEventListener('ended', function() {{
        #                                     setTimeout(function() {{
        #                                         nextAudio.play().catch(function(err) {{
        #                                             console.log('Autoplay prevented for audio', currentIdx + 1);
        #                                         }});
        #                                     }}, 1500);
        #                                 }}, false);
        #                             }}
        #                         }})(idx);
        #                     }}
        #                     return true;
        #                 }}
        #                 return false;
        #             }}
        #             
        #             // Try to setup immediately
        #             if (!setupSequentialPlayback()) {{
        #                 // If not ready, try again after a delay
        #                 var attempts = 0;
        #                 var interval = setInterval(function() {{
        #                     attempts++;
        #                     if (setupSequentialPlayback() || attempts > 10) {{
        #                         clearInterval(interval);
        #                     }}
        #                 }}, 500);
        #             }}
        #         }})();
        #         </script>
        #         """
        #         st.markdown(js_sequential, unsafe_allow_html=True)
        
        st.divider()
        
        # Display Moderator's Synthesis (combines all three mentor responses with personal context)
        display_moderator_answer(result['synthesis'])
        
        st.divider()
        
        # Action buttons
        st.header("📥 Export & Share")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download dialogue
            dialogue_text = export_dialogue_text(
                st.session_state.displayed_question,
                result['mentor_responses'],
                result['synthesis']
            )
            st.download_button(
                label="📄 Download as Text",
                data=dialogue_text,
                file_name=f"divine_dialogue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Copy to clipboard (simulated with text area)
            if st.button("📋 Copy Summary", use_container_width=True, key="copy_summary"):
                summary = f"Q: {st.session_state.displayed_question}\n\nSynthesis: {result['synthesis']}"
                st.code(summary, language=None)
                st.info("Copy the text above!")
        
        with col3:
            # Save to history
            if st.button("💾 Save to History", use_container_width=True, key="save_history"):
                st.session_state.dialogue_history.append({
                    'question': st.session_state.displayed_question,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'responses': result['mentor_responses'],
                    'synthesis': result['synthesis']
                })
                st.success("Saved to history!")
        
        # Store current dialogue
        st.session_state.current_dialogue = {
            'question': st.session_state.displayed_question,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'responses': result['mentor_responses'],
            'synthesis': result['synthesis']
        }
        
        # Follow-up section
        st.divider()
        st.header("🔄 Follow-Up Questions")
        st.write("Ask any of the mentors a follow-up question about their guidance or your situation.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("❓ Ask Krishna 🕉️", use_container_width=True, key="ask_krishna"):
                st.session_state.selected_mentor = "Krishna"
                st.rerun()
        
        with col2:
            if st.button("❓ Ask Buddha ☸️", use_container_width=True, key="ask_buddha"):
                st.session_state.selected_mentor = "Buddha"
                st.rerun()
        
        with col3:
            if st.button("❓ Ask Jesus ✝️", use_container_width=True, key="ask_jesus"):
                st.session_state.selected_mentor = "Jesus"
                st.rerun()
        
        # Display follow-up question input if mentor is selected
        if st.session_state.selected_mentor:
            mentor_icon = {'Krishna': '🕉️', 'Buddha': '☸️', 'Jesus': '✝️'}.get(st.session_state.selected_mentor, '✨')
            st.write(f"### {mentor_icon} Your question for {st.session_state.selected_mentor}:")
            
            follow_up_question = st.text_input(
                f"Ask {st.session_state.selected_mentor}:",
                key="follow_up_input",
                placeholder=f"E.g., Can you explain more about what you meant by...?",
                label_visibility="collapsed"
            )
            
            col_submit, col_cancel = st.columns([3, 1])
            with col_submit:
                if st.button("💬 Ask", use_container_width=True, key="submit_follow_up"):
                    if follow_up_question.strip():
                        # Call follow-up function
                        with st.spinner(f"🌟 {st.session_state.selected_mentor} is considering your question..."):
                            try:
                                follow_up_result = run_follow_up(
                                    question=follow_up_question.strip(),
                                    mentor_name=st.session_state.selected_mentor,
                                    conversation_history=st.session_state.conversation_history,
                                    user_background=st.session_state.user_background_stored,
                                    initial_question=st.session_state.displayed_question
                                )
                                
                                # Store follow-up response
                                st.session_state.follow_up_responses.append(follow_up_result)
                                
                                # Update conversation history with full context
                                st.session_state.conversation_history.append(
                                    f"User Follow-up to {st.session_state.selected_mentor}: {follow_up_question}"
                                )
                                st.session_state.conversation_history.append(
                                    f"{st.session_state.selected_mentor}: {follow_up_result['response']}"
                                )
                                
                                # Store in conversation history list for recursive follow-ups
                                if 'conversation_history_list' not in st.session_state:
                                    st.session_state.conversation_history_list = []
                                st.session_state.conversation_history_list.append({
                                    'turn': len(st.session_state.conversation_history_list) + 1,
                                    'mentor': st.session_state.selected_mentor,
                                    'question': follow_up_question,
                                    'response': follow_up_result['response'],
                                    'citations': follow_up_result.get('citations', [])
                                })
                                
                                # Clear selected mentor and input
                                st.session_state.selected_mentor = None
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ An error occurred: {str(e)}")
                                st.exception(e)
                    else:
                        st.warning("⚠️ Please enter a question!")
            
            with col_cancel:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_follow_up"):
                    st.session_state.selected_mentor = None
                    st.rerun()
        
        # Display follow-up responses
        if st.session_state.follow_up_responses:
            st.divider()
            st.write("### 💬 Follow-Up Responses")
            
            for i, follow_up in enumerate(st.session_state.follow_up_responses):
                mentor_name = follow_up['mentor']
                mentor_icon = follow_up['icon']
                response_text = follow_up['response']
                question = follow_up.get('question', 'Follow-up question')
                citations = follow_up.get('citations', [])
                
                # Display follow-up response header
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1f3a 0%, #2a3f5f 100%); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #667eea;">
                    <h4 style="color: #ffffff;">{mentor_icon} {mentor_name} responds:</h4>
                    <p style="font-size: 0.9rem; color: #d0d0d0; margin-bottom: 0.5rem;"><strong>Your question:</strong> {question}</p>
                </div>
                """, unsafe_allow_html=True)
                # Display response text directly (conversational format, no bullet parsing)
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #667eea;">
                    {response_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Show citations if available
                if citations and len(citations) > 0:
                    with st.expander(f"📖 {mentor_name}'s Referenced Verses ({len(citations)} citations)"):
                        for j, verse in enumerate(citations[:3], 1):
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                similarity = verse.get('similarity', 0.0)
                                st.metric("Similarity", f"{similarity:.1%}")
                            with col2:
                                reference = verse.get('reference', 'Unknown')
                                source = verse.get('source', 'Unknown')
                                verse_text = verse.get('text', '')
                                st.markdown(f"**{reference}** - {source}")
                                if verse_text:
                                    display_text = verse_text[:300] + "..." if len(verse_text) > 300 else verse_text
                                    st.markdown(f"<div class='verse-text'>{display_text}</div>", unsafe_allow_html=True)
                            if j < len(citations[:3]):
                                st.divider()
                
                if i < len(st.session_state.follow_up_responses) - 1:
                    st.divider()
    
    elif begin_button:
        st.warning("⚠️ Please enter a question first!")
    
    # Display history
    if st.session_state.dialogue_history:
        st.divider()
        st.header("📜 Dialogue History")
        
        for i, dialogue in enumerate(reversed(st.session_state.dialogue_history[-5:]), 1):
            with st.expander(f"{i}. {dialogue['question'][:60]}... ({dialogue['timestamp']})"):
                st.markdown(f"**Question:** {dialogue['question']}")
                st.markdown(f"**Synthesis:** {dialogue['synthesis'][:200]}...")
                
                if st.button(f"View Full Dialogue #{i}", key=f"view_{i}"):
                    st.info("Full dialogue viewer coming soon!")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            Built with ❤️ using LangGraph, FAISS, and Streamlit
        </p>
        <p style="font-size: 0.9rem;">
            Powered by Groq (⚡ Lightning Fast) • 4,903 Sacred Verses • 3 Spiritual Traditions
        </p>
        <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.8;">
            🕉️ May you find peace • ☸️ May you find wisdom • ✝️ May you find love
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
