# 🎯 DIVINE DIALOGUE - CODE WALKTHROUGH SCRIP
**For Hackathon Judges - 10-13 minute presentation**

---

## [STEP 1: STARTUP - 20 seconds]

**Action:** Open terminal and run:
```bash
streamlit run app.py
```

**Script:**
> "Let me start the application. As Streamlit loads, here's what happens behind the scenes:
> 
> 1. **RAG database loads** - 4,903 sacred verses indexed in FAISS
> 2. **LLM model initializes** - Groq API (llama-3.3-70b-versatile) for lightning-fast responses
> 3. **UI framework loads** - Streamlit web interface ready
> 4. **Voice input ready** - Browser Speech Recognition API enabled
> 
> The system is now ready for user input."

---

## [STEP 2: ARCHITECTURE OVERVIEW - 1 minute]

**Action:** Show file structure in IDE

**Script:**
> "The system has **3 core layers**:
> 
> **🏗️ LAYER 1: USER INTERFACE** (`app.py`)
> - Streamlit frontend with dark theme
> - Question input + user background personalization
> - **Voice input** via browser Speech Recognition API
> - Displays mentor responses sequentially
> - Follow-up question handling
> 
> **🏗️ LAYER 2: ORCHESTRATION** (`divine_dialogue_langgraph.py`)
> - LangGraph multi-agent state machine
> - Coordinates 3 mentor agents: Krishna → Buddha → Jesus
> - Each agent retrieves relevant verses via RAG
> - Moderator synthesizes all 3 responses into action plan
> - Fixed sequence ensures coherent dialogue
> 
> **🏗️ LAYER 3: DATA & AI** (RAG + LLM)
> - FAISS vector database with 4,903 verses
> - Semantic search using sentence-transformers
> - Groq API for fast LLM inference (300+ tokens/sec)
> - Mentor-specific verse filtering"

---

## [STEP 3: DATA FLOW - 1 minute]

**Action:** Point to code while explaining

**Script:**
> "Here's the complete data flow:
> 
> **1. USER INPUT**
> ```
> User Question + Background
>        ↓
> ```
> 
> **2. RAG RETRIEVAL** (for each mentor)
> - Semantic search in FAISS index
> - Krishna: Searches 701 Gita verses
> - Buddha: Searches 423 Dhammapada verses  
> - Jesus: Searches 3,779 Gospel verses
> - Returns top 3-5 most relevant verses per mentor
> 
> **3. LLM PROCESSING** (sequential)
> - **Krishna speaks first** - Gets question + background + Gita verses
> - **Buddha speaks second** - Gets question + background + Dhammapada verses + Krishna's response
> - **Jesus speaks third** - Gets question + background + Gospel verses + both previous responses
> 
> **4. MODERATOR SYNTHESIS**
> - Receives all 3 mentor responses
> - Creates personalized action plan
> - Formats: TODAY / THIS WEEK / ONGOING / WHEN OVERWHELMED
> 
> **5. UI DISPLAY**
> - Shows responses sequentially
> - Displays citations with similarity scores
> - User can ask follow-up questions"

---

## [STEP 4: KEY COMPONENTS - 1.5 minutes]

**Action:** Open and point to specific code sections

### **Component 1: Mentor Agents** (`divine_dialogue_langgraph.py`)

**Script:**
> "Each mentor is an LLM agent with a unique system prompt:
> 
> - **Krishna node** (lines 200-370): Teaches detachment, selfless action, dharma
> - **Buddha node** (lines 374-460): Teaches mindfulness, non-attachment, observation
> - **Jesus node** (lines 462-554): Teaches love, faith, compassion
> 
> Each agent:
> 1. Retrieves RAG verses using `search_rag_verses()`
> 2. Generates response citing specific verses
> 3. Takes 2-3 seconds (Groq is fast!)
> 4. Saves response to shared state"

### **Component 2: RAG System** (`build_rag_database.py` + `divine_dialogue_langgraph.py`)

