#!/usr/bin/env python3
"""
Quick test script for Divine Dialogue system
Tests the LangGraph multi-agent orchestration
"""

import os
from divine_dialogue_langgraph import run_divine_dialogue

def test_single_question():
    """Test with a single question"""
    
    # Check if API key is set
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_api_key_here":
        print("⚠️  WARNING: OPENROUTER_API_KEY not set in .env file")
        print("   Please add your OpenRouter API key to continue.")
        print("   Get one free at: https://openrouter.ai/")
        return
    
    print("\n" + "="*70)
    print("🧪 TESTING DIVINE DIALOGUE SYSTEM")
    print("="*70)
    
    # Test question
    question = "How can I find inner peace in times of suffering?"
    
    print(f"\n📝 Test Question: {question}\n")
    
    # Run dialogue
    result = run_divine_dialogue(question)
    
    # Display results
    if 'error' not in result:
        print("\n" + "="*70)
        print("✅ TEST SUCCESSFUL - All mentors responded!")
        print("="*70)
        
        print("\n📊 RESULTS SUMMARY:")
        print(f"  • Question: {result['question']}")
        print(f"  • Mentors: {len(result['mentor_responses'])}")
        print(f"  • Synthesis: {'✓' if result['synthesis'] else '✗'}")
        
        print("\n💬 MENTOR RESPONSES:")
        for response in result['mentor_responses']:
            print(f"\n  {response['icon']} {response['mentor']}:")
            print(f"     {response['response'][:100]}...")
            print(f"     Citations: {len(response['verses'])} verses")
        
        print(f"\n  🌟 Synthesis:")
        print(f"     {result['synthesis'][:150]}...")
        
        print("\n" + "="*70)
        print("✅ Divine Dialogue system is working correctly!")
        print("="*70)
        print("\n🚀 Next step: Run the Streamlit app with:")
        print("   streamlit run streamlit_app.py")
        print()
        
    else:
        print("\n" + "="*70)
        print("❌ TEST FAILED")
        print("="*70)
        print(f"Error: {result['error']}")
        print()


if __name__ == "__main__":
    test_single_question()
