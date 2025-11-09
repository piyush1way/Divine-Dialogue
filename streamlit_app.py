#!/usr/bin/env python3
"""
Divine Dialogue - Streamlit Web Interface
Multi-Agent Spiritual Debate System
"""

import streamlit as st
import os
from datetime import datetime
from divine_dialogue_langgraph import run_divine_dialogue, load_rag_database

# Page configuration
st.set_page_config(
    page_title="Divine Dialogue",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .mentor-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .krishna-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    }
    .buddha-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    .jesus-card {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    }
    .synthesis-card {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    .citation {
        font-size: 0.85rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'dialogue_history' not in st.session_state:
        st.session_state.dialogue_history = []
    if 'rag_loaded' not in st.session_state:
        st.session_state.rag_loaded = False


def load_rag_once():
    """Load RAG database once per session"""
    if not st.session_state.rag_loaded:
        with st.spinner("📚 Loading sacred texts database..."):
            load_rag_database()
            st.session_state.rag_loaded = True


def display_mentor_response(response_data):
    """Display a mentor's response in a styled card"""
    mentor = response_data['mentor']
    icon = response_data['icon']
    response = response_data['response']
    verses = response_data['verses']
    
    # Determine card class
    card_class = f"{mentor.lower()}-card"
    
    st.markdown(f"""
    <div class="mentor-card {card_class}">
        <h3>{icon} {mentor}</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">{response}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show citations in expander
    with st.expander(f"📖 View {mentor}'s Citations"):
        for i, verse in enumerate(verses[:3], 1):
            st.markdown(f"**{verse['reference']}** (Similarity: {verse['similarity']:.3f})")
            st.text(verse['text'][:300] + "...")
            st.divider()


def display_synthesis(synthesis_text):
    """Display the synthesis in a styled card"""
    st.markdown(f"""
    <div class="synthesis-card">
        <h2 style="text-align: center; margin-bottom: 1rem;">✨ Unified Wisdom</h2>
        <p style="font-size: 1.2rem; line-height: 1.8; text-align: center;">{synthesis_text}</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🕉️ ☸️ ✝️ Divine Dialogue</h1>
        <p style="font-size: 1.2rem;">Multi-Agent Spiritual Wisdom System</p>
        <p style="font-size: 0.9rem; opacity: 0.9;">Ask a question and receive wisdom from Krishna, Buddha, and Jesus</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Divine Dialogue** brings together three spiritual masters to discuss your questions:
        
        - 🕉️ **Krishna** - Bhagavad Gita (701 verses)
        - ☸️ **Buddha** - Dhammapada (423 verses)
        - ✝️ **Jesus** - Gospels (3,779 verses)
        
        Each mentor retrieves relevant teachings from their sacred texts using AI-powered semantic search.
        """)
        
        st.divider()
        
        st.header("🎯 Sample Questions")
        sample_questions = [
            "How can I find inner peace?",
            "What is the purpose of life?",
            "How should I treat my enemies?",
            "What happens after death?",
            "How do I overcome suffering?",
            "What is true love?",
            "How can I be a better person?"
        ]
        
        for q in sample_questions:
            if st.button(q, key=f"sample_{q}"):
                st.session_state.selected_question = q
        
        st.divider()
        
        st.header("📊 System Info")
        st.metric("Total Verses", "4,903")
        st.metric("Vector Store", "FAISS")
        st.metric("Embedding Model", "all-MiniLM-L6-v2")
        
        if st.button("🔄 Clear History"):
            st.session_state.dialogue_history = []
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💭 Ask Your Question")
        
        # Check if a sample question was selected
        default_question = st.session_state.get('selected_question', '')
        
        user_question = st.text_area(
            "Enter your spiritual question:",
            value=default_question,
            height=100,
            placeholder="e.g., How can I find inner peace in times of suffering?"
        )
        
        # Clear the selected question after using it
        if 'selected_question' in st.session_state:
            del st.session_state.selected_question
        
        col_btn1, col_btn2 = st.columns([3, 1])
        
        with col_btn1:
            ask_button = st.button("🚀 Start Divine Dialogue", type="primary")
        
        with col_btn2:
            if st.button("❌ Clear"):
                st.rerun()
    
    with col2:
        st.header("📜 Recent Dialogues")
        if st.session_state.dialogue_history:
            for i, dialogue in enumerate(reversed(st.session_state.dialogue_history[-5:]), 1):
                with st.expander(f"{i}. {dialogue['question'][:50]}..."):
                    st.write(f"**Asked:** {dialogue['timestamp']}")
                    st.write(f"**Synthesis:** {dialogue['synthesis'][:150]}...")
        else:
            st.info("No dialogues yet. Ask a question to begin!")
    
    # Process question
    if ask_button and user_question.strip():
        # Load RAG database
        load_rag_once()
        
        # Run the dialogue
        with st.spinner("🌟 The mentors are contemplating your question..."):
            try:
                result = run_divine_dialogue(user_question)
                
                if 'error' not in result:
                    # Display results
                    st.success("✅ Divine Dialogue Complete!")
                    
                    st.divider()
                    st.header("💬 The Mentors Speak")
                    
                    # Display each mentor's response
                    for response in result['mentor_responses']:
                        display_mentor_response(response)
                    
                    st.divider()
                    
                    # Display synthesis
                    display_synthesis(result['synthesis'])
                    
                    # Save to history
                    st.session_state.dialogue_history.append({
                        'question': user_question,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'mentor_responses': result['mentor_responses'],
                        'synthesis': result['synthesis']
                    })
                    
                    # Download option
                    st.divider()
                    
                    # Format dialogue for download
                    dialogue_text = f"""DIVINE DIALOGUE
Question: {user_question}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{'='*70}

"""
                    for response in result['mentor_responses']:
                        dialogue_text += f"{response['icon']} {response['mentor']}:\n{response['response']}\n\n"
                        dialogue_text += f"Citations: {', '.join([v['reference'] for v in response['verses'][:3]])}\n\n"
                        dialogue_text += f"{'='*70}\n\n"
                    
                    dialogue_text += f"✨ SYNTHESIS:\n{result['synthesis']}\n"
                    
                    st.download_button(
                        label="📥 Download Dialogue",
                        data=dialogue_text,
                        file_name=f"divine_dialogue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
                else:
                    st.error(f"❌ Error: {result['error']}")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)
    
    elif ask_button:
        st.warning("⚠️ Please enter a question first!")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>Built with ❤️ using LangGraph, FAISS, and Streamlit</p>
        <p style="font-size: 0.85rem;">Powered by OpenRouter AI • 4,903 Sacred Verses</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
