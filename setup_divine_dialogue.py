#!/usr/bin/env python3
"""
Divine Dialogue Setup Script
Checks dependencies and configuration
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor} (need 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = [
        'faiss',
        'sentence_transformers',
        'langgraph',
        'openai',
        'streamlit',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def check_rag_database():
    """Check if RAG database exists"""
    print("\n🗄️  Checking RAG database...")
    
    db_path = Path('sacred_texts_rag_faiss')
    
    if not db_path.exists():
        print("   ✗ RAG database not found")
        print("   Run: python build_rag_database.py")
        return False
    
    required_files = ['index.faiss', 'texts.json', 'metadatas.json']
    missing = []
    
    for file in required_files:
        file_path = db_path / file
        if file_path.exists():
            size = file_path.stat().st_size / (1024 * 1024)  # MB
            print(f"   ✓ {file} ({size:.1f} MB)")
        else:
            print(f"   ✗ {file} (missing)")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        print("   Run: python build_rag_database.py")
        return False
    
    return True

def check_api_key():
    """Check if OpenRouter API key is configured"""
    print("\n🔑 Checking API configuration...")
    
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ✗ .env file not found")
        print("   Create .env file with: OPENROUTER_API_KEY=your_key_here")
        return False
    
    # Read .env file
    with open(env_path, 'r') as f:
        content = f.read()
    
    if 'OPENROUTER_API_KEY' not in content:
        print("   ✗ OPENROUTER_API_KEY not in .env")
        return False
    
    # Check if it's the placeholder
    if 'your_openrouter_api_key_here' in content:
        print("   ⚠️  API key is still placeholder")
        print("   Get your free key at: https://openrouter.ai/")
        print("   Then update .env file")
        return False
    
    print("   ✓ API key configured")
    return True

def check_data_files():
    """Check if source data files exist"""
    print("\n📚 Checking source data files...")
    
    data_dir = Path('sacred-scriptures-mcp/data')
    
    if not data_dir.exists():
        print("   ✗ Data directory not found")
        return False
    
    required_files = [
        'bhagavad_gita_verses.json',
        'dhammapada.json',
        'kjv_bible.json'
    ]
    
    all_exist = True
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            size = file_path.stat().st_size / (1024 * 1024)  # MB
            print(f"   ✓ {file} ({size:.1f} MB)")
        else:
            print(f"   ✗ {file} (missing)")
            all_exist = False
    
    return all_exist

def print_summary(checks):
    """Print setup summary"""
    print("\n" + "="*70)
    print("📊 SETUP SUMMARY")
    print("="*70)
    
    all_passed = all(checks.values())
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    print("="*70)
    
    if all_passed:
        print("\n✅ ALL CHECKS PASSED!")
        print("\n🚀 You're ready to run Divine Dialogue:")
        print("\n   1. Test the system:")
        print("      python test_divine_dialogue.py")
        print("\n   2. Launch the web app:")
        print("      streamlit run streamlit_app.py")
        print()
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running Divine Dialogue.")
        print()

def main():
    """Run all setup checks"""
    print("\n" + "="*70)
    print("🕉️ ☸️ ✝️  DIVINE DIALOGUE - SETUP CHECK")
    print("="*70)
    
    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Source Data Files': check_data_files(),
        'RAG Database': check_rag_database(),
        'API Configuration': check_api_key()
    }
    
    print_summary(checks)

if __name__ == "__main__":
    main()
