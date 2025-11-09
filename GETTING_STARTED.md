# 🚀 Getting Started with Divine Dialogue

**Complete guide to get your Divine Dialogue system running in 15 minutes**

---

## ✅ Current Status

Your Divine Dialogue system is **95% ready**! Here's what's already done:

✅ Python 3.9 installed  
✅ All dependencies installed  
✅ RAG database built (4,903 verses)  
✅ Source data files present  
✅ All code files created  
✅ Documentation complete  

**Only 1 step remaining**: Add your OpenRouter API key

---

## 🔑 Step 1: Get Your Free API Key (2 minutes)

1. Go to **https://openrouter.ai/**
2. Click "Sign Up" (top right)
3. Sign up with Google/GitHub (fastest)
4. Go to "Keys" section
5. Click "Create Key"
6. Copy the key (starts with `sk-or-v1-`)

**Cost**: FREE (includes free tier models)

---

## 📝 Step 2: Add API Key to .env File (1 minute)

Open the `.env` file in your project root and replace the placeholder:

**Before:**
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**After:**
```
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

Save the file.

---

## 🧪 Step 3: Test the System (2 minutes)

Run the test script:

```bash
python test_divine_dialogue.py
```

**Expected output:**
```
======================================================================
🕉️ ☸️ ✝️  DIVINE DIALOGUE - Multi-Agent Spiritual Debate
======================================================================

Question: How can I find inner peace in times of suffering?

📚 Loading RAG database...
✓ Loaded 4903 verses

🕉️  Krishna is speaking...
☸️  Buddha is speaking...
✝️  Jesus is speaking...
🌟 Synthesizing wisdom...

======================================================================
✨ SYNTHESIS
======================================================================
[Unified wisdom appears here]

======================================================================
✅ TEST SUCCESSFUL - All mentors responded!
```

If you see this, **you're ready!** 🎉

---

## 🌐 Step 4: Launch the Web App (1 minute)

Start the Streamlit app:

```bash
streamlit run streamlit_app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Your browser will automatically open to the app!

---

## 🎯 Step 5: Try Your First Question (1 minute)

In the web app:

1. Type a question in the text area:
   - "How can I find inner peace?"
   - "What is the purpose of life?"
   - "How should I treat my enemies?"

2. Click "🚀 Start Divine Dialogue"

3. Watch as:
   - Krishna responds with Gita verses
   - Buddha responds with Dhammapada verses
   - Jesus responds with Gospel verses
   - Synthesis bridges all three

4. Expand citations to see the actual verses

**Congratulations!** You're now using Divine Dialogue! 🎊

---

## 📖 What to Do Next

### Explore Sample Questions

Try these questions to see the system in action:

**Life Purpose**
- "What is the meaning of life?"
- "What is my purpose?"
- "Why am I here?"

**Inner Peace**
- "How can I find peace?"
- "How do I calm my mind?"
- "How can I be happy?"

**Relationships**
- "How should I treat others?"
- "What is true love?"
- "How do I forgive?"

**Suffering**
- "Why do we suffer?"
- "How do I overcome pain?"
- "What happens after death?"

**Personal Growth**
- "How can I be a better person?"
- "What is wisdom?"
- "How do I find truth?"

### Customize the System

**Change the LLM Model**

Edit `divine_dialogue_langgraph.py`, line ~80:

```python
def call_llm(system_prompt, user_message, model="google/gemma-2-9b-it:free"):
    # Try different free models
```

**Adjust Response Length**

Edit system prompts in `divine_dialogue_langgraph.py`:

```python
system_prompt = """...
Your response should:
- Be 3-4 sentences maximum  # Change this
..."""
```

**Retrieve More Verses**

Edit `retrieve_verses()` in `divine_dialogue_langgraph.py`:

```python
def retrieve_verses(query, mentor, k=5):  # Change from 3 to 5
    # ...
```

### Share Your Results

**Download Dialogues**

After each dialogue, click "📥 Download Dialogue" to save as text file.

**Take Screenshots**

Use the screenshot feature to capture beautiful responses for sharing.

**Share on Social Media**

Post your favorite dialogues with #DivinDialogue

---

## 🐛 Troubleshooting

### Issue: "OPENROUTER_API_KEY not set"

**Solution:**
1. Check `.env` file exists in project root
2. Verify API key is correct (starts with `sk-or-v1-`)
3. No spaces around the `=` sign
4. Restart the app after editing `.env`

### Issue: "LLM call failed"

