# Setting Up Your Private Development Repository

This guide helps you create a private GitHub repository for your personal ThreatGPT development files.

## Step 1: Create a Private Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Name it: `ThreatGPT-Personal-Dev` (or any name you prefer)
4. **Important**: Set visibility to **Private** ⚠️
5. Don't initialize with README (we already have one locally)
6. Click **"Create repository"**

## Step 2: Connect Your Local Repository

After creating the repository on GitHub, run these commands in PowerShell:

```powershell
cd "C:\Users\MY PC\OneDrive\Documents\ThreatGpt\personal_dev"

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/Thundastormgod/ThreatGPT-Personal-Dev.git

# Push your files to the private repository
git push -u origin master
```

## Step 3: Setting Up on a New Device

When you get a new device:

```powershell
# Navigate to your ThreatGPT directory
cd "C:\Users\YOUR_USERNAME\Documents\ThreatGpt"

# Clone your private repository
git clone https://github.com/Thundastormgod/ThreatGPT-Personal-Dev.git personal_dev

# Your personal files are now available!
```

## Step 4: Daily Workflow

### When you make changes to personal files:

```powershell
cd personal_dev

# Check what changed
git status

# Add your changes
git add .

# Commit with a message
git commit -m "Updated test scripts"

# Push to sync across devices
git push
```

### When working on a new device:

```powershell
cd personal_dev

# Pull latest changes
git pull
```

## What's in Your Private Repository?

- ✅ All debug scripts (`debug_*.py`)
- ✅ All test scripts (`test_*.py`)
- ✅ Demo and experimental code
- ✅ Utility scripts
- ✅ Any personal working files

## Important Notes

⚠️ **Never make this repository public** - it contains development files not meant for production

✅ **The main ThreatGPT repository stays clean** - only production-ready code

✅ **Easy sync across devices** - commit and push from any device

✅ **Independent version control** - changes here don't affect the public repo

## Repository Structure

```
ThreatGpt/                    # Public repository (for team)
├── src/
├── templates/
└── personal_dev/             # Private repository (just for you) ← IGNORED by main repo
    ├── debug_*.py
    ├── test_*.py
    └── demo_*.py
```

## Troubleshooting

**Q: I accidentally pushed personal files to the public repo**
A: They're now in .gitignore and removed from tracking. Future changes won't be pushed.

**Q: Can my teammates see my personal files?**
A: No! The `personal_dev/` folder is in .gitignore and has its own private repository.

**Q: How do I add new files to my private repo?**
A: Just put them in `personal_dev/`, then `git add`, `git commit`, and `git push` from that directory.
