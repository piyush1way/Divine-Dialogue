# 🔧 Troubleshooting Guide - Divine Dialogue

## Common Issues and Solutions

---

## 1. Import Error: RemoveMessage

**Error:**
```
ImportError: cannot import name 'RemoveMessage' from 'langchain_core.messages'
```

**Cause:** Version incompatibility between LangGraph and LangChain

**Solution:**
```bash
pip install --upgrade langchain langchain-community langchain-core langgraph langsmith
```

**Verify:**
```bash
python -c "from langgraph.graph import StateGraph, END; print('Success!')"
```

---

## 2. API Key Not Set

**Error:**
```
⚠️ WARNING: OPENROUTER_API_KEY not set in .env file
```

**Solution:**
1. Get free API key from https://openrouter.ai/
2. Edit `.env` file:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```
3. Restart the app

**Verify:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENROUTER_API_KEY'))"
```

---

## 3. RAG Database Not Found

**Error:**
```
FileNotFoundError: sacred_texts_rag_faiss/ not found
```

**Solution:**
```bash
python build_rag_database.py
```

This will create the vector database (~2 minutes).

**Verify:**
```bash
dir sacred_texts_rag_faiss
```

Should show: `index.faiss`, `texts.json`, `metadatas.json`

---

## 4. Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install -r requirements.txt
```

**For specific modules:**
```bash
pip install streamlit
pip install langgraph
pip install faiss-cpu
pip install sentence-transformers
```

---

## 5. Streamlit Won't Start

**Error:**
```
streamlit: command not found
```

**Solution:**

**Windows:**
```bash
python -m streamlit run app.py
```

**Or ensure venv is activated:**
```bash
venv\Scripts\activate
streamlit run app.py
```

---

## 6. Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**

**Option 1: Use different port**
```bash
streamlit run app.py --server.port 8502
```

**Option 2: Kill existing process**
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8501 | xargs kill -9
```

---

## 7. Model Not Available (404 Error)

**Error:**
```
Error code: 404 - No endpoints found for [model-name]:free
```

**Cause:** Free tier model temporarily unavailable

**Solution:**
✅ **Already Fixed!** The system now automatically tries multiple fallback models:
1. Mistral 7B (primary)
2. Llama 3.2 3B (fallback)
3. Qwen 2 7B (fallback)
4. Phi-3 Mini (fallback)

**Action:**
```bash
# Just restart the app
streamlit run app.py
```

The system will automatically find an available model!

**Alternative:** Get your own API key at https://openrouter.ai/ for guaranteed availability.

---

## 8. Slow Responses

**Issue:** Dialogue takes >30 seconds

**Solutions:**

**1. Check internet connection**
```bash
ping openrouter.ai
```

**2. Use your own API key**
- Free tier models can be slow
- Personal key = faster responses

**3. Reduce RAG retrieval**
```python
def retrieve_verses(query, mentor, k=2):  # Changed from 3 to 2
```

---

## 8. Memory Error

**Error:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

**1. Close other applications**

**2. Reduce batch size**
Edit `build_rag_database.py`:
```python
batch_size = 50  # Changed from 100
```

**3. Use smaller model**
```python
model = SentenceTransformer('all-MiniLM-L6-v2')  # Already smallest
```

---

## 9. LLM Call Failed

**Error:**
```
⚠️ LLM call failed: [Error message]
```

**Possible Causes:**

**1. Invalid API Key**
- Check `.env` file
- Verify key starts with `sk-or-v1-`
- Get new key from https://openrouter.ai/

**2. Rate Limit**
- Free tier: ~20 requests/minute
- Wait 1 minute and try again
- Consider paid tier

**3. Model Unavailable**
- Try different model
- Check OpenRouter status

**4. No Internet**
- Check connection
- Verify firewall settings

---

## 10. Test Failures

**Error:**
```
❌ TEST FAILED
```

**Solutions:**

**Check specific test:**
```bash
python test_comprehensive.py
```

**Common test failures:**

**1. API Key Test**
- Expected if key not set
- Add key to `.env`

**2. RAG Test**
- Rebuild database: `python build_rag_database.py`

**3. Import Test**
- Reinstall dependencies: `pip install -r requirements.txt`

---

## 11. Streamlit Errors in Browser

**Error:** Blank page or connection error

**Solutions:**

**1. Check terminal for errors**
- Look for Python exceptions
- Fix any import errors

**2. Clear browser cache**
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

**3. Try different browser**
- Chrome, Firefox, Edge

**4. Check firewall**
- Allow Python/Streamlit through firewall

---

## 12. Dependencies Conflict

**Error:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solution:**

**Clean install:**
```bash
# Deactivate venv
deactivate

# Remove venv
rmdir /s /q venv  # Windows
# rm -rf venv  # Mac/Linux

# Create fresh venv
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 13. FAISS Import Error

**Error:**
```
ImportError: DLL load failed while importing _swigfaiss
```

**Solution:**

**Windows:**
```bash
pip uninstall faiss-cpu
pip install faiss-cpu --no-cache-dir
```

**Alternative:**
```bash
pip install faiss-cpu==1.7.4
```

---

## 14. Sentence Transformers Download

**Issue:** First run downloads model (~100MB)

**Solution:**
- Wait for download to complete
- Model cached for future use
- Location: `~/.cache/torch/sentence_transformers/`

**Manual download:**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
```

---

## 15. ChromaDB SQLite Error

**Error:**
```
Your system has an unsupported version of sqlite3
```

**Solution:**
- System automatically falls back to FAISS
- No action needed
- FAISS works perfectly

**If you want ChromaDB:**
```bash
pip install pysqlite3-binary
```

---

## Quick Diagnostic Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check if venv is activated
where python  # Windows
# which python  # Mac/Linux

# Test imports
python -c "import streamlit; print('Streamlit OK')"
python -c "import langgraph; print('LangGraph OK')"
python -c "import faiss; print('FAISS OK')"

# Run setup check
python setup_divine_dialogue.py

# Run tests
python test_comprehensive.py
```

---

## Getting Help

### 1. Check Documentation
- `README.md` - Overview
- `GETTING_STARTED.md` - Quick start
- `DEPLOYMENT_README.md` - Deployment
- `QUICK_FIX.md` - Common fixes

### 2. Run Diagnostics
```bash
python setup_divine_dialogue.py
```

### 3. Check Logs
- Terminal output
- Streamlit logs
- Test reports

### 4. Verify Setup
```bash
# Check all components
python -c "
from divine_dialogue_langgraph import load_rag_database
import streamlit
import faiss
print('All imports successful!')
"
```

---

## Still Having Issues?

### Create Clean Environment

```bash
# 1. Deactivate current venv
deactivate

# 2. Remove old venv
rmdir /s /q venv

# 3. Create new venv
python -m venv venv

# 4. Activate
venv\Scripts\activate

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install dependencies
pip install -r requirements.txt

# 7. Verify
python setup_divine_dialogue.py

# 8. Run app
streamlit run app.py
```

---

## Contact & Support

- Check GitHub Issues
- Review documentation
- Run diagnostic scripts
- Check test reports

---

**Most issues are resolved by:**
1. Upgrading packages
2. Adding API key
3. Rebuilding RAG database
4. Clean venv install

**Status:** ✅ Solutions provided for all common issues
