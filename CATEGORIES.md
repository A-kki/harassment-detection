# AI Harassment Detector - Categories

## 4 Detection Categories

### 1. 🔞 HARASSMENT
**Detects:** Creepy, inappropriate, and sexually suggestive content

**Keywords Include:**
- Sexual advances: "send pics", "send nudes", "what are you wearing", "sexy", "hot body"
- Stalking behavior: "following you", "watching you", "obsessed with you", "know where you live"
- Inappropriate requests: "come over", "alone tonight", "meet in person", "netflix and chill"
- Predatory language: "sugar daddy", "don't tell anyone", "secret between us"
- Adult content: "nsfw", "explicit", "18+", "x-rated"

**Pattern Detection:**
- "send/show me pics/pictures/photos" (high priority)
- "sexy/hot/beautiful girl/boy/woman/man"
- "meet/come me/over/tonight/alone"

---

### 2. ⚠️ BULLY
**Detects:** Toxic, harmful, and aggressive content

**Detection Method:**
- Uses AI model: `unitary/toxic-bert`
- Analyzes text for toxicity, threats, insults, and hate speech
- Threshold: >60% confidence for toxic classification

---

### 3. 🚨 FRAUD
**Detects:** Scams, phishing, and fraudulent schemes

**Keywords Include:**
- Phishing: "verify your account", "suspended", "confirm your identity"
- Scams: "prize", "winner", "lottery", "inheritance", "nigerian prince"
- Financial fraud: "bitcoin", "crypto", "investment opportunity", "guaranteed return"
- Urgency tactics: "urgent", "act now", "limited time", "claim your"

**Pattern Detection:**
- Credit card numbers (16 digits)
- Social Security Numbers (XXX-XX-XXXX)
- Suspicious URLs

---

### 4. ✅ SAFE
**Detects:** Appropriate and non-threatening messages

**Criteria:**
- No harassment indicators
- Low toxicity score
- No fraud patterns
- Normal, friendly communication

---

## Priority Order
1. **HARASSMENT** (checked first - highest priority for creepy content)
2. **FRAUD** (financial/scam detection)
3. **BULLY** (toxicity detection)
4. **SAFE** (default if no threats detected)

## Confidence Scoring
- **Harassment:** 65-95% (based on keyword matches)
- **Fraud:** 60-95% (based on fraud indicators)
- **Bully:** Based on AI model confidence
- **Safe:** Inverse of toxicity score
