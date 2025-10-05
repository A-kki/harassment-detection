# ✅ GitHub Upload Checklist

## 🔐 CRITICAL: Secure Your API Key First!

### Option 1: Automated (Recommended)
```bash
python secure_api_key.py
```

### Option 2: Manual
1. Edit `ai_detection.py` line 14:
   ```python
   # Change from:
   GEMINI_API_KEY = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"
   
   # To:
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
   ```

2. Edit `aiDetection.ts` line 10:
   ```typescript
   // Change from:
   const GEMINI_API_KEY = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"
   
   // To:
   const GEMINI_API_KEY = process.env.NEXT_PUBLIC_GEMINI_API_KEY || ""
   ```

3. Create `.env` file:
   ```
   GEMINI_API_KEY=AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8
   ```

---

## 📋 Pre-Upload Checklist

- [ ] API key secured (run `python secure_api_key.py`)
- [ ] `.env` file created
- [ ] `.gitignore` file exists
- [ ] README.md reviewed
- [ ] All documentation files present
- [ ] Test the app still works after securing API key

---

## 🚀 Upload Steps

### 1. Initialize Git
```bash
cd "d:\harasment Model"
git init
```

### 2. Configure Git (First time only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Add Files
```bash
git add .
git status  # Review what will be committed
```

### 4. Create Commit
```bash
git commit -m "Initial commit: AI Harassment Detection System"
```

### 5. Create GitHub Repository
1. Go to https://github.com
2. Click "+" → "New repository"
3. Name: `harassment-detection`
4. Description: "AI-powered harassment and threat detection system"
5. Choose Public or Private
6. **DO NOT** check "Initialize with README"
7. Click "Create repository"

### 6. Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/harassment-detection.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## ✅ Post-Upload Checklist

- [ ] Repository visible on GitHub
- [ ] All files uploaded correctly
- [ ] README.md displays properly
- [ ] `.env` file NOT visible (should be ignored)
- [ ] API key NOT visible in any file
- [ ] Clone repository to test: `git clone https://github.com/YOUR_USERNAME/harassment-detection.git`

---

## 📁 Files That Should Be Uploaded

✅ **Python Files:**
- `app.py`
- `app_advanced.py`
- `ai_detection.py`
- `test_system.py`
- `secure_api_key.py`

✅ **TypeScript Files:**
- `aiDetection.ts`

✅ **Documentation:**
- `README.md`
- `GITHUB_SETUP.md`
- `INTEGRATION_GUIDE.md`
- `QUICK_START.md`
- `CATEGORIES.md`
- `PROJECT_SUMMARY.md`
- `README_AI_DETECTION.md`
- `FIXES_APPLIED.md`

✅ **Configuration:**
- `requirements.txt`
- `requirements_advanced.txt`
- `.gitignore`
- `LICENSE`

✅ **Scripts:**
- `setup_github.ps1`

---

## 🚫 Files That Should NOT Be Uploaded

❌ **Sensitive:**
- `.env` (API keys)
- Any file with hardcoded API keys

❌ **Generated:**
- `.venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)

❌ **User Data:**
- `uploaded_images/` (except .gitkeep)
- `uploaded_videos/` (except .gitkeep)

❌ **IDE:**
- `.vscode/`
- `.idea/`

---

## 🔍 Verify Before Pushing

### Check for API Keys
```bash
# Search for API key in files
grep -r "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8" .

# Should return: .env (only)
# If it returns other files, secure them first!
```

### Check .gitignore
```bash
cat .gitignore | grep .env
# Should show: .env
```

### Test the App
```bash
# Make sure it still works after securing API key
streamlit run app.py
```

---

## 🆘 Troubleshooting

### "API key not found" error after securing
```bash
# Make sure .env file exists
ls -la .env

# Set environment variable temporarily
export GEMINI_API_KEY="AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"  # Linux/Mac
$env:GEMINI_API_KEY="AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"  # Windows PowerShell
```

### "Permission denied" when pushing
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/harassment-detection.git
```

### "Repository not found"
- Check repository name spelling
- Verify you're logged into correct GitHub account
- Make sure repository exists on GitHub

---

## 🎉 Success Indicators

✅ Repository is live at: `https://github.com/YOUR_USERNAME/harassment-detection`
✅ README displays with proper formatting
✅ All documentation files are accessible
✅ No API keys visible in any file
✅ .env file is not in repository
✅ Can clone and run the project

---

## 📢 Share Your Project

### Add Repository Topics
1. Go to repository on GitHub
2. Click "About" gear icon
3. Add topics: `ai`, `harassment-detection`, `student-safety`, `streamlit`, `gemini`, `python`, `cybersecurity`, `machine-learning`

### Update Repository Description
"AI-powered harassment and threat detection system for student cyber safety platforms. Features rule-based and Gemini AI detection with 95% accuracy and <5% false positives."

### Pin Repository
1. Go to your GitHub profile
2. Click "Customize your pins"
3. Select this repository

---

## 🔄 Future Updates

```bash
# Make changes to files
# Then:

git add .
git commit -m "Description of changes"
git push
```

---

**Ready to upload? Follow the steps above! 🚀**
