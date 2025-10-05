// utils/aiDetection.ts
// ✅ Context-Aware Harassment & Urgency Detector
// Works with or without Gemini API
// Safe for Hackathon demo use

import { GoogleGenerativeAI } from "@google/generative-ai"

// ============================================
// CONFIGURATION
// ============================================

const GEMINI_API_KEY = process.env.NEXT_PUBLIC_GEMINI_API_KEY || ""
const genAI = GEMINI_API_KEY ? new GoogleGenerativeAI(GEMINI_API_KEY) : null

// ============================================
// KEYWORD DATABASES
// ============================================

const harassmentKeywords = [
  "harass", "threat", "kill", "hate", "abuse", "attack", "blackmail",
  "bully", "hurt", "harm", "stalk", "assault", "violence",
  "beat up", "destroy you", "ruin your life", "expose you",
  "revenge", "get back at", "make you pay", "regret this"
]

const urgentWords = [
  "help", "emergency", "suicide", "kill myself", "end my life", "want to die",
  "self harm", "cutting", "overdose", "danger", "scared", "afraid",
  "threatening me", "going to hurt", "right now", "tonight", "today",
  "can't take it anymore", "no way out", "goodbye forever"
]

const neutralWords = [
  "assignment", "exam", "project", "deadline", "homework", "study",
  "test", "quiz", "presentation", "essay", "report", "class",
  "urgent project", "urgent assignment", "urgent homework", "due tomorrow"
]

const severePatterns = [
  /\b(kill|murder|shoot|stab)\s+(you|myself|someone)/i,
  /\b(suicide|kill myself|end my life)/i,
  /\b(have a gun|have a knife|have a weapon)/i,
  /\b(going to|gonna|will)\s+(hurt|harm|kill|attack)/i,
  /\b(rape|sexual assault|molest)/i,
  /\b(bomb|explosive|blow up)/i
]

// ============================================
// TYPE DEFINITIONS
// ============================================

interface BaseClassifierResult {
  harassmentConfidence: number
  urgencyConfidence: number
  isPotentialHarassment: boolean
  isPotentialUrgent: boolean
  hasSeverePattern: boolean
  neutralContext: boolean
}

interface AnalysisResult {
  isHarassment: boolean
  isUrgent: boolean
  confidence: number
  escalate: boolean
  category: string
  reason: string
  severity: 'none' | 'low' | 'medium' | 'high' | 'critical'
  rawScores: {
    harassment: number
    urgency: number
  }
}

// ============================================
// LAYER 1: KEYWORD-BASED CLASSIFIER
// ============================================

function baseClassifier(message: string): BaseClassifierResult {
  const text = message.toLowerCase()
  
  // Count keyword matches
  let harassmentScore = 0
  let urgencyScore = 0
  let neutralScore = 0
  
  harassmentKeywords.forEach(keyword => {
    if (text.includes(keyword)) harassmentScore += 1
  })
  
  urgentWords.forEach(keyword => {
    if (text.includes(keyword)) urgencyScore += 1
  })
  
  neutralWords.forEach(keyword => {
    if (text.includes(keyword)) neutralScore += 1
  })
  
  // Check for severe patterns
  const hasSeverePattern = severePatterns.some(pattern => pattern.test(text))
  
  // Calculate confidence scores (0-1 scale)
  let harassmentConfidence = Math.min(harassmentScore / 3, 1.0)
  let urgencyConfidence = Math.min(urgencyScore / 3, 1.0)
  
  // Adjust for neutral context (reduce false positives)
  if (neutralScore > 0) {
    harassmentConfidence *= 0.5
    urgencyConfidence *= 0.5
  }
  
  // Severe patterns override everything
  if (hasSeverePattern) {
    harassmentConfidence = Math.max(harassmentConfidence, 0.95)
    urgencyConfidence = Math.max(urgencyConfidence, 0.95)
  }
  
  return {
    harassmentConfidence,
    urgencyConfidence,
    isPotentialHarassment: harassmentConfidence > 0.2,
    isPotentialUrgent: urgencyConfidence > 0.2,
    hasSeverePattern,
    neutralContext: neutralScore > 0
  }
}

// ============================================
// LAYER 2: GEMINI CONTEXT VERIFIER
// ============================================

async function contextVerifierGemini(message: string): Promise<{ isRealThreat: boolean; reason: string }> {
  if (!genAI) {
    return contextVerifierFallback(message)
  }
  
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" })
    
    const prompt = `
You are a cyber safety AI for a student platform. Analyze this message carefully.

Message: "${message}"

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
`
    
    const result = await model.generateContent(prompt)
    const responseText = result.response.text().trim()
    
    // Parse response
    const isRealThreat = responseText.toLowerCase().includes('threat: true')
    
    // Extract reason
    const reasonMatch = responseText.match(/REASON:\s*(.+)/i)
    const reason = reasonMatch ? reasonMatch[1] : "AI analysis completed"
    
    return { isRealThreat, reason }
    
  } catch (error) {
    console.error("⚠️ Gemini verification failed:", error)
    return contextVerifierFallback(message)
  }
}