**Possible causes:**
- Invalid API key → Check `.env` file
- No internet → Check connection
- Rate limit → Wait 1 minute, try again
- Model unavailable → Try different model

**Quick fix:**
```python
# In divine_dialogue_langgraph.py, change model:
model="meta-llama/llama-3.2-3b-instruct:free"
```

### Issue: Slow responses

**Solutions:**
1. Use faster model (may cost money)
2. Reduce RAG retrieval (`k=2`)
3. Shorten system prompts
4. Check internet speed

### Issue: "Streamlit not found"

**Solution:**
```bash
pip install streamlit
```

### Issue: Port already in use

**Solution:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📊 Understanding the Output

### Mentor Response Format

```
🕉️ Krishna:
[Response text with natural verse references]

📖 View Krishna's Citations
  Gita 2.47 (Similarity: 0.523)
  [Full verse text]
```

**Similarity Score**: 0.0-1.0 (higher = more relevant)
- 0.5+ = Highly relevant
- 0.4-0.5 = Relevant
- <0.4 = Somewhat relevant

### Synthesis Format

```
✨ Unified Wisdom
[3-4 sentences bridging all three traditions]
```

The synthesis shows:
- Common themes across traditions
- How apparent contradictions resolve
- Universal spiritual truths

---

## 🎯 Tips for Best Results

### Ask Clear Questions

**Good:**
- "How can I find inner peace?"
- "What is the purpose of suffering?"
- "How should I treat my enemies?"

**Less Good:**
- "Tell me about Krishna"
- "What's in the Bible?"
- "Explain Buddhism"

### Use Spiritual Themes

The system works best with questions about:
- Life purpose and meaning
- Inner peace and happiness
- Love and relationships
- Suffering and death
- Personal growth
- Wisdom and truth
- Duty and ethics

### Explore Different Angles

Try asking the same question in different ways:
- "How do I find peace?" vs "What is inner peace?"
- "Why do we suffer?" vs "How do I overcome suffering?"

---

## 📚 Learn More

### Documentation

- **README.md** - Project overview
- **README_DIVINE_DIALOGUE.md** - Complete documentation
- **DEPLOYMENT_GUIDE.md** - Deployment instructions
- **PROJECT_SUMMARY.md** - Technical details
- **RAG_USAGE_GUIDE.md** - RAG system guide
- **QUICK_REFERENCE.md** - Quick reference

### Code Files

- **divine_dialogue_langgraph.py** - Core system (well-commented)
- **streamlit_app.py** - Web interface
- **build_rag_database.py** - Database builder

### Test Scripts

- **test_divine_dialogue.py** - System test
- **test_rag_search.py** - RAG test
- **setup_divine_dialogue.py** - Setup check

---

## 🎬 Demo Preparation (For Hackathon)

### Before the Demo

1. **Test 5 questions** beforehand
2. **Screenshot good results** as backup
3. **Practice your pitch** (2 minutes)
4. **Charge your laptop**
5. **Test internet connection**

### During the Demo

1. **Opening** (30 sec): Explain the concept
2. **Live Demo** (60 sec): Ask a question, show responses
3. **Technical** (30 sec): Highlight LangGraph + RAG
4. **Closing** (30 sec): Impact and future

### Backup Plan

If API fails:
- Show pre-generated responses
- Demo RAG search only
- Walk through architecture
- Show the code

---

## ✅ Final Checklist

Before your demo:

- [ ] API key configured
- [ ] Test script passes
- [ ] Web app launches
- [ ] 5 questions tested
- [ ] Screenshots taken
- [ ] Demo script practiced
- [ ] Laptop charged
- [ ] Internet working
- [ ] Backup plan ready

---

## 🎉 You're Ready!

Your Divine Dialogue system is fully operational and ready for:
- Personal use
- Hackathon demo
- Portfolio project
- Further development

**Enjoy exploring spiritual wisdom with AI!** 🌟

---

## 📞 Need Help?

1. Run `python setup_divine_dialogue.py` to check status
2. Review troubleshooting section above
3. Check documentation files
4. Review code comments

---

**Built with ❤️ for spiritual seekers everywhere**

🕉️ May you find peace  
☸️ May you find wisdom  
✝️ May you find love

---

## 🚀 Quick Commands Reference

```bash
# Check setup
python setup_divine_dialogue.py

# Test system
python test_divine_dialogue.py

# Test RAG
python test_rag_search.py

# Launch app
streamlit run streamlit_app.py

# Rebuild database (if needed)
python build_rag_database.py
```

**Your journey begins now!** 🌟
