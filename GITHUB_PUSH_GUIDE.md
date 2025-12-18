# 🚀 Guide to Push Project to GitHub

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - Or use: `winget install Git.Git` in PowerShell

2. **Verify Git Installation**:
   ```bash
   git --version
   ```

## Steps to Push to GitHub

### Step 1: Initialize Git Repository (if not already done)
```bash
git init
```

### Step 2: Add Remote Repository
```bash
git remote add origin https://github.com/jaanu-oss/Phonepae.git
```

### Step 3: Add All Files
```bash
git add .
```

### Step 4: Commit Files
```bash
git commit -m "Initial commit: PhonePe Pulse Analysis Project"
```

### Step 5: Set Main Branch (if needed)
```bash
git branch -M main
```

### Step 6: Push to GitHub
```bash
git push -u origin main
```

## If You Get Authentication Errors

If you encounter authentication issues, you may need to:

1. **Use Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate a new token with `repo` permissions
   - Use token as password when pushing

2. **Or use GitHub CLI**:
   ```bash
   gh auth login
   ```

## Quick One-Liner (After Git is Installed)

```bash
git init && git remote add origin https://github.com/jaanu-oss/Phonepae.git && git add . && git commit -m "Initial commit: PhonePe Pulse Analysis Project" && git branch -M main && git push -u origin main
```

## Files to Push

The following files/folders will be pushed:
- `app.py` - Streamlit application
- `main.py` - Main script
- `requirements.txt` - Dependencies
- `README.md` - Project documentation
- `scripts/` - Data processing and visualization scripts
- `data/` - Data files (if not in .gitignore)
- `outputs/` - Generated visualizations (if not in .gitignore)
- `.gitignore` - Git ignore file
- Other configuration files

## Note

Make sure to check `.gitignore` to see which files are excluded from being pushed.


