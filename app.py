import streamlit as st
import re

st.title("AI Harassment Detector")
st.markdown("### Detect Bullying, Harassment, Urgency, Fraud, and Safe Messages")

# Bullying/Toxic keywords
bully_keywords = [
    'stupid', 'idiot', 'dumb', 'loser', 'worthless', 'pathetic', 'ugly', 'fat',
    'hate you', 'nobody likes you', 'waste of space',
    'retard', 'moron', 'freak', 'weirdo', 'disgusting', 'trash', 'garbage',
    'shut up', 'go away', 'annoying', 'stupid bitch',
    'piece of shit', 'fuck you', 'fuck off', 'asshole', 'bastard', 'slut', 'whore'
]

# Urgency/Emergency keywords (NEW - CRITICAL)
urgency_keywords = [
    'help me', 'emergency', 'suicide', 'kill myself', 'end my life', 'want to die',
    'self harm', 'cutting', 'overdose', 'pills', 'danger', 'scared', 'afraid',
    'threatening me', 'going to hurt', 'hurt me', 'abuse', 'violence',
    'can\'t take it anymore', 'no way out', 'goodbye forever', 'final goodbye',
    'kill yourself', 'die', 'harm yourself', 'hurt yourself',
    'rape', 'assault', 'molest', 'attack', 'weapon', 'gun', 'knife'
]

# Fraud detection keywords
fraud_keywords = [
    'click here', 'verify your account', 'suspended', 'confirm your identity',
    'prize', 'winner', 'lottery', 'inheritance', 'nigerian prince', 'bank account',
    'credit card', 'social security', 'password', 'pin', 'claim your', 'act now',
    'limited time', 'free money', 'cash prize', 'wire transfer', 'bitcoin', 'crypto',
    'investment opportunity', 'guaranteed return', 'risk-free', 'double your money'
]

# Harassment/Creepy words detection
harassment_keywords = [
    'sexy', 'hot body', 'send pics', 'send nudes', 'wanna hook up', 'dtf', 'netflix and chill',
    'come over', 'alone tonight', 'what are you wearing', 'undress', 'strip', 'naked',
    'bedroom', 'horny', 'turn me on', 'seduce', 'flirt', 'kiss me', 'touch you',
    'stalking', 'following you', 'watching you', 'obsessed with you', 'can\'t stop thinking',
    'you\'re mine', 'belong to me', 'won\'t leave you alone', 'know where you live',
    'creep', 'perv', 'sleazy', 'inappropriate', 'uncomfortable', 'boundaries',
    'age/sex/location', 'asl', 'private chat', 'secret between us', 'don\'t tell anyone',
    'meet in person', 'come to my place', 'get in my car', 'run away with me',
    'sugar daddy', 'sugar baby', 'pay for your time', 'compensated dating',
    'explicit', 'nsfw', 'adult content', 'x-rated', '18+', 'mature content'
]

# Safe/Academic keywords (to reduce false positives)
safe_keywords = [
    'homework', 'assignment', 'project', 'study', 'exam', 'test', 'quiz',
    'class', 'teacher', 'professor', 'due tomorrow', 'deadline'
]

def detect_urgency(text):
    """Check if text contains urgent/emergency content"""
    text_lower = text.lower()
    urgency_score = 0
    matched_keywords = []
    
    # Check for urgency keywords
    for keyword in urgency_keywords:
        if keyword in text_lower:
            urgency_score += 1
            matched_keywords.append(keyword)
    
    # Check for critical patterns
    if re.search(r'\b(kill|end)\s+(myself|my life)', text_lower):
        urgency_score += 3  # High priority
    if re.search(r'\b(suicide|self harm|overdose)', text_lower):
        urgency_score += 3
    if re.search(r'\b(help|emergency|danger)', text_lower):
        urgency_score += 1
    
    return urgency_score, matched_keywords

def detect_bully(text):
    """Check if text contains bullying/toxic content"""
    text_lower = text.lower()
    bully_score = 0
    matched_keywords = []
    
    # Check for bully keywords
    for keyword in bully_keywords:
        if keyword in text_lower:
            bully_score += 1
            matched_keywords.append(keyword)
    
    # Check for aggressive patterns
    if re.search(r'\b(hate|despise|loathe)\s+(you|him|her|them)', text_lower):
        bully_score += 1
    
    return bully_score, matched_keywords

def detect_fraud(text):
    """Check if text contains fraud indicators"""
    text_lower = text.lower()
    fraud_score = 0
    
    # Check for fraud keywords
    for keyword in fraud_keywords:
        if keyword in text_lower:
            fraud_score += 1
    
    # Check for suspicious patterns
    if re.search(r'\b\d{16}\b', text):  # Credit card pattern
        fraud_score += 2
    if re.search(r'\b\d{3}-\d{2}-\d{4}\b', text):  # SSN pattern
        fraud_score += 2
    if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
        fraud_score += 1  # Contains URL
    
    return fraud_score

