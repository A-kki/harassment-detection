"""
AI Harassment & Urgency Detection System
==========================================
Two-layer detection: Keyword classifier + Gemini context filter
Optimized for Student Cyber Safety Platform
"""

import re
import os
from typing import Dict, List, Tuple
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    GEMINI_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Gemini API not available: {e}")
    model = None
    GEMINI_AVAILABLE = False

# ============================================
# KEYWORD DATABASES
# ============================================

# 🚨 Harassment keywords (high severity)
HARASSMENT_KEYWORDS = [
    'harass', 'threat', 'kill', 'hate', 'abuse', 'attack', 'blackmail',
    'bully', 'hurt', 'harm', 'stalk', 'rape', 'assault', 'violence',
    'beat up', 'destroy you', 'ruin your life', 'expose you', 'leak your',
    'revenge', 'get back at', 'make you pay', 'regret this'
]

# 🆘 Urgent/Emergency keywords (requires immediate action)
URGENT_KEYWORDS = [
    'help', 'emergency', 'suicide', 'kill myself', 'end my life', 'want to die',
    'self harm', 'cutting', 'overdose', 'danger', 'scared', 'afraid',
    'threatening me', 'going to hurt', 'right now', 'tonight', 'today',
    'can\'t take it anymore', 'no way out', 'goodbye forever'
]

# ✅ Neutral/Academic keywords (reduces false positives)
NEUTRAL_KEYWORDS = [
    'assignment', 'exam', 'project', 'deadline', 'homework', 'study',
    'test', 'quiz', 'presentation', 'essay', 'report', 'class',
    'urgent project', 'urgent assignment', 'urgent homework', 'due tomorrow'
]

# 🔴 Severe threat patterns (immediate escalation)
SEVERE_PATTERNS = [
    r'\b(kill|murder|shoot|stab)\s+(you|myself|someone)',
    r'\b(suicide|kill myself|end my life)',
    r'\b(have a gun|have a knife|have a weapon)',
    r'\b(going to|gonna|will)\s+(hurt|harm|kill|attack)',
    r'\b(rape|sexual assault|molest)',
    r'\b(bomb|explosive|blow up)'
]


# ============================================
# LAYER 1: KEYWORD-BASED CLASSIFIER
# ============================================

def base_classifier(message: str) -> Dict:
    """
    Lightweight keyword-based detection
    Returns harassment and urgency scores
    """
    text = message.lower()
    
    # Count keyword matches
    harassment_score = sum(1 for keyword in HARASSMENT_KEYWORDS if keyword in text)
    urgency_score = sum(1 for keyword in URGENT_KEYWORDS if keyword in text)
    neutral_score = sum(1 for keyword in NEUTRAL_KEYWORDS if keyword in text)
    
    # Check for severe patterns
    severe_match = any(re.search(pattern, text) for pattern in SEVERE_PATTERNS)
    
    # Calculate confidence scores (0-1 scale)
    harassment_confidence = min(harassment_score / 3, 1.0)  # Cap at 1.0
    urgency_confidence = min(urgency_score / 3, 1.0)
    
    # Adjust for neutral context (reduce false positives)
    if neutral_score > 0:
        harassment_confidence *= 0.5
        urgency_confidence *= 0.5
    
    # Severe patterns override everything
    if severe_match:
        harassment_confidence = max(harassment_confidence, 0.95)
        urgency_confidence = max(urgency_confidence, 0.95)
    
    return {
        'harassment_confidence': harassment_confidence,
        'urgency_confidence': urgency_confidence,
        'is_potential_harassment': harassment_confidence > 0.2,
        'is_potential_urgent': urgency_confidence > 0.2,
        'has_severe_pattern': severe_match,
        'neutral_context': neutral_score > 0
    }


# ============================================
# LAYER 2: GEMINI CONTEXT VERIFIER
# ============================================

