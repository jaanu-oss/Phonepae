# PowerShell script to push PhonePe Pulse project to GitHub
# Repository: https://github.com/jaanu-oss/Phonepae

Write-Host "🚀 PhonePe Pulse - GitHub Push Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or run: winget install Git.Git" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📁 Checking repository status..." -ForegroundColor Cyan

# Check if .git exists
if (Test-Path .git) {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to initialize git repository" -ForegroundColor Red
        exit 1
    }
}

# Check if remote exists
$remoteExists = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Remote 'origin' already exists: $remoteExists" -ForegroundColor Green
} else {
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/jaanu-oss/Phonepae.git
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to add remote" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Remote added successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "📝 Adding all files..." -ForegroundColor Cyan
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to add files" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Files added" -ForegroundColor Green

Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Cyan
$commitMessage = "Initial commit: PhonePe Pulse Analysis Project with Streamlit Dashboard"
git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  No changes to commit (or commit failed)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Changes committed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🌿 Setting branch to 'main'..." -ForegroundColor Cyan
git branch -M main 2>&1 | Out-Null
Write-Host "✅ Branch set to 'main'" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "   Repository: https://github.com/jaanu-oss/Phonepae" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  You may be prompted for GitHub credentials" -ForegroundColor Yellow
Write-Host "   If using Personal Access Token, use it as password" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "   View your repository at: https://github.com/jaanu-oss/Phonepae" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Common issues:" -ForegroundColor Red
    Write-Host "   1. Authentication required - use Personal Access Token" -ForegroundColor Yellow
    Write-Host "   2. Repository might not exist or you don't have access" -ForegroundColor Yellow
    Write-Host "   3. Check your internet connection" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 To create a Personal Access Token:" -ForegroundColor Cyan
    Write-Host "   GitHub → Settings → Developer settings → Personal access tokens" -ForegroundColor Gray
}


