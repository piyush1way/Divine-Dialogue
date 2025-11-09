#!/usr/bin/env python3
"""
PHASE 3: Comprehensive Integration & Testing Suite
Tests RAG, LangGraph, and Streamlit components
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Test results tracking
test_results = {
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'tests': []
}


def log_test(name, status, message=""):
    """Log test result"""
    test_results['tests'].append({
        'name': name,
        'status': status,
        'message': message
    })
    
    if status == 'PASS':
        test_results['passed'] += 1
        print(f"  ✅ {name}")
    elif status == 'FAIL':
        test_results['failed'] += 1
        print(f"  ❌ {name}")
        if message:
            print(f"     Error: {message}")
    elif status == 'WARN':
        test_results['warnings'] += 1
        print(f"  ⚠️  {name}")
        if message:
            print(f"     Warning: {message}")


def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


# ============================================================================
# PHASE 3.1: TEST RAG INTEGRATION
# ============================================================================

def test_rag_integration():
    """Test RAG database integration"""
    print_section("PHASE 3.1: RAG INTEGRATION TESTS")
    
    # Test 1: Verify FAISS loads correctly
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
        
        db_path = Path('sacred_texts_rag_faiss')
        
        # Check database exists
        if not db_path.exists():
            log_test("FAISS Database Exists", "FAIL", "Database directory not found")
            return
        
        # Load index
        index = faiss.read_index(str(db_path / 'index.faiss'))
        log_test("FAISS Index Loads", "PASS", f"Loaded {index.ntotal} vectors")
        
        # Load texts
        with open(db_path / 'texts.json', 'r', encoding='utf-8') as f:
            texts = json.load(f)
        log_test("Texts JSON Loads", "PASS", f"Loaded {len(texts)} texts")
        
        # Load metadata
        with open(db_path / 'metadatas.json', 'r', encoding='utf-8') as f:
            metadatas = json.load(f)
        log_test("Metadata JSON Loads", "PASS", f"Loaded {len(metadatas)} metadata entries")
        
        # Verify counts match
        if index.ntotal == len(texts) == len(metadatas):
            log_test("Vector/Text/Metadata Count Match", "PASS", f"All have {index.ntotal} entries")
        else:
            log_test("Vector/Text/Metadata Count Match", "FAIL", 
                    f"Mismatch: {index.ntotal} vs {len(texts)} vs {len(metadatas)}")
        
        # Load embedding model
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        log_test("Embedding Model Loads", "PASS", "Model loaded successfully")
        
        # Test 2: Test retrieval for each mentor
        print("\n  Testing retrieval for each mentor:")
        
        test_query = "How can I find peace?"
        query_embedding = model.encode([test_query], convert_to_numpy=True)
        
        for mentor in ['krishna', 'buddha', 'jesus']:
            # Search
            distances, indices = index.search(query_embedding.astype('float32'), 50)
            
            # Filter by mentor
            mentor_results = []
            for idx, dist in zip(indices[0], distances[0]):
                if metadatas[idx]['mentor'] == mentor:
                    mentor_results.append({
                        'text': texts[idx],
                        'metadata': metadatas[idx],
                        'distance': dist
                    })
                    if len(mentor_results) >= 3:
                        break
            
            if len(mentor_results) >= 3:
                log_test(f"Retrieve {mentor.title()} verses", "PASS", 
                        f"Found {len(mentor_results)} verses")
            else:
                log_test(f"Retrieve {mentor.title()} verses", "WARN", 
                        f"Only found {len(mentor_results)} verses")
        
        # Test 3: Verify metadata filtering works
        print("\n  Testing metadata filtering:")
        
        mentor_counts = {'krishna': 0, 'buddha': 0, 'jesus': 0}
        for metadata in metadatas:
            mentor = metadata.get('mentor', 'unknown')
            if mentor in mentor_counts:
                mentor_counts[mentor] += 1
        
        expected_counts = {
            'krishna': 701,
            'buddha': 423,
            'jesus': 3779
        }
        
        for mentor, count in mentor_counts.items():
            expected = expected_counts[mentor]
            if count == expected:
                log_test(f"Metadata filter: {mentor.title()}", "PASS", 
                        f"{count} verses (expected {expected})")
            else:
                log_test(f"Metadata filter: {mentor.title()}", "WARN", 
                        f"{count} verses (expected {expected})")
        
        # Test verse structure
        sample_metadata = metadatas[0]
        required_fields = ['mentor', 'source', 'reference']
        
        if all(field in sample_metadata for field in required_fields):
            log_test("Metadata Structure", "PASS", "All required fields present")
        else:
            missing = [f for f in required_fields if f not in sample_metadata]
            log_test("Metadata Structure", "FAIL", f"Missing fields: {missing}")
        
    except ImportError as e:
        log_test("Import Dependencies", "FAIL", str(e))
    except Exception as e:
        log_test("RAG Integration", "FAIL", str(e))


# ============================================================================
# PHASE 3.2: TEST LANGGRAPH WORKFLOW
# ============================================================================

def test_langgraph_workflow():
    """Test LangGraph multi-agent workflow"""
    print_section("PHASE 3.2: LANGGRAPH WORKFLOW TESTS")
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_api_key_here":
        log_test("API Key Configuration", "FAIL", "OPENROUTER_API_KEY not set")
        print("\n  ⚠️  Skipping LangGraph tests - API key required")
        print("     Get free key at: https://openrouter.ai/")
        return
    
    log_test("API Key Configuration", "PASS", "API key is set")
    
    try:
        from divine_dialogue_langgraph import run_divine_dialogue, load_rag_database
        log_test("Import LangGraph Module", "PASS")
        
        # Load RAG database
        print("\n  Loading RAG database...")
        load_rag_database()
        log_test("Load RAG Database", "PASS")
        
        # Test with sample questions
        sample_questions = [
            "How can I find inner peace?",
            "What is the purpose of life?",
            "How should I treat others?"
        ]
        
        print("\n  Testing with sample questions:")
        
        for i, question in enumerate(sample_questions[:1], 1):  # Test with 1 question to save time
            print(f"\n  Question {i}: {question}")
            
            try:
                result = run_divine_dialogue(question)
                
                # Verify no error
                if 'error' in result:
                    log_test(f"Question {i}: No Error", "FAIL", result['error'])
                    continue
                else:
                    log_test(f"Question {i}: No Error", "PASS")
                
                # Verify all three mentors respond
                if len(result['mentor_responses']) == 3:
                    log_test(f"Question {i}: Three Mentors Respond", "PASS")
                else:
                    log_test(f"Question {i}: Three Mentors Respond", "FAIL", 
                            f"Only {len(result['mentor_responses'])} mentors responded")
                
                # Verify mentor names
                expected_mentors = {'Krishna', 'Buddha', 'Jesus'}
                actual_mentors = {r['mentor'] for r in result['mentor_responses']}
                
                if expected_mentors == actual_mentors:
                    log_test(f"Question {i}: Correct Mentors", "PASS")
                else:
                    log_test(f"Question {i}: Correct Mentors", "FAIL", 
                            f"Expected {expected_mentors}, got {actual_mentors}")
                
                # Verify synthesis is generated
                if result.get('synthesis') and len(result['synthesis']) > 0:
                    log_test(f"Question {i}: Synthesis Generated", "PASS", 
                            f"{len(result['synthesis'])} characters")
                else:
                    log_test(f"Question {i}: Synthesis Generated", "FAIL", 
                            "Synthesis is empty")
                
                # Check response coherence
                print("\n  Checking response coherence:")
                
                for response in result['mentor_responses']:
                    mentor = response['mentor']
                    text = response['response']
                    verses = response['verses']
                    
                    # Check response length
                    if len(text) > 20:
                        log_test(f"  {mentor}: Response Length", "PASS", 
                                f"{len(text)} characters")
                    else:
                        log_test(f"  {mentor}: Response Length", "WARN", 
                                f"Only {len(text)} characters")
                    
                    # Check verses retrieved
                    if len(verses) > 0:
                        log_test(f"  {mentor}: Verses Retrieved", "PASS", 
                                f"{len(verses)} verses")
                    else:
                        log_test(f"  {mentor}: Verses Retrieved", "FAIL", 
                                "No verses retrieved")
                    
                    # Check verse structure
                    if verses and all('reference' in v and 'text' in v for v in verses):
                        log_test(f"  {mentor}: Verse Structure", "PASS")
                    else:
                        log_test(f"  {mentor}: Verse Structure", "FAIL", 
                                "Missing reference or text")
                
                # Test conversation history
                if 'conversation_history' in result and len(result['conversation_history']) > 0:
                    log_test(f"Question {i}: Conversation History", "PASS", 
                            f"{len(result['conversation_history'])} entries")
                else:
                    log_test(f"Question {i}: Conversation History", "WARN", 
                            "No conversation history")
                
            except Exception as e:
                log_test(f"Question {i}: Execution", "FAIL", str(e))
        
    except ImportError as e:
        log_test("Import LangGraph Module", "FAIL", str(e))
    except Exception as e:
        log_test("LangGraph Workflow", "FAIL", str(e))


# ============================================================================
# PHASE 3.3: TEST STREAMLIT APP
# ============================================================================

def test_streamlit_app():
    """Test Streamlit application"""
    print_section("PHASE 3.3: STREAMLIT APP TESTS")
    
    try:
        import streamlit
        log_test("Streamlit Installed", "PASS", f"Version {streamlit.__version__}")
    except ImportError:
        log_test("Streamlit Installed", "FAIL", "Streamlit not installed")
        return
    
    # Check app files exist
    app_files = ['app.py', 'streamlit_app.py']
    
    for app_file in app_files:
        if Path(app_file).exists():
            log_test(f"App File: {app_file}", "PASS")
            
            # Check file size
            size = Path(app_file).stat().st_size
            if size > 1000:
                log_test(f"  {app_file} Size", "PASS", f"{size/1024:.1f} KB")
            else:
                log_test(f"  {app_file} Size", "WARN", f"Only {size} bytes")
            
            # Check for key components
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_elements = [
                ('st.set_page_config', 'Page Configuration'),
                ('st.text_area', 'Text Input'),
                ('st.button', 'Button'),
                ('run_divine_dialogue', 'Backend Integration')
            ]
            
            for element, description in required_elements:
                if element in content:
                    log_test(f"  {app_file}: {description}", "PASS")
                else:
                    log_test(f"  {app_file}: {description}", "WARN", 
                            f"{element} not found")
        else:
            log_test(f"App File: {app_file}", "FAIL", "File not found")
    
    # Test error handling in app
    print("\n  Checking error handling:")
    
    for app_file in app_files:
        if Path(app_file).exists():
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            error_handling = [
                ('try:', 'Try-Except Blocks'),
                ('except', 'Exception Handling'),
                ('st.error', 'Error Display'),
                ('st.warning', 'Warning Display')
            ]
            
            for pattern, description in error_handling:
                if pattern in content:
                    log_test(f"  {app_file}: {description}", "PASS")
                else:
                    log_test(f"  {app_file}: {description}", "WARN", 
                            f"{pattern} not found")
    
    # Check UI elements
    print("\n  Checking UI elements:")
    
    ui_elements = [
        ('st.header', 'Headers'),
        ('st.markdown', 'Markdown/Styling'),
        ('st.spinner', 'Loading Indicators'),
        ('st.expander', 'Expandable Sections'),
        ('st.download_button', 'Download Functionality')
    ]
    
    for app_file in app_files:
        if Path(app_file).exists():
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for element, description in ui_elements:
                if element in content:
                    log_test(f"  {app_file}: {description}", "PASS")


# ============================================================================
# ADDITIONAL TESTS
# ============================================================================

def test_dependencies():
    """Test all required dependencies"""
    print_section("ADDITIONAL: DEPENDENCY TESTS")
    
    dependencies = [
        ('faiss', 'FAISS'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('langgraph', 'LangGraph'),
        ('openai', 'OpenAI Client'),
        ('streamlit', 'Streamlit'),
        ('dotenv', 'Python Dotenv')
    ]
    
    for module, name in dependencies:
        try:
            __import__(module)
            log_test(f"Dependency: {name}", "PASS")
        except ImportError:
            log_test(f"Dependency: {name}", "FAIL", f"{module} not installed")


def test_file_structure():
    """Test project file structure"""
    print_section("ADDITIONAL: FILE STRUCTURE TESTS")
    
    required_files = [
        ('divine_dialogue_langgraph.py', 'LangGraph Backend'),
        ('app.py', 'Enhanced Streamlit App'),
        ('streamlit_app.py', 'Original Streamlit App'),
        ('build_rag_database.py', 'RAG Builder'),
        ('requirements.txt', 'Dependencies'),
        ('.env', 'Environment Config'),
        ('README.md', 'Documentation')
    ]
    
    for filename, description in required_files:
        if Path(filename).exists():
            log_test(f"File: {description}", "PASS", filename)
        else:
            log_test(f"File: {description}", "WARN", f"{filename} not found")
    
    # Check RAG database directory
    if Path('sacred_texts_rag_faiss').exists():
        log_test("RAG Database Directory", "PASS")
        
        rag_files = ['index.faiss', 'texts.json', 'metadatas.json']
        for rag_file in rag_files:
            if (Path('sacred_texts_rag_faiss') / rag_file).exists():
                log_test(f"  RAG File: {rag_file}", "PASS")
            else:
                log_test(f"  RAG File: {rag_file}", "FAIL", "Missing")
    else:
        log_test("RAG Database Directory", "FAIL", "Not found")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def print_summary():
    """Print test summary"""
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    total = test_results['passed'] + test_results['failed'] + test_results['warnings']
    
    print(f"\n  Total Tests: {total}")
    print(f"  ✅ Passed:   {test_results['passed']}")
    print(f"  ❌ Failed:   {test_results['failed']}")
    print(f"  ⚠️  Warnings: {test_results['warnings']}")
    
    if test_results['failed'] == 0:
        print("\n  🎉 ALL CRITICAL TESTS PASSED!")
        status = "READY FOR DEMO"
    elif test_results['failed'] < 5:
        print("\n  ⚠️  SOME TESTS FAILED - Review and fix")
        status = "NEEDS ATTENTION"
    else:
        print("\n  ❌ MULTIPLE FAILURES - System not ready")
        status = "NOT READY"
    
    print(f"\n  Status: {status}")
    print("="*70)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total': total,
                'passed': test_results['passed'],
                'failed': test_results['failed'],
                'warnings': test_results['warnings'],
                'status': status
            },
            'tests': test_results['tests']
        }, f, indent=2)
    
    print(f"\n  📄 Detailed report saved to: {report_file}")
    print()


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  🧪 DIVINE DIALOGUE - COMPREHENSIVE TEST SUITE")
    print("  Phase 3: Integration & Testing")
    print("="*70)
    print(f"\n  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all test phases
    test_dependencies()
    test_file_structure()
    test_rag_integration()
    test_langgraph_workflow()
    test_streamlit_app()
    
    # Print summary
    print_summary()
    
    # Return exit code
    return 0 if test_results['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
