# PowerShell script to set up GitHub repository
# Run this in PowerShell: .\setup_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GitHub Setup for Harassment Detection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Secure API key
Write-Host "Step 1: Securing API key..." -ForegroundColor Yellow
python secure_api_key.py

Write-Host ""
Write-Host "Step 2: Initializing Git repository..." -ForegroundColor Yellow
git init

Write-Host ""
Write-Host "Step 3: Adding files to Git..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Step 4: Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: AI Harassment Detection System"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Local Git repository is ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com and create a new repository"
Write-Host "2. Name it: harassment-detection (or your preferred name)"
Write-Host "3. DO NOT initialize with README"
Write-Host "4. After creating, run these commands:"
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/harassment-detection.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Replace YOUR_USERNAME with your actual GitHub username!" -ForegroundColor Red
Write-Host ""

# Pause to let user read
Read-Host "Press Enter to continue..."