def detect_harassment(text):
    """Check if text contains harassment/creepy content"""
    text_lower = text.lower()
    harassment_score = 0
    matched_keywords = []
    
    # Check for harassment keywords
    for keyword in harassment_keywords:
        if keyword in text_lower:
            harassment_score += 1
            matched_keywords.append(keyword)
    
    # Check for creepy patterns
    if re.search(r'\b(sexy|hot|beautiful)\s+(girl|boy|woman|man|lady)', text_lower):
        harassment_score += 1
    if re.search(r'\b(send|show)\s+(me|pics|pictures|photos)', text_lower):
        harassment_score += 2
    if re.search(r'\b(meet|come)\s+(me|over|tonight|alone)', text_lower):
        harassment_score += 1
    
    return harassment_score, matched_keywords

def classify_message(text):
    """Classify message into urgency, bully, harassment, fraud, or safe"""
    if not text.strip():
        return "safe", 0.0, "No text provided", {}
    
    # Check if it's academic/safe context
    text_lower = text.lower()
    is_academic = any(keyword in text_lower for keyword in safe_keywords)
    
    # Get all scores
    urgency_score, urgency_matches = detect_urgency(text)
    harassment_score, harassment_matches = detect_harassment(text)
    bully_score, bully_matches = detect_bully(text)
    fraud_score = detect_fraud(text)
    
    # PRIORITY 1: Urgency/Emergency (HIGHEST PRIORITY)
    if urgency_score >= 2 and not is_academic:
        confidence = min(0.98, 0.75 + (urgency_score * 0.08))
        keywords_str = ", ".join(urgency_matches[:3])
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "urgency", confidence, f"🚨 URGENT/EMERGENCY: {keywords_str}", details
    
    # PRIORITY 2: Harassment (creepy content)
    if harassment_score >= 2:
        confidence = min(0.95, 0.65 + (harassment_score * 0.08))
        keywords_str = ", ".join(harassment_matches[:3])
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "harassment", confidence, f"Inappropriate/creepy content: {keywords_str}", details
    
    # PRIORITY 3: Bullying/Toxicity
    if bully_score >= 2:
        confidence = min(0.95, 0.65 + (bully_score * 0.08))
        keywords_str = ", ".join(bully_matches[:3])
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "bully", confidence, f"Toxic/bullying content: {keywords_str}", details
    
    # PRIORITY 4: Fraud
    if fraud_score >= 2:
        confidence = min(0.95, 0.6 + (fraud_score * 0.1))
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "fraud", confidence, "Potential fraud/scam detected", details
    
    # Lower threshold checks
    if urgency_score >= 1 and not is_academic:
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "urgency", 0.75, "Potentially urgent content detected", details
    elif harassment_score >= 1:
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "harassment", 0.70, "Potentially inappropriate content detected", details
    elif bully_score >= 1:
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "bully", 0.65, "Potentially toxic content detected", details
    elif fraud_score >= 1:
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "fraud", 0.65, "Suspicious content detected", details
    else:
        details = {
            'urgency': urgency_score,
            'harassment': harassment_score,
            'bully': bully_score,
            'fraud': fraud_score
        }
        return "safe", 0.95, "Message appears safe", details

# UI
text = st.text_area("Enter a message to analyze:", height=150, placeholder="Type or paste text here...")

if st.button(" Analyze Message", type="primary"):
    if text:
        with st.spinner("Analyzing..."):
            category, confidence, reason, details = classify_message(text)
            
            # Display results
            st.markdown("---")
            st.subheader("Analysis Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Category", category.upper())
            with col2:
                st.metric("Confidence", f"{confidence:.1%}")
            
            # Color-coded message
            if category == "urgency":
                st.error(f" **URGENCY/EMERGENCY DETECTED**\n\n{reason}")
                st.error(" IMMEDIATE ACTION REQUIRED - This message indicates a potential emergency or crisis situation!")
            elif category == "harassment":
                st.error(f" **HARASSMENT DETECTED**\n\n{reason}")
                st.warning("This message contains inappropriate, creepy, or sexually suggestive content.")
            elif category == "bully":
                st.error(f" **BULLYING DETECTED**\n\n{reason}")
                st.warning("This message contains harmful or toxic content.")
            elif category == "fraud":
                st.error(f" **FRAUD/SCAM DETECTED**\n\n{reason}")
                st.warning("This message appears to be a scam or phishing attempt.")
            else:
                st.success(f" **SAFE MESSAGE**\n\n{reason}")
                st.info("This message appears to be safe and appropriate.")
            
            # Show detailed scores
            with st.expander(" Detailed Scores"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Urgency Score", details['urgency'])
                with col2:
                    st.metric("Harassment Score", details['harassment'])
                with col3:
                    st.metric("Bully Score", details['bully'])
                with col4:
                    st.metric("Fraud Score", details['fraud'])
    else:
        st.warning("Please enter some text to analyze.")
