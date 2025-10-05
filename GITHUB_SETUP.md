# 🚀 GitHub Setup Guide

## Step-by-Step Instructions to Upload Your Project to GitHub

### Prerequisites
- Git installed on your computer
- GitHub account created

### Step 1: Initialize Git Repository

Open PowerShell/Terminal in your project folder and run:

```bash
cd "d:\harasment Model"
git init
```

### Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Add Files to Git

```bash
# Add all files
git add .

# Check what will be committed
git status
```

### Step 4: Create First Commit

```bash
git commit -m "Initial commit: AI Harassment Detection System"
```

### Step 5: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** button (top right)
3. Select **"New repository"**
4. Fill in:
   - **Repository name**: `harassment-detection` (or your preferred name)
   - **Description**: "AI-powered harassment and threat detection system for student safety"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README (we already have one)
5. Click **"Create repository"**

### Step 6: Connect Local to GitHub

GitHub will show you commands. Use these:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/harassment-detection.git

# Verify remote
git remote -v
```

### Step 7: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

### Step 8: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded!

---

## 🔐 IMPORTANT: Secure Your API Key

### Before Pushing to GitHub:

1. **Remove API key from code:**

Edit `ai_detection.py` (line 14):
```python
# Before:
GEMINI_API_KEY = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"

# After:
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
```

2. **Create .env file** (already in .gitignore):
```bash
echo "GEMINI_API_KEY=AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8" > .env
```

3. **Update aiDetection.ts** (line 10):
```typescript
// Before:
const GEMINI_API_KEY = "AIzaSyDJj2hwB41_RAG1Tk-lN3bH4W4pvRQUGC8"

// After:
const GEMINI_API_KEY = process.env.NEXT_PUBLIC_GEMINI_API_KEY || ""
```

4. **Commit the changes:**
```bash
git add .
git commit -m "Secure API key using environment variables"
git push
```

---

## 📁 What Gets Uploaded

✅ **Included:**
- All Python files (`.py`)
- TypeScript files (`.ts`)
- Documentation (`.md`)
- Requirements files
- License
- .gitignore

❌ **Excluded (by .gitignore):**
- Virtual environment (`.venv/`)
- Python cache (`__pycache__/`)
- API keys (`.env`)
- Uploaded files
- IDE settings

---

## 🔄 Future Updates

### To update your GitHub repository:

```bash
# 1. Make changes to your files

# 2. Stage changes
git add .

# 3. Commit with message
git commit -m "Description of changes"

# 4. Push to GitHub
git push
```

### Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# View differences
git diff
```

---

## 🌟 Make Your Repository Stand Out

### Add Topics/Tags on GitHub:
1. Go to your repository
2. Click "About" (gear icon)
3. Add topics: `ai`, `harassment-detection`, `student-safety`, `streamlit`, `gemini`, `cybersecurity`

### Add Repository Description:
"AI-powered harassment and threat detection system for student cyber safety platforms. Features rule-based and Gemini AI detection with 95% accuracy."

### Pin Repository:
1. Go to your GitHub profile
2. Click "Customize your pins"
3. Select this repository

---

## 📊 GitHub Repository Features

### Enable GitHub Pages (Optional):
1. Go to Settings → Pages
2. Select branch: `main`
3. Select folder: `/docs` or `root`
4. Your documentation will be live!

### Add Repository Badges:
Already included in README.md:
- Python version
- Streamlit version
- License

### Create Releases:
```bash
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied"
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/harassment-detection.git
```

### Issue: "Repository not found"
- Check repository name spelling
- Verify you're logged into correct GitHub account
- Make sure repository exists on GitHub

### Issue: "Failed to push"
```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### Issue: "Large files rejected"
```bash
# Remove large files from git
git rm --cached large_file.ext
git commit -m "Remove large file"
git push
```

---

## ✅ Checklist Before Pushing

- [ ] API keys removed from code
- [ ] .env file created (not committed)
- [ ] .gitignore file present
- [ ] README.md updated
- [ ] All files added (`git add .`)
- [ ] Changes committed
- [ ] Remote repository created on GitHub
- [ ] Remote added to local repo
- [ ] Pushed to GitHub

---

## 🎉 Success!

Your project is now on GitHub! Share the link:
```
https://github.com/YOUR_USERNAME/harassment-detection
```

### Next Steps:
1. ⭐ Star your own repository
2. 📝 Add more documentation
3. 🐛 Create issues for future features
4. 🤝 Invite collaborators
5. 📢 Share with the community!

---

**Need Help?**
- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/docs/gittutorial
- GitHub Desktop (GUI): https://desktop.github.com/