def context_verifier_gemini(message: str) -> Tuple[bool, str]:
    """
    Uses Gemini AI to verify if message is truly harassment/urgent
    Returns (is_real_threat, explanation)
    """
    if not GEMINI_AVAILABLE:
        return context_verifier_fallback(message)
    
    try:
        prompt = f"""
You are a cyber safety AI for a student platform. Analyze this message carefully.

Message: "{message}"

Determine:
1. Is this REAL harassment, threat, or emergency requiring immediate escalation?
2. Or is it a false positive (like "urgent homework" or casual language)?

Consider context:
- Student language patterns
- Academic urgency vs real danger
- Casual vs serious threats

Respond in this exact format:
THREAT: [true/false]
REASON: [brief explanation]
"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Parse response
        is_threat = 'THREAT: true' in result_text.lower()
        
        # Extract reason
        reason_match = re.search(r'REASON:\s*(.+)', result_text, re.IGNORECASE)
        reason = reason_match.group(1) if reason_match else "AI analysis completed"
        
        return is_threat, reason
        
    except Exception as e:
        print(f"⚠️ Gemini verification failed: {e}")
        return context_verifier_fallback(message)


def context_verifier_fallback(message: str) -> Tuple[bool, str]:
    """
    Rule-based fallback when Gemini is unavailable
    More conservative approach
    """
    text = message.lower()
    
    # Check for severe patterns first
    if any(re.search(pattern, text) for pattern in SEVERE_PATTERNS):
        return True, "Severe threat pattern detected"
    
    # Check if urgent words present WITHOUT neutral context
    has_urgent = any(word in text for word in URGENT_KEYWORDS)
    has_neutral = any(word in text for word in NEUTRAL_KEYWORDS)
    
    if has_urgent and not has_neutral:
        return True, "Urgent keywords detected without academic context"
    
    # Check for harassment without neutral context
    harassment_count = sum(1 for word in HARASSMENT_KEYWORDS if word in text)
    if harassment_count >= 2 and not has_neutral:
        return True, "Multiple harassment indicators detected"
    
    return False, "Likely false positive or normal message"


# ============================================
# MAIN ANALYSIS FUNCTION
# ============================================

def analyze_message(message: str) -> Dict:
    """
    Combined two-layer detection system
    
    Args:
        message: User message to analyze
        
    Returns:
        {
            'is_harassment': bool,
            'is_urgent': bool,
            'confidence': float (0-1),
            'escalate': bool,
            'category': str,
            'reason': str,
            'severity': str (low/medium/high/critical)
        }
    """
    
    # Layer 1: Keyword classification
    base_result = base_classifier(message)
    
    # Layer 2: Context verification (only if potential threat detected)
    context_valid = False
    reason = "Message appears safe"
    
    if base_result['is_potential_harassment'] or base_result['is_potential_urgent']:
        context_valid, reason = context_verifier_gemini(message)
    
    # Determine final classification
    is_harassment = base_result['is_potential_harassment'] and context_valid
    is_urgent = base_result['is_potential_urgent'] and context_valid
    
    # Calculate overall confidence
    confidence = max(
        base_result['harassment_confidence'],
        base_result['urgency_confidence']
    )
    
    # Severe patterns always escalate
    if base_result['has_severe_pattern']:
        is_harassment = True
        is_urgent = True
        confidence = 0.95
        escalate = True
        severity = 'critical'
        category = 'severe_threat'
    else:
        # Determine if escalation is needed
        escalate = (is_harassment or is_urgent) and confidence > 0.5
        
        # Determine severity level
        if confidence > 0.8:
            severity = 'high'
        elif confidence > 0.5:
            severity = 'medium'
        elif confidence > 0.2:
            severity = 'low'
        else:
            severity = 'none'
        
        # Determine category
        if is_harassment and is_urgent:
            category = 'harassment_urgent'
        elif is_harassment:
            category = 'harassment'
        elif is_urgent:
            category = 'urgent'
        else:
            category = 'safe'
    
    return {
        'is_harassment': is_harassment,
        'is_urgent': is_urgent,
        'confidence': round(confidence, 2),
        'escalate': escalate,
        'category': category,
        'reason': reason,
        'severity': severity,
        'raw_scores': {
            'harassment': base_result['harassment_confidence'],
            'urgency': base_result['urgency_confidence']
        }
    }


# ============================================
# BATCH ANALYSIS (for multiple messages)
# ============================================

def analyze_messages_batch(messages: List[str]) -> List[Dict]:
    """
    Analyze multiple messages at once
    Useful for chat history analysis
    """
    return [analyze_message(msg) for msg in messages]


# ============================================
# DEMO & TESTING
# ============================================

def demo():
    """
    Sample usage demonstration
    """
    print("=" * 60)
    print("🛡️ AI HARASSMENT & URGENCY DETECTION DEMO")
    print("=" * 60)
    
    test_messages = [
        "I have an urgent project due tomorrow, need help!",
        "I'm going to kill myself tonight. I can't take it anymore.",
        "You're such an idiot, I hate you so much!",
        "Can someone help me with my homework?",
        "I'm being threatened by someone at school. They said they'll hurt me.",
        "This assignment is killing me lol",
        "I know where you live. You're going to regret this.",
        "Emergency! Someone is following me home right now!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'─' * 60}")
        print(f"Test {i}: {message}")
        print(f"{'─' * 60}")
        
        result = analyze_message(message)
        
        print(f"📊 Analysis Results:")
        print(f"   Harassment: {'✅ YES' if result['is_harassment'] else '❌ NO'}")
        print(f"   Urgent: {'✅ YES' if result['is_urgent'] else '❌ NO'}")
        print(f"   Confidence: {result['confidence']:.0%}")
        print(f"   Escalate: {'🚨 YES' if result['escalate'] else '✅ NO'}")
        print(f"   Category: {result['category']}")
        print(f"   Severity: {result['severity'].upper()}")
        print(f"   Reason: {result['reason']}")


if __name__ == "__main__":
    demo()