**Script:**
> "The RAG system uses FAISS for vector search:
> 
> - **Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`
> - **Vector index**: FAISS (fast similarity search)
> - **Search function**: `search_rag_verses()` finds verses by meaning, not keywords
> - **Mentor filtering**: Only searches verses from that mentor's scripture
> - **Returns**: Top verses with similarity scores (0.0-1.0)"

### **Component 3: LangGraph Orchestration** (`divine_dialogue_langgraph.py`, lines 694-716)

**Script:**
> "The workflow is defined as a state graph:
> 
> ```python
> workflow.set_entry_point("krishna")
> workflow.add_edge("krishna", "buddha")
> workflow.add_edge("buddha", "jesus")
> workflow.add_edge("jesus", "moderator")
> ```
> 
> **State management**: `ConversationState` TypedDict tracks:
> - User question & background
> - Mentor responses (in order)
> - Citations for each mentor
> - Final synthesis"

### **Component 4: Voice Input** (`app.py`, lines 1104-1330)

**Script:**
> "Voice input uses browser's Web Speech API:
> 
> - JavaScript handles speech recognition
> - Real-time transcription into text areas
> - No server-side processing needed
> - Works in Chrome, Edge, Safari
> - Microphone button toggles recording"

---

## [STEP 5: TECHNICAL FLOW - 1 minute]

**Action:** Trace through code execution

**Script:**
> "Let me trace one complete request:
> 
> **1. User enters question** → `app.py` line 1139
> - Question: 'How to overcome depression?'
> - Background: 'M.Tech student at IIT...'
> 
> **2. Call orchestration** → `run_divine_dialogue()` line 719
> - Initializes LangGraph state
> - Starts workflow execution
> 
> **3. KRISHNA AGENT** (node executes)
> - RAG search: Finds Gita verses 2.47, 4.41, 8.12
> - LLM generates response citing these verses
> - Response saved to state
> - **Time: ~2-3 seconds**
> 
> **4. BUDDHA AGENT** (receives Krishna's response)
> - RAG search: Finds Dhammapada verses 221, 353, 376
> - LLM builds on Krishna's wisdom
> - Response saved to state
> - **Time: ~2-3 seconds**
> 
> **5. JESUS AGENT** (receives both previous responses)
> - RAG search: Finds Gospel verses from Matthew, Luke, Mark
> - LLM adds love/faith perspective
> - Response saved to state
> - **Time: ~2-3 seconds**
> 
> **6. MODERATOR AGENT**
> - Receives all 3 responses + user background
> - Creates personalized action plan
> - Formats with bullet points and emojis
> - **Time: ~3-4 seconds**
> 
> **7. UI DISPLAY** (`app.py` line 1197)
> - Displays responses sequentially
> - Shows citations in expandable sections
> - Enables follow-up questions
> 
> **Total time: ~10-15 seconds** (thanks to Groq's speed!)"

---

## [STEP 6: KEY FEATURES HIGHLIGHT - 1 minute]

**Action:** Show specific features in code

**Script:**
> "Key technical highlights:
> 
> **✅ Multi-Agent Coordination**
> - Mentors acknowledge each other (no contradictions)
> - Sequential flow ensures coherent dialogue
> - State management tracks full conversation
> 
> **✅ Authentic Teachings**
> - RAG ensures real verses, not AI-generated
> - Citations with similarity scores prove authenticity
> - Each mentor references specific verses
> 
> **✅ Personalization**
> - User background shapes all responses
> - Moderator creates situation-specific action plan
> - Follow-up questions maintain context
> 
> **✅ Performance**
> - Groq API: 300+ tokens/second
> - FAISS: Sub-millisecond vector search
> - Total response time: 10-15 seconds
> 
> **✅ Voice Input**
> - Browser-based, no server processing
> - Real-time transcription
> - Works offline after initial load"

---

## [STEP 7: READY FOR UI DEMO - 30 seconds]

**Action:** Switch to browser showing the app

**Script:**
> "The system is now ready. Let me demonstrate:
> 
> 1. **Voice input** - Click microphone, speak question
> 2. **Background personalization** - Add context about yourself
> 3. **Real-time responses** - Watch mentors respond sequentially
> 4. **Citations** - See which verses were referenced
> 5. **Action plan** - Moderator's personalized guidance
> 6. **Follow-up questions** - Ask any mentor for clarification"

---

## [LIVE UI DEMO - 3-4 minutes]

**Action:** Demonstrate the full flow

**Script:**
> "Let me show you this in action..."
> 
> **[Enter a real question via voice or typing]**
> - "I'm facing depression and anxiety due to academics. How can I overcome this?"
> 
> **[Add background]**
> - "I'm an M.Tech student at IIT. My family expects high grades, but I'm feeling overwhelmed."
> 
> **[Click "Begin Divine Dialogue"]**
> - Show loading spinner
> - Explain: "RAG is searching, LLM is generating..."
> 
> **[Watch responses appear]**
> - Krishna speaks first (2-3 sec)
> - Buddha builds on it (2-3 sec)
> - Jesus adds love/faith (2-3 sec)
> - Moderator synthesizes (3-4 sec)
> 
> **[Show citations]**
> - Expand Krishna's citations
> - Show similarity scores
> - Explain: "These are real verses from Bhagavad Gita"
> 
> **[Show action plan]**
> - Point to TODAY / THIS WEEK / ONGOING sections
> - Explain: "Personalized based on user's situation"
> 
> **[Demonstrate follow-up]**
> - Click "Ask Krishna"
> - Enter follow-up question
> - Show response maintains context

---

## [Q&A PREPARATION - Key Points]

**Be ready to explain:**

1. **Why 3 mentors?**
   - Diverse perspectives (Hindu, Buddhist, Christian)
   - Shows universal truths across traditions
   - Can easily add more (Quran, Torah, etc.)

2. **How is it personalized?**
   - User background shapes all prompts
   - Moderator creates situation-specific action plan
   - Follow-ups maintain full conversation context

3. **How fast is it?**
   - Groq API: 2-3 seconds per mentor
   - Total: 10-15 seconds for full dialogue
   - Much faster than GPT-4 (30+ seconds)

4. **How scalable?**
   - Can add 10+ spiritual traditions
   - RAG database easily expandable
   - LangGraph handles any number of agents

5. **What makes it unique?**
   - Multi-agent orchestration (not just RAG)
   - Sequential dialogue (mentors build on each other)
   - Authentic citations (real verses, not generated)
   - Voice input (accessibility feature)
   - Personalized synthesis (not generic advice)

6. **Technical stack?**
   - **Frontend**: Streamlit
   - **Orchestration**: LangGraph
   - **RAG**: FAISS + sentence-transformers
   - **LLM**: Groq (llama-3.3-70b-versatile)
   - **Voice**: Browser Web Speech API

---

## 📊 PRESENTATION TIMELINE

```
[0-0:20]    STARTUP
[0:20-1:20] ARCHITECTURE OVERVIEW
[1:20-2:20] DATA FLOW
[2:20-3:50] KEY COMPONENTS
[3:50-4:50] TECHNICAL FLOW
[4:50-5:50] KEY FEATURES
[5:50-6:20] TRANSITION TO DEMO
[6:20-10:20] LIVE UI DEMO
[10:20-13:00] Q&A
```

**Total: 10-13 minutes** ✅

---

## 🎯 TRANSITION PHRASES

- "Let me show you the code..." → Open IDE
- "Here's how it works..." → Point to specific function
- "Now let's see it in action..." → Switch to browser
- "Notice how..." → Highlight specific feature
- "The key innovation is..." → Explain technical highlight

---

## ✅ CHECKLIST BEFORE PRESENTATION

- [ ] Terminal ready with `streamlit run app.py` command
- [ ] IDE open with key files visible
- [ ] Browser ready with app loaded
- [ ] Sample question prepared
- [ ] Voice input tested (microphone permissions)
- [ ] All features working (RAG, LLM, follow-ups)
- [ ] Backup plan if API fails (show cached responses)

---

**Good luck with your presentation! 🚀**

