# 🕉️ ☸️ ✝️ Divine Dialogue

**Multi-Agent Spiritual Wisdom System powered by LangGraph**

> Ask a spiritual question and receive wisdom from Krishna, Buddha, and Jesus - each grounded in their sacred texts through AI-powered semantic search.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0-green.svg)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What is Divine Dialogue?

Divine Dialogue orchestrates conversations between three AI spiritual mentors:
- **🕉️ Krishna** from the Bhagavad Gita (701 verses)
- **☸️ Buddha** from the Dhammapada (423 verses)  
- **✝️ Jesus** from the Gospels (3,779 verses)

Each mentor retrieves relevant teachings from their sacred texts using semantic search, then engages in a thoughtful dialogue that synthesizes universal truths.

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Check setup
python setup_divine_dialogue.py

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key (get free key at https://console.groq.com/)
# Create .env file: GROQ_API_KEY=your_key_here
# No credit card required - free tier available!

# 4. Test system
python test_divine_dialogue.py

# 5. Launch web app
streamlit run app.py
```

**Done!** App runs at `http://localhost:8501`

### 🎤 Using Voice Input
1. Click the microphone button (🎤) next to the question or background field
2. Allow microphone access when prompted
3. Speak your question or background information
4. Click the button again (now red 🔴) to stop recording
5. Your speech is automatically transcribed into the text field

---

## 🌟 Features

### Multi-Agent Orchestration
LangGraph coordinates three AI mentors in sequential dialogue with state management. Each mentor builds on the previous one's wisdom, creating a coherent conversation.

### RAG-Powered Responses
4,903 sacred verses in FAISS vector database with semantic search and citation tracking. Each mentor retrieves relevant verses from their sacred texts (Gita, Dhammapada, Gospels).

### Personalized Guidance
User background personalization ensures responses are tailored to your specific situation, challenges, and life context. The moderator creates customized action plans.

### Voice Input (Speech-to-Text)
Click the microphone button to speak your question instead of typing. Uses browser's Web Speech API for real-time transcription.

### Beautiful Web Interface
Streamlit UI with gradient cards, expandable citations, conversation history, and follow-up question support.

### Unified Synthesis
AI moderator synthesizes all three mentor responses into a personalized action plan with:
- 🔴 TODAY actions (immediate steps)
- 🟡 THIS WEEK habits
- 🟢 ONGOING practices
- 🆘 Crisis techniques for when overwhelmed

---

## 📊 System Overview

```
User Question + Background
     ↓
  [Voice Input] → Speech-to-Text (optional)
     ↓
  Krishna (retrieves Gita verses → responds with citations)
     ↓
  Buddha (retrieves Dhammapada verses → builds on Krishna)
     ↓
  Jesus (retrieves Gospel verses → harmonizes both)
     ↓
  Moderator (synthesizes → personalized action plan)
     ↓
  Display with Citations + Follow-up Questions
```

**Database**: 4,903 verses | **Vector Store**: FAISS | **Embeddings**: 384-dim | **LLM**: Groq (llama-3.3-70b-versatile)

---

## 🎬 Demo

### Sample Question
> "I'm facing depression and anxiety due to academics. How can I overcome this?"

### User Background
> "I'm an M.Tech student at IIT struggling with anxiety. My family expects high grades, but I'm feeling overwhelmed by coursework. I value honesty and hard work, but I'm losing motivation..."

### Krishna's Response
> "My dear student, I see your struggle with academic pressure and anxiety. The Gita teaches in verse 2.47: 'You have a right to perform your prescribed duty, but you are not entitled to the fruits of action.' This means focus on your studies themselves—the thinking, learning, understanding—not the placement outcome. When you detach from the result, the anxiety loosens its grip."

**Citations**: Gita 2.47, 4.41, 8.12 (with similarity scores)

### Buddha's Response
> "Krishna speaks of detaching from outcomes through action, and there is wisdom in this. I add another dimension: observe the anxiety itself without fighting it. In Dhammapada verse 221, I teach: 'Give up anger, renounce pride, overcome all fetters.' The fetters binding you are not your grades—they are your CRAVING for them. Watch this craving arise. Simply observe. This is mindfulness."

**Citations**: Dhammapada 221, 376, 353 (with similarity scores)

### Jesus's Response
> "Krishna and Buddha speak truth about detachment and observation. I add: Come to me, all who are weary and burdened, and I will give you rest (Matthew 11:28). Your worth is not in your grades but in your heart. Trust that you are loved regardless of outcomes. Faith in divine timing brings peace that surpasses understanding."

**Citations**: Matthew 11:28, John 14:27, Luke 12:22 (with similarity scores)

### Moderator's Personalized Action Plan
> **🎯 FOR YOU:**
> 
> **YOUR SITUATION:**
> ✨ Academic pressure causing anxiety
> ✨ Family expectations creating stress
> 
> **WISDOM FROM THE MASTERS:**
> 🕉️ Krishna teaches: Detach from outcomes, focus on learning itself
> ☸️ Buddha teaches: Observe anxiety without judgment, practice mindfulness
> ✝️ Jesus teaches: Find rest in faith, trust in divine timing
> 
> **YOUR ACTION PLAN:**
> 
> 🔴 TODAY: Take 5 deep breaths before study sessions. Remind yourself: "I learn for understanding, not for grades."
> 
> 🟡 THIS WEEK: Practice 10 minutes of mindfulness daily. Journal one thing you learned, not one grade you got.
> 
> 🟢 ONGOING: Study with detachment. Your worth is not your GPA. Trust the process.
> 
> 🆘 WHEN OVERWHELMED: Stop. Breathe. Remember: This moment is temporary. Your soul is eternal.

---

## 📁 Project Structure

```
├── divine_dialogue_langgraph.py    # Core LangGraph system ⭐
│   ├── krishna_node()              # Krishna mentor agent
│   ├── buddha_node()                # Buddha mentor agent
│   ├── jesus_node()                 # Jesus mentor agent
│   ├── moderator_node()             # Personalized action plan
│   └── run_divine_dialogue()        # Main orchestration
│
├── app.py                           # Web interface ⭐
│   ├── Voice input (Speech-to-Text)
│   ├── User background personalization
│   ├── Follow-up questions
│   └── Response display with citations
│
├── build_rag_database.py            # RAG database builder
├── test_divine_dialogue.py          # System test
├── setup_divine_dialogue.py         # Setup checker
│
├── sacred_texts_rag_faiss/          # Vector database (7.5 MB)
│   ├── index.faiss                  # FAISS vector index
│   ├── texts.json                   # Verse texts
│   └── metadatas.json               # Verse metadata
│
├── requirements.txt                 # Dependencies
├── .env                             # API keys (create this)
│
└── Documentation/
    ├── README.md                    # This file
    ├── CODE_WALKTHROUGH_SCRIPT.md   # Presentation script
    ├── PRESENTATION_CHEAT_SHEET.md  # Quick reference
    ├── DEPLOYMENT_README.md         # Deployment guide
    └── PROJECT_SUMMARY.md           # Technical details
```

---

## 🛠️ Technology Stack

- **LangGraph** - Multi-agent orchestration and state management
- **FAISS** - Vector similarity search (4,903 verses indexed)
- **Sentence Transformers** - Text embeddings (all-MiniLM-L6-v2, 384-dim)
- **Groq API** - Lightning-fast LLM (llama-3.3-70b-versatile, ⚡ 300+ tokens/second, free tier)
- **Streamlit** - Web interface with dark theme
- **Web Speech API** - Browser-based voice input (Speech-to-Text)
- **Python 3.8+** - Core language

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file - Main overview |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Quick start guide (5 minutes) |
| [DEPLOYMENT_README.md](DEPLOYMENT_README.md) | Complete deployment & architecture |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical details & metrics |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues & solutions |

---

## 🧪 Testing

### Test RAG Search
```bash
python test_rag_search.py
```

### Test LangGraph System
```bash
python test_divine_dialogue.py
```

### Test Web Interface
```bash
streamlit run app.py
```

---

## 🚀 Deployment

### Local (Recommended for Hackathon)
```bash
streamlit run app.py
```

### Streamlit Cloud (Free Hosting)
1. Push to GitHub
2. Connect at https://streamlit.io/cloud
3. Add API key to secrets
4. Deploy

### Hugging Face Spaces
1. Create Space at https://huggingface.co/spaces
2. Upload files
3. Add secrets
4. Deploy

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details.

---

## 🎯 Use Cases

- **Spiritual Guidance** - Personalized wisdom from three traditions
- **Mental Health Support** - Accessible guidance for anxiety, depression, stress
- **Student Counseling** - Academic pressure, career uncertainty, motivation
- **Comparative Religion** - Explore universal truths across traditions
- **Interfaith Dialogue** - Bridge religious boundaries with authentic teachings
- **Personal Reflection** - Multiple perspectives on life challenges
- **Education** - Teaching tool for philosophy, ethics, and spirituality
- **Accessibility** - Voice input for users who prefer speaking over typing

---

## 📊 Performance

- **RAG Search**: <100ms per query (FAISS vector search)
- **LLM Response**: 2-3 seconds per mentor (⚡ Groq powered)
- **Total Dialogue**: 10-15 seconds (lightning fast!)
- **Voice Input**: Real-time transcription (browser-based, no server processing)
- **Memory**: ~500MB (includes FAISS index + embeddings)
- **Database**: 4,903 verses, 7.5 MB
- **Response Quality**: Personalized action plans with specific, actionable steps

---

## 🐛 Troubleshooting

### Common Issues

**"GROQ_API_KEY not set"**
- Create `.env` file in project root: `GROQ_API_KEY=your_key_here`
- Get free key at https://console.groq.com/ (no credit card required)

**"RAG database not found"**
- Run `python build_rag_database.py`
- Wait for database to build (takes 2-3 minutes)

**"Import error: langgraph"**
- Run `pip install -r requirements.txt`
- Ensure Python 3.8+ is installed

**Voice input not working**
- Check browser compatibility (Chrome, Edge, Safari support Web Speech API)
- Allow microphone permissions when prompted
- Try refreshing the page if button doesn't respond

**Slow responses**
- Groq is already the fastest! If still slow, check your internet connection
- First response may take longer (RAG database loading)

**Follow-up questions not working**
- Ensure you've completed an initial dialogue first
- Check that mentor responses were generated successfully

See [DEPLOYMENT_README.md](DEPLOYMENT_README.md) for more solutions.

---

## 🎓 Learning Resources

### Understanding the Code

**LangGraph Basics**
- [divine_dialogue_langgraph.py](divine_dialogue_langgraph.py) - Well-commented
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

**RAG Implementation**
- [build_rag_database.py](build_rag_database.py) - Database builder
- [RAG_USAGE_GUIDE.md](RAG_USAGE_GUIDE.md) - Detailed guide

**Streamlit UI**
- [app.py](app.py) - UI code
- [Streamlit Docs](https://docs.streamlit.io/)

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📄 License

MIT License - feel free to use for your own projects!

---

## 🙏 Acknowledgments

- Sacred texts from public domain sources
- Groq for lightning-fast free LLM access (⚡ 300+ tokens/second)
- LangGraph team for the framework
- Sentence Transformers for embeddings
- Streamlit for the UI framework

---

## 🎯 Roadmap

### Phase 1 (Complete) ✅
- RAG database with 4,903 verses
- LangGraph multi-agent system
- Three AI mentors
- Streamlit web interface
- Comprehensive documentation

### Phase 2 (Current Status)
- [x] Voice input (Speech-to-Text) ✅
- [x] Personalized action plans ✅
- [x] User background personalization ✅
- [x] Follow-up questions ✅
- [ ] Add more traditions (Taoism, Sufism, etc.)
- [ ] Conversation memory across sessions
- [ ] User authentication
- [ ] Mobile app
- [ ] Voice output (Text-to-Speech)

### Phase 3 (Production)
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] API endpoints
- [ ] Enterprise features

---

## 📞 Support

**Setup Issues?**
- Run `python setup_divine_dialogue.py`
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Technical Questions?**
- Review code comments
- Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**Demo Preparation?**
- See demo script in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🌟 Star This Project

If you find Divine Dialogue useful, please star the repository!

**Built with ❤️ for spiritual seekers everywhere**

🕉️ May you find peace  
☸️ May you find wisdom  
✝️ May you find love

---

## 🚀 Get Started Now

```bash
python setup_divine_dialogue.py
streamlit run app.py
```

**Your journey to divine wisdom begins here.** 🌟

### 🎯 Key Features to Try

1. **Voice Input**: Click 🎤 to speak your question
2. **Personalization**: Add your background for tailored guidance
3. **Follow-up Questions**: Ask any mentor for clarification
4. **Action Plans**: Get specific TODAY/THIS WEEK/ONGOING steps
5. **Citations**: See which verses were referenced (with similarity scores)

---

## 💡 Why Divine Dialogue?

- ✅ **Authentic** - Real verses from sacred texts, not AI-generated
- ✅ **Personalized** - Responses tailored to your specific situation
- ✅ **Multi-Perspective** - Three traditions, one unified wisdom
- ✅ **Accessible** - Free, fast, voice-enabled
- ✅ **Actionable** - Specific steps, not generic advice

**Built with ❤️ for spiritual seekers everywhere**

🕉️ May you find peace  
☸️ May you find wisdom  
✝️ May you find love
