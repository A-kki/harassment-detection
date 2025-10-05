"""
Advanced Student Cyber Safety Platform
Two-Layer AI Detection System with Gemini Integration
"""

import streamlit as st
from ai_detection import analyze_message, analyze_messages_batch
import time

# Page configuration
st.set_page_config(
    page_title="Student Cyber Safety Platform",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .critical-alert {
        background-color: #ff4444;
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        font-size: 1.2em;
        margin: 10px 0;
    }
    .high-alert {
        background-color: #ff8800;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
    }
    .medium-alert {
        background-color: #ffbb33;
        color: black;
        padding: 15px;
        border-radius: 8px;
    }
    .safe-message {
        background-color: #00C851;
        color: white;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ Student Cyber Safety Platform")
st.markdown("### AI-Powered Harassment & Urgency Detection System")
st.markdown("*Two-layer detection: Keyword Classifier + Gemini Context Filter*")

# Sidebar
with st.sidebar:
    st.header("⚙️ System Info")
    st.info("**Detection Layers:**\n- Layer 1: Keyword Analysis\n- Layer 2: Gemini AI Context")
    
    st.header("📊 Categories")
    st.markdown("""
    - 🔴 **Critical**: Immediate threat
    - 🟠 **High**: Serious concern
    - 🟡 **Medium**: Potential issue
    - 🟢 **Safe**: Normal message
    """)
    
    st.header("🚨 Escalation")
    st.markdown("""
    Messages are escalated when:
    - Confidence > 50%
    - Severe patterns detected
    - Multiple threat indicators
    """)

# Main tabs
tab1, tab2, tab3 = st.tabs(["📝 Single Message Analysis", "📊 Batch Analysis", "🧪 Test Cases"])

# ============================================
# TAB 1: SINGLE MESSAGE ANALYSIS
# ============================================
with tab1:
    st.header("Analyze a Single Message")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        message_input = st.text_area(
            "Enter message to analyze:",
            height=150,
            placeholder="Type or paste a message here...",
            help="Enter any message from chat, report form, or social media"
        )
    
    with col2:
        st.markdown("### Quick Examples")
        if st.button("📚 Urgent Homework"):
            message_input = "I have an urgent project due tomorrow, need help!"
        if st.button("🆘 Suicide Risk"):
            message_input = "I'm going to kill myself tonight. I can't take it anymore."
        if st.button("😡 Bullying"):
            message_input = "You're such an idiot, I hate you so much!"
        if st.button("🔪 Threat"):
            message_input = "I know where you live. You're going to regret this."
    
    if st.button("🔍 Analyze Message", type="primary", use_container_width=True):
        if message_input:
            with st.spinner("🤖 AI analyzing message..."):
                # Simulate processing time
                time.sleep(1)
                
                # Analyze message
                result = analyze_message(message_input)
                
                st.markdown("---")
                
                # Display results based on severity
                if result['severity'] == 'critical':
                    st.markdown(f"""
                    <div class="critical-alert">
                        🚨 CRITICAL ALERT - IMMEDIATE ACTION REQUIRED 🚨
                    </div>
                    """, unsafe_allow_html=True)
                    st.error(f"**Category:** {result['category'].upper()}")
                    st.error(f"**Reason:** {result['reason']}")
                    
                elif result['severity'] == 'high':
                    st.markdown(f"""
                    <div class="high-alert">
                        ⚠️ HIGH PRIORITY - Escalation Recommended
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif result['severity'] == 'medium':
                    st.markdown(f"""
                    <div class="medium-alert">
                        ⚡ MEDIUM PRIORITY - Monitor Situation
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.markdown(f"""
                    <div class="safe-message">
                        ✅ SAFE - No Immediate Concerns
                    </div>
                    """, unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Harassment",
                        "YES" if result['is_harassment'] else "NO",
                        delta="Alert" if result['is_harassment'] else None,
                        delta_color="inverse" if result['is_harassment'] else "normal"
                    )
                
                with col2:
                    st.metric(
                        "Urgent",
                        "YES" if result['is_urgent'] else "NO",
                        delta="Alert" if result['is_urgent'] else None,
                        delta_color="inverse" if result['is_urgent'] else "normal"
                    )
                
                with col3:
                    st.metric(
                        "Confidence",
                        f"{result['confidence']:.0%}",
                        delta=None
                    )
                
                with col4:
                    st.metric(
                        "Escalate",
                        "YES" if result['escalate'] else "NO",
                        delta="Action Required" if result['escalate'] else None,
                        delta_color="inverse" if result['escalate'] else "normal"
                    )
                
                # Detailed breakdown
                with st.expander("📊 Detailed Analysis"):
                    st.json(result)
                
                # Action recommendations
                if result['escalate']:
                    st.markdown("### 🚨 Recommended Actions:")
                    if result['severity'] == 'critical':
                        st.error("""
                        1. **Immediately notify school administration**
                        2. **Contact emergency services if needed**
                        3. **Alert parents/guardians**
                        4. **Document all evidence**
                        5. **Provide immediate support resources**
                        """)
                    elif result['severity'] == 'high':
                        st.warning("""
                        1. **Notify school counselor**
                        2. **Contact parents/guardians**
                        3. **Monitor situation closely**
                        4. **Provide support resources**
                        """)
                    else:
                        st.info("""
                        1. **Log incident for review**
                        2. **Monitor for escalation**
                        3. **Consider follow-up**
                        """)
        else:
            st.warning("Please enter a message to analyze.")

# ============================================
# TAB 2: BATCH ANALYSIS
# ============================================
with tab2:
    st.header("Batch Message Analysis")
    st.markdown("Analyze multiple messages at once (e.g., chat history, reports)")
    
    batch_input = st.text_area(
        "Enter messages (one per line):",
        height=200,
        placeholder="Message 1\nMessage 2\nMessage 3\n...",
        help="Each line will be analyzed separately"
    )
    
    if st.button("🔍 Analyze Batch", type="primary"):
        if batch_input:
            messages = [msg.strip() for msg in batch_input.split('\n') if msg.strip()]
            
            with st.spinner(f"🤖 Analyzing {len(messages)} messages..."):
                results = analyze_messages_batch(messages)
                
                # Summary statistics
                st.markdown("### 📊 Summary Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                total_harassment = sum(1 for r in results if r['is_harassment'])
                total_urgent = sum(1 for r in results if r['is_urgent'])
                total_escalate = sum(1 for r in results if r['escalate'])
                total_critical = sum(1 for r in results if r['severity'] == 'critical')
                
                with col1:
                    st.metric("Total Messages", len(messages))
                with col2:
                    st.metric("Harassment", total_harassment)
                with col3:
                    st.metric("Urgent", total_urgent)
                with col4:
                    st.metric("Critical", total_critical)
                
                # Detailed results
                st.markdown("### 📋 Detailed Results")
                
                for i, (msg, result) in enumerate(zip(messages, results), 1):
                    with st.expander(f"Message {i}: {msg[:50]}..." if len(msg) > 50 else f"Message {i}: {msg}"):
                        
                        # Severity badge
                        if result['severity'] == 'critical':
                            st.error(f"🚨 CRITICAL - {result['category']}")
                        elif result['severity'] == 'high':
                            st.warning(f"⚠️ HIGH - {result['category']}")
                        elif result['severity'] == 'medium':
                            st.info(f"⚡ MEDIUM - {result['category']}")
                        else:
                            st.success(f"✅ SAFE - {result['category']}")
                        
                        st.write(f"**Confidence:** {result['confidence']:.0%}")
                        st.write(f"**Escalate:** {'YES' if result['escalate'] else 'NO'}")
                        st.write(f"**Reason:** {result['reason']}")
        else:
            st.warning("Please enter messages to analyze.")

# ============================================
# TAB 3: TEST CASES
# ============================================
with tab3:
    st.header("🧪 Pre-loaded Test Cases")
    st.markdown("Test the system with various scenarios")
    
    test_cases = {
        "Safe - Academic": [
            "I have an urgent project due tomorrow, need help!",
            "Can someone help me with my homework?",
            "This assignment is killing me lol"
        ],
        "Harassment": [
            "You're such an idiot, I hate you so much!",
            "I'm going to make your life miserable",
            "I know where you live. You're going to regret this."
        ],
        "Urgent/Emergency": [
            "I'm going to kill myself tonight. I can't take it anymore.",
            "Someone is threatening me at school. I'm scared.",
            "Emergency! Someone is following me home right now!"
        ],
        "Severe Threats": [
            "I have a gun and I'm going to use it",
            "I'm going to hurt everyone at school tomorrow",
            "I want to kill myself and take others with me"
        ]
    }
    
    category = st.selectbox("Select Test Category:", list(test_cases.keys()))
    
    if st.button("🚀 Run Test Cases", type="primary"):
        messages = test_cases[category]
        
        with st.spinner(f"Testing {len(messages)} messages..."):
            results = analyze_messages_batch(messages)
            
            for msg, result in zip(messages, results):
                st.markdown("---")
                st.markdown(f"**Message:** {msg}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if result['severity'] == 'critical':
                        st.error(f"🚨 {result['severity'].upper()}")
                    elif result['severity'] == 'high':
                        st.warning(f"⚠️ {result['severity'].upper()}")
                    else:
                        st.info(f"ℹ️ {result['severity'].upper()}")
                
                with col2:
                    st.write(f"**Category:** {result['category']}")
                    st.write(f"**Confidence:** {result['confidence']:.0%}")
                
                with col3:
                    st.write(f"**Escalate:** {'🚨 YES' if result['escalate'] else '✅ NO'}")
                    st.write(f"**Reason:** {result['reason']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🛡️ Student Cyber Safety Platform | Powered by Gemini AI</p>
    <p>Built for 24-hour Hackathon | Two-Layer Detection System</p>
</div>
""", unsafe_allow_html=True)
