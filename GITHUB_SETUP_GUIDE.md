# 🚀 ScoutIQ GitHub Setup Guide

This guide will help you push your ScoutIQ project to GitHub and make it available for deployment on any device.

## Prerequisites

1. **Git configured** with your name and email
2. **GitHub account** 
3. **GitHub CLI** (recommended) or manual setup

## Quick Setup (Automated)

Run the automated setup script:

```bash
./SETUP_GITHUB.sh
```

This script will:
- ✅ Check your Git configuration
- ✅ Install GitHub CLI if needed
- ✅ Authenticate with GitHub
- ✅ Create the repository
- ✅ Push all files to GitHub
- ✅ Set up the remote origin

## Manual Setup

If you prefer to set up manually:

### 1. Configure Git (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Install GitHub CLI (Optional but Recommended)

**macOS:**
```bash
brew install gh
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 3. Authenticate with GitHub

```bash
gh auth login
```

Choose:
- GitHub.com
- HTTPS
- Login with a web browser

### 4. Create Repository

**Option A: Using GitHub CLI**
```bash
gh repo create ScoutIQ --public --description "AI Property Intelligence Companion - React + Mapbox frontend with FastAPI backend"
```

**Option B: Manual (via GitHub.com)**
1. Go to https://github.com/new
2. Repository name: `ScoutIQ`
3. Description: `AI Property Intelligence Companion - React + Mapbox frontend with FastAPI backend`
4. Set to Public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### 5. Add Remote and Push

```bash
# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/ScoutIQ.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: ScoutIQ AI Property Intelligence Platform"

# Push to GitHub
git push -u origin main
```

## After Setup

### 1. Update README.md

Replace `YOUR_USERNAME` in the README.md with your actual GitHub username:

```bash
# Find and replace in README.md
sed -i '' 's/YOUR_USERNAME/your_actual_username/g' README.md
```

### 2. Test Clone on Another Device

```bash
git clone https://github.com/YOUR_USERNAME/ScoutIQ.git
cd ScoutIQ
./START.sh
```

### 3. Share Your Repository

Your repository will be available at:
`https://github.com/YOUR_USERNAME/ScoutIQ`

## Repository Structure

Your GitHub repository will include:

```
ScoutIQ/
├── README.md                 # Comprehensive documentation
├── .gitignore               # Git ignore rules
├── START.sh                 # Main launcher script
├── start_backend.sh         # Backend launcher
├── start_frontend.sh        # Frontend launcher
├── TEST_INTEGRATION.sh      # Integration tests
├── SETUP_GITHUB.sh          # GitHub setup script
├── backend/                 # FastAPI backend
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── ...
├── frontend/                # React frontend
│   ├── package.json
│   ├── src/
│   └── ...
├── docs/                    # Documentation
└── data/                    # Sample data (gitignored)
```

## Deployment Options

Once on GitHub, you can deploy using:

### 1. Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create scoutiq-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### 2. Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### 3. DigitalOcean App Platform
- Connect your GitHub repository
- Configure build settings
- Deploy automatically

### 4. Docker
```bash
# Build Docker image
docker build -t scoutiq .

# Run container
docker run -p 8000:8000 scoutiq
```

## Security Notes

- ✅ `.env` files are gitignored (contains sensitive tokens)
- ✅ `node_modules/` is gitignored (can be reinstalled)
- ✅ `venv/` is gitignored (can be recreated)
- ✅ Large data files are gitignored
- ✅ Log files are gitignored

## Next Steps

1. **Set up CI/CD** with GitHub Actions
2. **Add issue templates** for bug reports and feature requests
3. **Set up branch protection** rules
4. **Add contributors** if working in a team
5. **Create releases** for version management

## Troubleshooting

### Git Authentication Issues
```bash
# Use personal access token instead of password
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/ScoutIQ.git
```

### Large File Issues
```bash
# If you have large files, use Git LFS
git lfs track "*.csv"
git lfs track "*.zip"
git add .gitattributes
```

### Permission Issues
```bash
# Make sure you have write access to the repository
gh repo view YOUR_USERNAME/ScoutIQ --json permissions
```

---

**Happy coding! 🚀**

Your ScoutIQ project is now ready to be shared and deployed anywhere!
