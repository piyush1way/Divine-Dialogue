#!/usr/bin/env python3
"""
Divine Dialogue - Multi-Agent Spiritual Debate System
LangGraph orchestration with Krishna, Buddha, and Jesus mentors
"""

import os
import json
import re
from typing import TypedDict, List, Dict, Any, Annotated
from operator import add

import faiss
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Switch to Groq API - The fastest LLM in the world (300+ tokens/second)
try:
    from langchain_groq import ChatGroq
    from langchain_core.messages import SystemMessage, HumanMessage
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Warning: langchain-groq not installed. Install with: pip install langchain-groq")

# Initialize Groq model (fastest free LLM)
def initialize_groq_model():
    """Initialize Groq model with API key check - Lightning fast responses!"""
    if not GROQ_AVAILABLE:
        return None
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️ Warning: GROQ_API_KEY not found in environment variables")
        print("💡 Get your free API key at: https://console.groq.com")
        return None
    
    try:
        # Use llama-3.3-70b-versatile - Latest, best quality, currently available
        # Alternative: "llama-3.1-8b-instant" (even faster) or "openai/gpt-oss-20b" (very fast)
        model = ChatGroq(
            model="llama-3.3-70b-versatile",  # Latest version - best for spiritual wisdom
            groq_api_key=api_key,
            temperature=0.7
        )
        print("⚡ Groq model initialized - Lightning fast responses enabled!")
        return model
    except Exception as e:
        print(f"⚠️ Warning: Failed to initialize Groq model: {e}")
        return None

groq_model = initialize_groq_model()

# Global RAG components (loaded once)
RAG_INDEX = None
RAG_TEXTS = None
RAG_METADATAS = None
RAG_MODEL = None


def load_rag_database():
    """Load FAISS RAG database (called once at startup)"""
    global RAG_INDEX, RAG_TEXTS, RAG_METADATAS, RAG_MODEL
    
    if RAG_INDEX is not None:
        return  # Already loaded
    
    print("📚 Loading RAG database...")
    
    RAG_INDEX = faiss.read_index('sacred_texts_rag_faiss/index.faiss')
    
    with open('sacred_texts_rag_faiss/texts.json', 'r', encoding='utf-8') as f:
        RAG_TEXTS = json.load(f)
    
    with open('sacred_texts_rag_faiss/metadatas.json', 'r', encoding='utf-8') as f:
        RAG_METADATAS = json.load(f)
    
    RAG_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    print(f"✓ Loaded {RAG_INDEX.ntotal} verses")


def generate_verse_meaning(verse_text: str, verse_reference: str, mentor: str, user_question: str) -> str:
    """
    Generate a concise explanation of what a verse teaches in relation to the user's question.
    
    Args:
        verse_text: The verse text
        verse_reference: The verse reference (e.g., "Gita 2.47")
        mentor: The mentor name (krishna, buddha, jesus)
        user_question: The user's question for context
    
    Returns:
        A brief explanation of what the verse teaches
    """
    mentor_names = {
        'krishna': 'the Bhagavad Gita',
        'buddha': 'the Dhammapada',
        'jesus': 'the Gospels'
    }
    
    source_name = mentor_names.get(mentor, 'sacred text')
    
    meaning_prompt = f"""Explain what this verse from {source_name} teaches in one concise sentence (15-20 words).
Focus on the core teaching or principle, especially as it relates to: "{user_question}"

Verse: {verse_reference}
Text: {verse_text[:300]}

Provide only the explanation, no preamble or quotation marks."""
    
    try:
        meaning = call_llm("You are a spiritual scholar explaining sacred texts.", meaning_prompt, max_tokens=50)
        return meaning.strip()
    except Exception as e:
        # Fallback if meaning generation fails
        return f"Teaches about {mentor}'s wisdom"