function contextVerifierFallback(message: string): { isRealThreat: boolean; reason: string } {
  const text = message.toLowerCase()
  
  // Check for severe patterns first
  if (severePatterns.some(pattern => pattern.test(text))) {
    return { isRealThreat: true, reason: "Severe threat pattern detected" }
  }
  
  // Check if urgent words present WITHOUT neutral context
  const hasUrgent = urgentWords.some(word => text.includes(word))
  const hasNeutral = neutralWords.some(word => text.includes(word))
  
  if (hasUrgent && !hasNeutral) {
    return { isRealThreat: true, reason: "Urgent keywords detected without academic context" }
  }
  
  // Check for harassment without neutral context
  const harassmentCount = harassmentKeywords.filter(word => text.includes(word)).length
  if (harassmentCount >= 2 && !hasNeutral) {
    return { isRealThreat: true, reason: "Multiple harassment indicators detected" }
  }
  
  return { isRealThreat: false, reason: "Likely false positive or normal message" }
}

// ============================================
// MAIN ANALYSIS FUNCTION
// ============================================

export async function analyzeMessage(message: string): Promise<AnalysisResult> {
  // Layer 1: Keyword classification
  const baseResult = baseClassifier(message)
  
  // Layer 2: Context verification (only if potential threat detected)
  let contextValid = false
  let reason = "Message appears safe"
  
  if (baseResult.isPotentialHarassment || baseResult.isPotentialUrgent) {
    const verification = await contextVerifierGemini(message)
    contextValid = verification.isRealThreat
    reason = verification.reason
  }
  
  // Determine final classification
  let isHarassment = baseResult.isPotentialHarassment && contextValid
  let isUrgent = baseResult.isPotentialUrgent && contextValid
  
  // Calculate overall confidence
  let confidence = Math.max(
    baseResult.harassmentConfidence,
    baseResult.urgencyConfidence
  )
  
  let escalate: boolean
  let severity: 'none' | 'low' | 'medium' | 'high' | 'critical'
  let category: string
  
  // Severe patterns always escalate
  if (baseResult.hasSeverePattern) {
    isHarassment = true
    isUrgent = true
    confidence = 0.95
    escalate = true
    severity = 'critical'
    category = 'severe_threat'
  } else {
    // Determine if escalation is needed
    escalate = (isHarassment || isUrgent) && confidence > 0.5
    
    // Determine severity level
    if (confidence > 0.8) {
      severity = 'high'
    } else if (confidence > 0.5) {
      severity = 'medium'
    } else if (confidence > 0.2) {
      severity = 'low'
    } else {
      severity = 'none'
    }
    
    // Determine category
    if (isHarassment && isUrgent) {
      category = 'harassment_urgent'
    } else if (isHarassment) {
      category = 'harassment'
    } else if (isUrgent) {
      category = 'urgent'
    } else {
      category = 'safe'
    }
  }
  
  return {
    isHarassment,
    isUrgent,
    confidence: Math.round(confidence * 100) / 100,
    escalate,
    category,
    reason,
    severity,
    rawScores: {
      harassment: baseResult.harassmentConfidence,
      urgency: baseResult.urgencyConfidence
    }
  }
}

// ============================================
// BATCH ANALYSIS
// ============================================

export async function analyzeMessagesBatch(messages: string[]): Promise<AnalysisResult[]> {
  return Promise.all(messages.map(msg => analyzeMessage(msg)))
}

// ============================================
// SAMPLE USAGE DEMO
// ============================================

/*
// Example 1: In a chat handler
async function handleChatMessage(input: string) {
  const analysis = await analyzeMessage(input)

  if (analysis.escalate) {
    // 🔔 Notify Admin / Cyber Alert / Parent Email
    console.log("⚠️ ESCALATION NEEDED:", analysis)
    notifyAdmin(analysis)
    sendParentAlert(analysis)
  } else {
    console.log("✅ Safe or normal message.")
  }
  
  return analysis
}

// Example 2: In a report form
async function handleReportSubmission(reportText: string) {
  const analysis = await analyzeMessage(reportText)
  
  // Store with priority based on severity
  await saveReport({
    text: reportText,
    severity: analysis.severity,
    category: analysis.category,
    needsImmediate: analysis.escalate,
    confidence: analysis.confidence
  })
  
  if (analysis.severity === 'critical') {
    // Immediate notification to authorities
    await notifyEmergencyContacts()
  }
}

// Example 3: Testing
(async () => {
  const testMessages = [
    "I have an urgent project due tomorrow, need help!",
    "I'm going to kill myself tonight. I can't take it anymore.",
    "You're such an idiot, I hate you so much!",
    "Can someone help me with my homework?",
    "I'm being threatened by someone at school. They said they'll hurt me."
  ]
  
  for (const msg of testMessages) {
    const result = await analyzeMessage(msg)
    console.log(`\nMessage: ${msg}`)
    console.log(`Result:`, result)
  }
})()
*/
