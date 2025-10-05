# 🛡️ AI Harassment & Urgency Detection System - Integration Guide

## 📋 Overview

This is a **two-layer AI detection system** designed for Student Cyber Safety Platforms. It combines:
1. **Layer 1**: Fast keyword-based classifier
2. **Layer 2**: Gemini AI context verification

## 🚀 Quick Start

### Python (Backend/Streamlit)

```python
from ai_detection import analyze_message

# Analyze a single message
result = analyze_message("I'm being threatened at school")

print(result)
# Output:
# {
#   'is_harassment': True,
#   'is_urgent': True,
#   'confidence': 0.85,
#   'escalate': True,
#   'category': 'harassment_urgent',
#   'reason': 'Urgent keywords detected without academic context',
#   'severity': 'high'
# }

# Use in your application
if result['escalate']:
    notify_admin(result)
    send_parent_alert(result)
```

### TypeScript/JavaScript (Frontend)

```typescript
import { analyzeMessage } from '@/utils/aiDetection'

// In your chat handler
async function handleChatMessage(input: string) {
  const analysis = await analyzeMessage(input)

  if (analysis.escalate) {
    // 🔔 Notify Admin / Cyber Alert / Parent Email
    console.log("⚠️ ESCALATION NEEDED:", analysis)
    await notifyAdmin(analysis)
    await sendParentAlert(analysis)
  }
  
  return analysis
}

// In your report form
async function handleReportSubmission(reportText: string) {
  const analysis = await analyzeMessage(reportText)
  
  await saveReport({
    text: reportText,
    severity: analysis.severity,
    category: analysis.category,
    needsImmediate: analysis.escalate,
    confidence: analysis.confidence
  })
  
  if (analysis.severity === 'critical') {
    await notifyEmergencyContacts()
  }
}
```

## 📦 Installation

### Python
```bash
pip install streamlit google-generativeai
```

### TypeScript/JavaScript
```bash
npm install @google/generative-ai
# or
yarn add @google/generative-ai
```

## 🔧 Configuration

### Set Gemini API Key

**Python** (`ai_detection.py`):
```python
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

**TypeScript** (`aiDetection.ts`):
```typescript
const GEMINI_API_KEY = "YOUR_API_KEY_HERE"
// Or use environment variable:
const GEMINI_API_KEY = process.env.NEXT_PUBLIC_GEMINI_API_KEY
```

## 📊 Response Format

```typescript
{
  isHarassment: boolean,      // Is this harassment?
  isUrgent: boolean,          // Is this urgent/emergency?
  confidence: number,         // 0-1 confidence score
  escalate: boolean,          // Should this be escalated?
  category: string,           // 'harassment', 'urgent', 'safe', etc.
  reason: string,             // Explanation from AI
  severity: string,           // 'none', 'low', 'medium', 'high', 'critical'
  rawScores: {
    harassment: number,
    urgency: number
  }
}
```

## 🎯 Use Cases

### 1. Chat Application
```python
# Monitor real-time chat messages
def on_message_received(message, user_id):
    result = analyze_message(message)
    
    if result['escalate']:
        # Flag message for review
        flag_message(message, user_id, result)
        
        # Notify moderators
        notify_moderators(user_id, message, result)
        
        # If critical, take immediate action
        if result['severity'] == 'critical':
            suspend_user(user_id)
            notify_emergency_contacts()
```

### 2. Report Form
```python
# Analyze submitted reports
def handle_report_submission(report_data):
    result = analyze_message(report_data['description'])
    
    # Save with priority
    save_report({
        **report_data,
        'priority': result['severity'],
        'auto_escalated': result['escalate'],
        'ai_confidence': result['confidence']
    })
    
    # Route to appropriate handler
    if result['severity'] == 'critical':
        route_to_emergency_team(report_data)
    elif result['severity'] == 'high':
        route_to_counselor(report_data)
    else:
        route_to_standard_queue(report_data)
```

### 3. Batch Analysis
```python
# Analyze chat history
messages = get_chat_history(user_id)
results = analyze_messages_batch(messages)

# Identify patterns
harassment_count = sum(1 for r in results if r['is_harassment'])
if harassment_count > 3:
    flag_user_for_review(user_id)
```

## 🛠️ Customization

### Add Custom Keywords

**Python**:
```python
# In ai_detection.py
HARASSMENT_KEYWORDS.extend([
    'your_custom_keyword',
    'another_keyword'
])
```

**TypeScript**:
```typescript
// In aiDetection.ts
const harassmentKeywords = [
  ...existingKeywords,
  'your_custom_keyword',
  'another_keyword'
]
```

### Adjust Thresholds

```python
# Change escalation threshold
if confidence > 0.3:  # Default is 0.5
    escalate = True

# Change severity levels
if confidence > 0.6:  # Default is 0.8
    severity = 'high'
```

## 🧪 Testing

### Run Demo (Python)
```bash
python ai_detection.py
```

### Run Advanced UI (Streamlit)
```bash
streamlit run app_advanced.py
```

### Test Cases
```python
test_messages = [
    "I have an urgent project due tomorrow",  # Safe
    "I'm going to kill myself",               # Critical
    "You're such an idiot",                   # Harassment
    "Someone is threatening me"               # Urgent
]

for msg in test_messages:
    result = analyze_message(msg)
    print(f"{msg}: {result['category']} ({result['confidence']:.0%})")
```

## 🔒 Security Best Practices

1. **Never hardcode API keys in production**
   ```typescript
   // Use environment variables
   const GEMINI_API_KEY = process.env.GEMINI_API_KEY
   ```

2. **Rate limiting**
   ```python
   # Implement rate limiting for API calls
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def analyze_message_cached(message):
       return analyze_message(message)
   ```

3. **Data privacy**
   - Don't log sensitive messages
   - Encrypt stored analysis results
   - Follow GDPR/COPPA guidelines

## 📈 Performance

- **Layer 1 (Keywords)**: ~1ms per message
- **Layer 2 (Gemini)**: ~500-1000ms per message
- **Fallback mode**: ~2ms per message

### Optimization Tips
```python
# Use batch analysis for multiple messages
results = analyze_messages_batch(messages)  # Faster than loop

# Cache results for duplicate messages
from functools import lru_cache

@lru_cache(maxsize=1000)
def analyze_cached(message):
    return analyze_message(message)
```

## 🐛 Troubleshooting

### Gemini API Not Working
```python
# Check if fallback is being used
if not GEMINI_AVAILABLE:
    print("Using rule-based fallback")
```

### False Positives
```python
# Adjust neutral keywords
NEUTRAL_KEYWORDS.extend([
    'your_safe_phrase',
    'another_safe_phrase'
])
```

### False Negatives
```python
# Add more threat keywords
HARASSMENT_KEYWORDS.extend([
    'missed_threat_word',
    'another_threat_word'
])
```

## 📞 Support

For issues or questions:
1. Check the demo: `python ai_detection.py`
2. Review test cases in `app_advanced.py`
3. Adjust thresholds based on your use case

## 🎉 Hackathon Tips

1. **Start with the demo** - Run `streamlit run app_advanced.py`
2. **Test edge cases** - Use the test cases tab
3. **Customize keywords** - Add domain-specific terms
4. **Monitor confidence** - Adjust thresholds based on results
5. **Have a fallback** - System works without Gemini API

## 📄 License

Free to use for educational and hackathon purposes.

---

**Built for 24-hour Hackathons | Optimized for Student Safety Platforms**