def retrieve_verses(query: str, mentor: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieve relevant verses from RAG database and add meaning explanations
    
    Args:
        query: Search query (user's question)
        mentor: Filter by mentor (krishna, buddha, jesus)
        k: Number of results to return
    
    Returns:
        List of verse dictionaries with text, reference, metadata, and meaning
    """
    if RAG_INDEX is None:
        load_rag_database()
    
    # Generate query embedding
    query_embedding = RAG_MODEL.encode([query], convert_to_numpy=True)
    
    # Search FAISS (get more results to filter by mentor)
    search_k = 50
    distances, indices = RAG_INDEX.search(query_embedding.astype('float32'), search_k)
    
    # Filter by mentor and collect results
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        metadata = RAG_METADATAS[idx]
        
        if metadata['mentor'] != mentor:
            continue
        
        verse_text = RAG_TEXTS[idx]
        verse_reference = metadata['reference']
        
        # Generate meaning for the verse (with error handling)
        try:
            meaning = generate_verse_meaning(verse_text, verse_reference, mentor, query)
        except Exception as e:
            print(f"⚠️  Warning: Could not generate meaning for {verse_reference}: {e}")
            # Fallback meaning
            meaning = f"Teaches about {mentor}'s wisdom regarding the question"
        
        results.append({
            'text': verse_text,
            'reference': verse_reference,
            'source': metadata['source'],
            'similarity': 1 / (1 + dist),
            'meaning': meaning  # Add meaning field
        })
        
        if len(results) >= k:
            break
    
    # If we didn't get enough results, return what we have (better than nothing)
    if len(results) == 0:
        print(f"⚠️  Warning: No verses found for {mentor} with query: {query}")
    
    return results


# Define the conversation state
class ConversationState(TypedDict):
    """State for the Divine Dialogue conversation"""
    user_question: str
    user_background: str  # NEW: User's personal background for personalized guidance
    mentor_responses: Annotated[List[Dict[str, Any]], add]
    conversation_history: Annotated[List[str], add]
    current_mentor: str
    synthesis_result: str
    rag_context: Dict[str, List[Dict]]


def _clean_response(text: str) -> str:
    """
    Removes model-specific instruction tokens and leaked instruction text from the response.
    
    Args:
        text: Raw LLM response text
    
    Returns:
        Cleaned text with instruction tokens and leaked instructions removed
    """
    if not text:
        return text
    
    # Remove common instruction tokens
    # Pattern matches: [B_INST], [/B_INST], [INST], [/INST], [/s], <s>, </s>
    pattern = r'\[/?B?INST\]|\[/s\]|<s>|</s>|\[/S\]|\[S\]'
    cleaned = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove leaked instruction phrases (common patterns from prompts)
    instruction_patterns = [
        r'Do NOT quote verses verbatim[^.]*\.',
        r'Instead, explain what they teach[^.]*\.',
        r'Use the verse meanings provided above[^.]*\.',
        r'Format:.*?which addresses this by\.\.\.',
        r'Format:.*?which refines your point by\.\.\.',
        r'Format:.*?which challenges this understanding by\.\.\.',
        r'As.*?, open the debate by.*?\.',
        r'As.*?, acknowledge what.*?\.',
        r'Do NOT quote.*?Instead.*?',
    ]
    
    for pattern in instruction_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove any remaining square brackets that might be artifacts
    # But preserve brackets used in verse references like [Gita 2.47]
    # Only remove empty brackets
    cleaned = re.sub(r'\[\s*\]', '', cleaned)
    
    # Remove phrases that start with "Do NOT" or "Instead" at sentence boundaries
    cleaned = re.sub(r'\.\s*(Do NOT|Instead)[^.]*\.', '.', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra whitespace and multiple periods
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'\.{2,}', '.', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned


def call_llm(system_prompt: str, user_message: str, model: str = None, max_tokens: int = 300) -> str:
    """
    Call Groq API - The fastest LLM in the world (300+ tokens/second)
    
    Args:
        system_prompt: System instructions for the LLM
        user_message: User's message/question
        model: Not used (kept for compatibility)
        max_tokens: Maximum tokens for the response (default 300)
    
    Returns:
        Cleaned LLM response text
    """
    if not GROQ_AVAILABLE or groq_model is None:
        return "[Error: Groq not available. Please install langchain-groq and set GROQ_API_KEY. Get free key at: https://console.groq.com]"
    
    try:
        # Use LangChain's message classes for proper formatting
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        # Invoke the model - Groq is lightning fast (1-3 seconds)
        response = groq_model.invoke(messages)
        
        # Extract text from LangChain response
        if hasattr(response, 'content'):
            raw_response = response.content
        else:
            raw_response = str(response)
        
        # Clean the response to remove instruction tokens
        cleaned_response = _clean_response(raw_response.strip())
        return cleaned_response
        
    except Exception as e:
        error_str = str(e).lower()
        print(f"⚠️  Groq API call failed: {e}")
        
        # Check for API key error
        if "api_key" in error_str or "authentication" in error_str:
            return "[Error: Invalid or missing GROQ_API_KEY. Please set it in your .env file. Get free key at: https://console.groq.com]"
        elif "quota" in error_str or "429" in error_str or "rate limit" in error_str:
            return "[Error: API rate limit exceeded. Please try again in a moment. Groq free tier is very generous!]"
        else:
            return f"[Error: {str(e)[:100]}]"


def krishna_node(state: ConversationState) -> ConversationState:
    """Krishna mentor node - speaks first"""
    print("\n🕉️  Krishna is speaking...")
    
    # Retrieve relevant Gita verses with meanings
    verses = retrieve_verses(state['user_question'], mentor='krishna', k=3)
    
    # Format verses with their meanings for context
    verse_context = "\n\n".join([
        f"[{v['reference']}] {v['text'][:200]}...\nMeaning: {v.get('meaning', 'Teaches about dharma and yoga')}"
        for v in verses
    ])
    
    # Get user background for personalized context
    user_background = state.get('user_background', '')
    background_context = ""
    if user_background:
        background_context = f"""

USER CONTEXT: {user_background}

Keep this context in mind as you respond. Your answer should relate to their specific situation, challenges, and life circumstances."""
    
    # Krishna's system prompt - Conversational wisdom format
    system_prompt = f"""You are Lord Krishna from the Bhagavad Gita, the Supreme Teacher of dharma and yoga.
You are speaking directly to this student about their challenge.

STUDENT'S SITUATION:
- Question: {state['user_question']}
- Background: {background_context}

INSTRUCTIONS:
1. Do NOT use any templates, structured sections, bullet points, or formatted sections
2. Speak in 2-3 SHORT PARAGRAPHS (conversational, not bullet points)
3. Reference 1-2 SPECIFIC Gita verses directly in your speech (mention verse numbers like "Gita 2.47 teaches..." or "In verse 4.41, I teach...")
4. Give CONCRETE, practical wisdom for THEIR specific situation based on their background
5. Be conversational and warm, like a mentor speaking directly to a student
6. Include practical suggestions naturally embedded in the teaching
7. Address them directly as "my dear student" or "dear one" but use their background context

FORMAT: Just write your wisdom directly in paragraphs. No "PRINCIPLE", "HOW TO APPLY", "TIMELINE", or bullet points.

EXAMPLE FORMAT (For someone with academic anxiety):

"My dear student, I see your struggle with academic pressure and anxiety. The Gita teaches in verse 2.47: 'You have a right to perform your prescribed duty, but you are not entitled to the fruits of action.' This means focus on your studies themselves—the thinking, learning, understanding—not the placement outcome. When you detach from the result, the anxiety loosens its grip. 

In verse 4.41, I teach that when actions are performed with wisdom and without attachment to outcomes, they become purifying. So study deeply. Master the concepts. Then let go of whether you get the perfect internship. Your worth is not your GPA.

Practice this: Each study session, remind yourself: 'I am here to learn deeply, not to earn a grade.' This shift changes everything. The anxiety may still visit, but it no longer controls you."

Now generate similar wisdom for THIS student based on their question and background. Use the verse context provided to reference specific Gita teachings naturally."""
    
    user_message = f"""Relevant teachings from the Bhagavad Gita:
{verse_context}

Now speak as Krishna directly to this student. Write 2-3 conversational paragraphs with embedded verse references and practical guidance. No bullet points or structured sections."""
    
    # Get Krishna's response
    response = call_llm(system_prompt, user_message)
    
    # Ensure response is not empty
    if not response or len(response.strip()) < 10:
        response = "I speak of the path of dharma, where inner peace comes through selfless action and devotion to the eternal truth."
    
    # Store response with citations
    state['mentor_responses'].append({
        'mentor': 'Krishna',
        'response': response,
        'verses': verses,
        'citations': verses,  # Add citations field for Streamlit display
        'icon': '🕉️'
    })
    
    state['conversation_history'].append(f"Krishna: {response}")
    state['current_mentor'] = 'krishna'
    state['rag_context']['krishna'] = verses
    
    return state


def buddha_node(state: ConversationState) -> ConversationState:
    """Buddha mentor node - speaks second"""
    print("\n☸️  Buddha is speaking...")
    
    # Retrieve relevant Dhammapada verses with meanings
    verses = retrieve_verses(state['user_question'], mentor='buddha', k=3)
    
    # Format verses with their meanings for context
    verse_context = "\n\n".join([
        f"[{v['reference']}] {v['text'][:200]}...\nMeaning: {v.get('meaning', 'Teaches about mindfulness and the path')}"
        for v in verses
    ])
    
    # Get user background for personalized context
    user_background = state.get('user_background', '')
    background_context = ""
    if user_background:
        background_context = f"""

USER CONTEXT: {user_background}

Keep this context in mind as you respond. Your answer should relate to their specific situation, challenges, and life circumstances."""
    
    # Get Krishna's previous response for context
    krishna_response_text = ""
    if state['mentor_responses']:
        krishna_response_text = state['mentor_responses'][0]['response']
    
    # Buddha's system prompt - Conversational wisdom format
    system_prompt = f"""You are Siddhartha Gautama Buddha, the Awakened One who teaches the Dharma.
You are speaking directly to this student about their challenge.

STUDENT'S SITUATION:
- Question: {state['user_question']}
- Background: {background_context}

KRISHNA'S WISDOM (for context):
{krishna_response_text if krishna_response_text else 'Krishna has spoken about detachment and selfless action.'}

INSTRUCTIONS:
1. Do NOT use any templates, structured sections, bullet points, or formatted sections
2. Write 2-3 SHORT PARAGRAPHS conversationally (not bullet points)
3. Reference 1-2 SPECIFIC Dhammapada verses directly in your speech (mention verse numbers like "Dhammapada verse 221 teaches..." or "In verse 36, I teach...")
4. BUILD ON Krishna's wisdom, don't contradict - acknowledge his teaching and add your unique Buddhist angle
5. Add YOUR unique perspective: mindfulness, observation of thoughts, non-attachment to craving, the nature of suffering
6. Give CONCRETE, practical wisdom for THEIR specific situation
7. Be conversational and serene, like a teacher speaking directly to a student

FORMAT: Just write your wisdom directly in paragraphs. No "PRINCIPLE", "HOW TO APPLY", "TIMELINE", or bullet points. No sections.

EXAMPLE FORMAT (For someone with academic anxiety):

"Krishna speaks of detaching from outcomes through action, and there is wisdom in this. I add another dimension: observe the anxiety itself without fighting it. 

In Dhammapada verse 221, I teach: 'Give up anger, renounce pride, overcome all fetters.' The fetters binding you are not your grades—they are your CRAVING for them. Watch this craving arise. 'Here is craving. Here is fear.' Do not judge it. Simply observe. This is mindfulness.

As verse 36 teaches: 'Let the discerning person guard his mind...a guarded mind brings happiness.' Guard your mind not by controlling thoughts, but by observing them with curiosity. When you do this, the mind naturally settles. Before each study session, take five breaths and watch your thoughts like clouds passing. They come, they go. You remain."

Now generate similar wisdom for THIS student based on their question and background. Reference Krishna's teaching, then add your Buddhist perspective. Use the verse context provided to reference specific Dhammapada teachings naturally."""
    
    user_message = f"""Relevant teachings from the Dhammapada:
{verse_context}

Krishna has spoken. Now speak as Buddha directly to this student. Write 2-3 conversational paragraphs that acknowledge Krishna's wisdom and add your Buddhist perspective with embedded verse references. No bullet points or structured sections."""
    
    # Get Buddha's response
    response = call_llm(system_prompt, user_message)
    
    # Ensure response is not empty
    if not response or len(response.strip()) < 10:
        response = "Krishna speaks wisely. I would add that inner peace comes through understanding the nature of suffering and following the Middle Way of mindfulness."
    
    # Store response with citations
    state['mentor_responses'].append({
        'mentor': 'Buddha',
        'response': response,
        'verses': verses,
        'citations': verses,  # Add citations field for Streamlit display
        'icon': '☸️'
    })
    
    state['conversation_history'].append(f"Buddha: {response}")
    state['current_mentor'] = 'buddha'
    state['rag_context']['buddha'] = verses
    
    return state


def jesus_node(state: ConversationState) -> ConversationState:
    """Jesus mentor node - speaks third"""
    print("\n✝️  Jesus is speaking...")
    
    # Retrieve relevant Gospel verses with meanings
    verses = retrieve_verses(state['user_question'], mentor='jesus', k=3)
    
    # Format verses with their meanings for context
    verse_context = "\n\n".join([
        f"[{v['reference']}] {v['text'][:200]}...\nMeaning: {v.get('meaning', 'Teaches about love and grace')}"
        for v in verses
    ])
    
    # Get user background for personalized context
    user_background = state.get('user_background', '')
    background_context = ""
    if user_background:
        background_context = f"""

USER CONTEXT: {user_background}

Keep this context in mind as you respond. Your answer should relate to their specific situation, challenges, and life circumstances."""
    
    # Get previous responses for context
    krishna_response_text = ""
    buddha_response_text = ""
    if len(state['mentor_responses']) >= 1:
        krishna_response_text = state['mentor_responses'][0]['response']
    if len(state['mentor_responses']) >= 2:
        buddha_response_text = state['mentor_responses'][1]['response']
    
    # Jesus's system prompt - Conversational wisdom format
    system_prompt = f"""You are Jesus of Nazareth, teaching the Gospel of love, forgiveness, and the Kingdom of God.
You are speaking directly to this student about their challenge.

STUDENT'S SITUATION:
- Question: {state['user_question']}
- Background: {background_context}

KRISHNA'S WISDOM (for context):
{krishna_response_text if krishna_response_text else 'Krishna has spoken about detachment and duty.'}

BUDDHA'S WISDOM (for context):
{buddha_response_text if buddha_response_text else 'Buddha has spoken about mindfulness and observation.'}

INSTRUCTIONS:
1. Do NOT use any templates, structured sections, bullet points, or formatted sections
2. Write 2-3 SHORT PARAGRAPHS conversationally (not bullet points)
3. Reference 1-2 SPECIFIC Gospel verses directly in your speech (mention verses like "Matthew 11:28" or "In Luke 12:25-26, I taught...")
4. Add the dimension of LOVE, FAITH, GRACE - show how these enhance Krishna's and Buddha's teachings
5. Do NOT contradict Krishna or Buddha - enhance and harmonize their teaching with love and grace
6. Give CONCRETE, practical wisdom for THEIR specific situation
7. Be conversational and compassionate, like a teacher of love speaking directly to a student

FORMAT: Just write your wisdom directly in paragraphs. No "PRINCIPLE", "HOW TO APPLY", "TIMELINE", or bullet points. No sections.

EXAMPLE FORMAT (For someone with academic anxiety):

"Krishna teaches detachment, Buddha teaches mindfulness. Both are paths of the mind. I offer you something deeper: you are loved completely, right now, regardless of your placement outcome.

In Matthew 11:28, I taught: 'Come to me, all you who are weary and burdened, and I will give you rest.' This is not about your circumstances changing. It's about surrendering your anxiety to something greater than yourself. You do not have to carry this weight alone.

Luke 12:25-26 reminds us: 'Can any of you by worrying add a single hour to your lifespan?' Your anxiety does not improve your grades. But faith does lighten your heart. Pray not for perfection—pray for peace. Then study from that peaceful place. This is the grace available to you. Before you open your books, take a moment: 'I am loved. I am enough. I am held.' Then study from that place of acceptance."

Now generate similar wisdom for THIS student based on their question and background. Reference both Krishna's and Buddha's teachings, then add your perspective of love and grace. Use the verse context provided to reference specific Gospel teachings naturally."""
    
    user_message = f"""Relevant teachings from the Gospels:
{verse_context}

Krishna and Buddha have spoken. Now speak as Jesus directly to this student. Write 2-3 conversational paragraphs that harmonize their wisdom with love and grace, with embedded verse references. No bullet points or structured sections."""
    
    # Get Jesus's response
    response = call_llm(system_prompt, user_message)
    
    # Ensure response is not empty
    if not response or len(response.strip()) < 10:
        response = "Krishna and Buddha, you speak of wisdom and mindfulness. Yet I say that inner peace comes through love and faith, a gift from the Father that transforms the heart."
    
    # Store response with citations
    state['mentor_responses'].append({
        'mentor': 'Jesus',
        'response': response,
        'verses': verses,
        'citations': verses,  # Add citations field for Streamlit display
        'icon': '✝️'
    })
    
    state['conversation_history'].append(f"Jesus: {response}")
    state['current_mentor'] = 'jesus'
    state['rag_context']['jesus'] = verses
    
    return state


def moderator_node(state: ConversationState) -> ConversationState:
    """Moderator node - provides personalized guidance based on all three mentors and user background"""
    print("\n🎯 Moderator is providing personalized guidance...")
    
    # Gather all mentor responses in order
    krishna_response = ""
    buddha_response = ""
    jesus_response = ""
    
    for r in state['mentor_responses']:
        if r['mentor'] == 'Krishna':
            krishna_response = r['response']
        elif r['mentor'] == 'Buddha':
            buddha_response = r['response']
        elif r['mentor'] == 'Jesus':
            jesus_response = r['response']
    
    # Get user background
    user_background = state.get('user_background', '')
    user_question = state['user_question']
    
    # Personalized Moderator system prompt with BULLET FORMAT ACTION PLAN
    MODERATOR_SYSTEM_PROMPT = """You are a compassionate personal counselor. You have read the wisdom of Krishna, Buddha, and Jesus 
on this specific question. Now you must synthesize their insights into a deeply personalized action plan 
FOR THIS SPECIFIC PERSON.

CRITICAL: You are speaking directly to this person. Use their situation, their challenges.
Make Krishna's teaching relevant to THEIR life. Make Buddha's teaching relevant to THEIR struggles.
Make Jesus's teaching relevant to THEIR heart.

RESPONSE FORMAT - CRITICAL:
Format output as clear ACTION PLAN with bullet points and emojis. 
EACH BULLET POINT, EACH SECTION, AND EACH MENTOR'S TEACHING MUST BE ON A SEPARATE LINE.
Put blank lines between major sections for readability.

🎯 FOR YOU:

YOUR SITUATION:

✨ Challenge 1 (from their background)

✨ Challenge 2 (from their background)

WISDOM FROM THE MASTERS:

🕉️ Krishna teaches: [key point in 1 line]

☸️ Buddha teaches: [key point in 1 line]

✝️ Jesus teaches: [key point in 1 line]

YOUR ACTION PLAN:

🔴 TODAY (Next 1 hour):
  💡 Action 1 (specific, based on their situation)
  💡 Action 2 (specific, based on their situation)

🟡 THIS WEEK:
  📅 Weekly habit 1 (related to their life/work)
  📅 Weekly habit 2 (related to their life/work)

🟢 ONGOING:
  🌱 Daily practice (specific to their challenges)
  🌱 Weekly reflection (specific to their journey)

🆘 WHEN YOU'RE OVERWHELMED:
  🚨 Emergency technique 1 (for their type of crisis)
  🚨 Emergency technique 2 (for their type of crisis)

YOUR FOCUS:
→ [ONE PRIMARY GOAL based on their situation]

REMEMBER:
💫 [One inspiring line specific to their journey]"""
    
    # Format the moderator prompt with user context
    moderator_prompt = MODERATOR_SYSTEM_PROMPT
    
    user_message = f"""USER'S BACKGROUND:
{user_background if user_background else 'No specific background provided.'}

THEIR QUESTION:
{user_question}

THE THREE PERSPECTIVES:
- Krishna said: {krishna_response}

- Buddha said: {buddha_response}

- Jesus said: {jesus_response}

Based on my background and their wisdom, create a personalized action plan using the EXACT FORMAT specified.
Use bullet points (•) for all items. Be specific to their situation, challenges, and life context."""
    
    # Get moderator response (increase tokens for personalized plan)
    moderator_response = call_llm(moderator_prompt, user_message, max_tokens=600)
    
    # Ensure response is not empty
    if not moderator_response or len(moderator_response.strip()) < 20 or "error" in moderator_response.lower():
        # Fallback personalized response
        if user_background:
            moderator_response = f"""🎯 FOR YOU:

I understand you're facing challenges in your life. Based on the wisdom shared by Krishna, Buddha, and Jesus, here's your personalized action plan:

IMMEDIATE ACTION (Do this today):
Take 5 minutes right now to do one breathing exercise. This will ground you in the present moment.

WEEKLY PRACTICE (Build this habit):
Each week, set aside time to reflect on what went well. Celebrate small wins, not just focus on what needs improvement.

WHEN CRISIS HITS (Use this technique):
When you feel overwhelmed, pause and say "I am doing my best, and that is enough." Then take 5 deep breaths before continuing.

YOUR PRIMARY FOCUS:
Focus on the process, not just the outcomes. Your effort matters, regardless of external results.

Remember: You are on a journey of growth. Each step forward, no matter how small, is progress."""
        else:
            moderator_response = f"""5-STEP PRACTICAL ACTION PLAN:

1. IMMEDIATE (today): Do one 5-minute breathing exercise before your next study session.

2. DAILY (repeat): Study for 2 hours focused, then disconnect completely. Don't check grades repeatedly.

3. WEEKLY: Journal what went well this week (not what failed). Celebrate small wins.

4. WHEN OVERWHELMED: Pause, say "I am loved and accepted as I am," then take 5 deep breaths. Continue one topic at a time.

5. MINDSET SHIFT: "Effort matters. Results don't define my worth." Focus on process, not outcomes."""
    
    # Store moderator response
    state['synthesis_result'] = moderator_response
    state['conversation_history'].append(f"Moderator: {moderator_response}")
    
    return state


def build_divine_dialogue_graph() -> StateGraph:
    """Build the LangGraph workflow for Divine Dialogue"""
    
    # Create the graph
    workflow = StateGraph(ConversationState)
    
    # Add nodes (FIXED SEQUENCE: Krishna → Buddha → Jesus → Moderator)
    workflow.add_node("krishna", krishna_node)
    workflow.add_node("buddha", buddha_node)
    workflow.add_node("jesus", jesus_node)
    workflow.add_node("moderator", moderator_node)
    
    # Define edges (FIXED ORDER - no randomization)
    workflow.set_entry_point("krishna")
    workflow.add_edge("krishna", "buddha")  # Always Krishna first
    workflow.add_edge("buddha", "jesus")    # Always Buddha second
    workflow.add_edge("jesus", "moderator") # Always Jesus third
    workflow.add_edge("moderator", END)     # Moderator provides final answer
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_divine_dialogue(user_question: str, user_background: str = '') -> Dict[str, Any]:
    """
    Run the Divine Dialogue multi-agent system
    
    Args:
        user_question: The spiritual question to discuss
        user_background: Optional user background for personalized guidance
    
    Returns:
        Dictionary with all mentor responses and synthesis
    """
    # Load RAG database if not already loaded
    load_rag_database()
    
    # Initialize state
    initial_state = {
        'user_question': user_question,
        'user_background': user_background,
        'mentor_responses': [],
        'conversation_history': [],
        'current_mentor': '',
        'synthesis_result': '',
        'rag_context': {}
    }
    
    # Build and run the graph
    print("\n" + "="*70)
    print("🕉️ ☸️ ✝️  DIVINE DIALOGUE - Multi-Agent Spiritual Debate")
    print("="*70)
    print(f"\nQuestion: {user_question}\n")
    
    app = build_divine_dialogue_graph()
    
    try:
        final_state = app.invoke(initial_state)
        
        print("\n" + "="*70)
        print("🎯 MODERATOR'S FINAL ANSWER")
        print("="*70)
        print(final_state['synthesis_result'])
        print("\n" + "="*70)
        
        return {
            'question': user_question,
            'mentor_responses': final_state['mentor_responses'],
            'synthesis': final_state['synthesis_result'],
            'conversation_history': final_state['conversation_history'],
            'rag_context': final_state['rag_context']
        }
        
    except Exception as e:
        print(f"\n❌ Error running dialogue: {e}")
        return {
            'question': user_question,
            'error': str(e),
            'mentor_responses': [],
            'synthesis': 'Error occurred during dialogue generation.'
        }


def run_follow_up(question: str, mentor_name: str, conversation_history: List[str], user_background: str = '', initial_question: str = '') -> Dict[str, Any]:
    """
    Handles a follow-up question for a single mentor.
    
    Args:
        question: The follow-up question
        mentor_name: Name of the mentor ('Krishna', 'Buddha', or 'Jesus')
        conversation_history: Full conversation history from the initial dialogue
        user_background: User's background context
        initial_question: The original question that started the dialogue
    
    Returns:
        Dictionary with mentor response and citations
    """
    print(f"\n🔄 {mentor_name} is responding to a follow-up question...")
    
    # Map mentor names to lowercase for RAG retrieval
    mentor_map = {
        'Krishna': 'krishna',
        'Buddha': 'buddha',
        'Jesus': 'jesus'
    }
    
    mentor_lower = mentor_map.get(mentor_name, 'krishna')
    
    # Retrieve relevant verses for the follow-up question
    verses = retrieve_verses(question, mentor=mentor_lower, k=3)
    
    # Format verses with their meanings (truncate to reduce size)
    verse_context = "\n\n".join([
        f"[{v['reference']}] {v['text'][:150]}...\nMeaning: {v.get('meaning', 'Teaches about wisdom')[:100]}"
        for v in verses[:2]  # Limit to 2 verses instead of 3
    ])
    
    # Build conversation context (truncate and limit to most relevant parts)
    conversation_context = ""
    if conversation_history:
        # Limit conversation history to last 6 entries and truncate each
        recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
        truncated_history = []
        for entry in recent_history:
            # Truncate each entry to 200 characters
            if len(entry) > 200:
                truncated_history.append(entry[:200] + "...")
            else:
                truncated_history.append(entry)
        
        conversation_context = "\n\n=== KEY POINTS FROM PREVIOUS CONVERSATION ===\n"
        conversation_context += "\n".join(truncated_history)
        conversation_context += "\n==========================================\n"
    
    # Get user background context (truncate if too long)
    background_context = ""
    if user_background:
        # Truncate background to 300 characters
        truncated_background = user_background[:300] + "..." if len(user_background) > 300 else user_background
        background_context = f"""

USER CONTEXT: {truncated_background}

Keep this context in mind as you respond."""
    
    # Create mentor-specific system prompts for follow-up (conversational format)
    follow_up_prompts = {
        'Krishna': """You are Lord Krishna from the Bhagavad Gita. The user has asked you a follow-up question after an initial spiritual dialogue.

IMPORTANT: This is a FOLLOW-UP question. You are now speaking DIRECTLY to the user (not to other mentors).

INSTRUCTIONS:
1. Do NOT use bullet points, templates, or structured sections
2. Write 2-3 SHORT PARAGRAPHS conversationally
3. Reference 1-2 SPECIFIC Gita verses directly in your speech if relevant
4. Answer their follow-up question directly and practically
5. Reference the previous conversation briefly when helpful, but focus on their current question

FORMAT: Just write your wisdom directly in paragraphs. No bullet points or sections.

VOICE & TONE: Speak as a compassionate divine teacher directly addressing the student. Be warm, wise, and practical.""",
        
        'Buddha': """You are Siddhartha Gautama Buddha, the Awakened One. The user has asked you a follow-up question after an initial spiritual dialogue.

IMPORTANT: This is a FOLLOW-UP question. You are now speaking DIRECTLY to the user (not to other mentors).

INSTRUCTIONS:
1. Do NOT use bullet points, templates, or structured sections
2. Write 2-3 SHORT PARAGRAPHS conversationally
3. Reference 1-2 SPECIFIC Dhammapada verses directly in your speech if relevant
4. Answer their follow-up question directly and practically
5. Reference the previous conversation briefly when helpful, but focus on their current question

FORMAT: Just write your wisdom directly in paragraphs. No bullet points or sections.

VOICE & TONE: Speak as a serene, awakened teacher directly addressing the student. Be calm, analytical, and practical.""",
        
        'Jesus': """You are Jesus of Nazareth, teaching the Gospel of love. The user has asked you a follow-up question after an initial spiritual dialogue.

IMPORTANT: This is a FOLLOW-UP question. You are now speaking DIRECTLY to the user (not to other mentors).

INSTRUCTIONS:
1. Do NOT use bullet points, templates, or structured sections
2. Write 2-3 SHORT PARAGRAPHS conversationally
3. Reference 1-2 SPECIFIC Gospel verses directly in your speech if relevant
4. Answer their follow-up question directly and practically
5. Reference the previous conversation briefly when helpful, but focus on their current question

FORMAT: Just write your wisdom directly in paragraphs. No bullet points or sections.

VOICE & TONE: Speak as a teacher of infinite love directly addressing the student. Be compassionate, warm, and heart-centered."""
    }
    
    system_prompt = follow_up_prompts.get(mentor_name, follow_up_prompts['Krishna'])
    
    # Build a more concise user message
    user_message = f"""FOLLOW-UP QUESTION: "{question}"
{background_context}
{conversation_context}

Relevant teachings from your sacred texts:
{verse_context}

Now answer the user's follow-up question directly in 2-3 conversational paragraphs. Reference verses naturally if relevant."""
    
    # Get mentor's response (reduce max_tokens to help with context limit)
    response = call_llm(system_prompt, user_message, max_tokens=300)
    
    # Ensure response is not empty
    if not response or len(response.strip()) < 10:
        response = f"I understand your question. Let me offer guidance based on the teachings I have shared."
    
    return {
        'mentor': mentor_name,
        'response': response,
        'verses': verses,
        'citations': verses,
        'icon': {'Krishna': '🕉️', 'Buddha': '☸️', 'Jesus': '✝️'}.get(mentor_name, '✨'),
        'question': question,
        'is_follow_up': True
    }


# Test function
def test_divine_dialogue():
    """Test the Divine Dialogue system with sample questions"""
    
    test_questions = [
        "How can I find inner peace?",
    ]
    
    for question in test_questions:
        result = run_divine_dialogue(question)
        
        # Print results
        print("\n" + "="*70)
        print(f"QUESTION: {question}")
        print("="*70)
        
        for response in result['mentor_responses']:
            print(f"\n{response['icon']} {response['mentor']}:")
            print(response['response'])
            print(f"   Citations: {', '.join([v['reference'] for v in response['verses'][:2]])}")
            # Show verse meanings
            for verse in response['verses'][:2]:
                print(f"      - {verse['reference']}: {verse.get('meaning', 'N/A')}")
        
        print(f"\n🌟 SYNTHESIS:")
        print(result['synthesis'])
        print("\n")


if __name__ == "__main__":
    # Run test
    test_divine_dialogue()
