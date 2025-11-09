# 🎯 DIVINE DIALOGUE - QUICK REFERENCE CHEAT SHEET

**One-page guide for hackathon presentation**

---

## ⚡ QUICK START (20 sec)

```bash
streamlit run app.py
```

**Say:** "RAG loads 4,903 verses → Groq LLM initializes → UI ready"

---

## 🏗️ ARCHITECTURE (3 layers - 1 min)

1. **UI Layer** (`app.py`) - Streamlit + Voice Input
2. **Orchestration** (`divine_dialogue_langgraph.py`) - LangGraph agents
3. **Data Layer** - FAISS RAG + Groq LLM

---

## 🔄 DATA FLOW (1 min)

```
User Question
    ↓
RAG Search (FAISS) → Find relevant verses
    ↓
Krishna Agent → Gita verses → Response
    ↓
Buddha Agent → Dhammapada verses → Response (builds on Krishna)
    ↓
Jesus Agent → Gospel verses → Response (builds on both)
    ↓
Moderator → Synthesizes → Action Plan
    ↓
UI Display
```

---

## 📁 KEY FILES & LINE NUMBERS

- **`app.py`** (line 981) - Main UI, voice input (1104-1330)
- **`divine_dialogue_langgraph.py`** (line 719) - `run_divine_dialogue()`
- **`divine_dialogue_langgraph.py`** (line 694) - `build_divine_dialogue_graph()`
- **`divine_dialogue_langgraph.py`** (line 200) - Krishna node
- **`divine_dialogue_langgraph.py`** (line 374) - Buddha node
- **`divine_dialogue_langgraph.py`** (line 462) - Jesus node
- **`divine_dialogue_langgraph.py`** (line 556) - Moderator node

---

## 🎯 KEY POINTS TO EMPHASIZE

✅ **Multi-agent orchestration** (not just RAG)  
✅ **Sequential dialogue** (mentors build on each other)  
✅ **Authentic citations** (real verses, not generated)  
✅ **Voice input** (accessibility)  
✅ **Fast** (10-15 sec total, Groq API)  
✅ **Personalized** (user background shapes responses)  

---

## 💬 DEMO SCRIPT (3-4 min)

1. **Show voice input** - Click mic, speak question
2. **Add background** - "M.Tech student at IIT..."
3. **Click "Begin Divine Dialogue"**
4. **Watch responses** - Krishna → Buddha → Jesus → Moderator
5. **Show citations** - Expand, show similarity scores
6. **Show action plan** - TODAY / THIS WEEK / ONGOING
7. **Follow-up demo** - Ask Krishna a question

---

## ❓ COMMON Q&A ANSWERS

**Q: Why 3 mentors?**  
A: Diverse perspectives show universal truths. Can add more easily.

**Q: How fast?**  
A: 2-3 sec per mentor, 10-15 sec total (Groq is 10x faster than GPT-4)

**Q: How personalized?**  
A: User background shapes all prompts. Moderator creates situation-specific plan.

**Q: What's unique?**  
A: Multi-agent orchestration with sequential dialogue. Not just RAG - agents coordinate.

**Q: Technical stack?**  
A: Streamlit + LangGraph + FAISS + Groq + Web Speech API

---

## ⏱️ TIMING

- **0-6 min**: Code walkthrough
- **6-10 min**: Live demo
- **10-13 min**: Q&A

**Total: 10-13 minutes** ✅

---

## 🚨 BACKUP PLAN

If API fails:
- Show cached responses
- Explain architecture without live demo
- Show code structure and explain flow

---

**Keep this page open during presentation! 📋**

