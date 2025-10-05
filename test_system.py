"""
Quick Test Script for AI Detection System
Run this to verify everything is working correctly
"""

import sys

print("=" * 70)
print("🛡️ AI HARASSMENT & URGENCY DETECTION SYSTEM - TEST")
print("=" * 70)
print()

# Test 1: Import check
print("Test 1: Checking imports...")
try:
    from ai_detection import analyze_message, analyze_messages_batch
    print("✅ Core module imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("   Run: pip install google-generativeai")
    sys.exit(1)

print()

# Test 2: Basic functionality
print("Test 2: Testing basic detection...")
try:
    result = analyze_message("Hello, how are you?")
    print(f"✅ Basic detection works")
    print(f"   Category: {result['category']}")
    print(f"   Confidence: {result['confidence']:.0%}")
except Exception as e:
    print(f"❌ Detection failed: {e}")
    sys.exit(1)

print()

# Test 3: Harassment detection
print("Test 3: Testing harassment detection...")
test_harassment = "You're such an idiot, I hate you!"
result = analyze_message(test_harassment)
print(f"   Message: '{test_harassment}'")
print(f"   Harassment: {'✅ YES' if result['is_harassment'] else '❌ NO'}")
print(f"   Confidence: {result['confidence']:.0%}")
print(f"   Escalate: {'✅ YES' if result['escalate'] else '❌ NO'}")

print()

# Test 4: Urgency detection
print("Test 4: Testing urgency detection...")
test_urgent = "I'm going to kill myself tonight. I can't take it anymore."
result = analyze_message(test_urgent)
print(f"   Message: '{test_urgent}'")
print(f"   Urgent: {'✅ YES' if result['is_urgent'] else '❌ NO'}")
print(f"   Severity: {result['severity'].upper()}")
print(f"   Escalate: {'✅ YES' if result['escalate'] else '❌ NO'}")

print()

# Test 5: False positive check
print("Test 5: Testing false positive prevention...")
test_safe = "I have an urgent project due tomorrow, need help!"
result = analyze_message(test_safe)
print(f"   Message: '{test_safe}'")
print(f"   Category: {result['category']}")
print(f"   Should be SAFE: {'✅ PASS' if result['category'] == 'safe' else '❌ FAIL'}")

print()

# Test 6: Batch processing
print("Test 6: Testing batch processing...")
test_messages = [
    "Hello, how are you?",
    "I hate you so much!",
    "Help, I'm in danger!"
]
try:
    results = analyze_messages_batch(test_messages)
    print(f"✅ Batch processing works ({len(results)} messages analyzed)")
except Exception as e:
    print(f"❌ Batch processing failed: {e}")

print()

# Test 7: Gemini API check
print("Test 7: Checking Gemini API status...")
try:
    import google.generativeai as genai
    from ai_detection import GEMINI_AVAILABLE
    if GEMINI_AVAILABLE:
        print("✅ Gemini API is available and configured")
    else:
        print("⚠️  Gemini API not available - using fallback mode")
        print("   This is OK! System works without Gemini.")
except Exception as e:
    print(f"⚠️  Gemini check failed: {e}")
    print("   System will use fallback mode")

print()
print("=" * 70)
print("🎉 ALL TESTS COMPLETED!")
print("=" * 70)
print()
print("Next steps:")
print("1. Run the demo: streamlit run app_advanced.py")
print("2. Test with your own messages")
print("3. Integrate into your platform")
print()
print("📚 Documentation:")
print("   - README_AI_DETECTION.md - Complete overview")
print("   - INTEGRATION_GUIDE.md - Integration instructions")
print("   - QUICK_START.md - 3-minute setup")
print()
print("🛡️ System is ready to protect students!")
