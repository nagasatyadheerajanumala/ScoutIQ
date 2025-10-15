#!/bin/bash

# ScoutIQ GitHub Setup Script
# This script helps you set up the GitHub repository

set -e

echo "🚀 ScoutIQ GitHub Setup"
echo "========================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if git is configured
echo "1️⃣  Checking Git Configuration..."
if ! git config --global user.name > /dev/null 2>&1; then
    echo "${RED}❌ Git user.name not configured${NC}"
    echo "Please run:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
    exit 1
fi

if ! git config --global user.email > /dev/null 2>&1; then
    echo "${RED}❌ Git user.email not configured${NC}"
    echo "Please run:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
    exit 1
fi

echo "${GREEN}✅ Git configured: $(git config --global user.name) <$(git config --global user.email)>${NC}"

# Check if GitHub CLI is installed
echo ""
echo "2️⃣  Checking GitHub CLI..."
if ! command -v gh &> /dev/null; then
    echo "${YELLOW}⚠️  GitHub CLI not installed${NC}"
    echo "Installing GitHub CLI..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install gh
        else
            echo "${RED}❌ Homebrew not found. Please install GitHub CLI manually:${NC}"
            echo "  https://cli.github.com/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh
    else
        echo "${RED}❌ Unsupported OS. Please install GitHub CLI manually:${NC}"
        echo "  https://cli.github.com/"
        exit 1
    fi
fi

echo "${GREEN}✅ GitHub CLI installed${NC}"

# Check GitHub authentication
echo ""
echo "3️⃣  Checking GitHub Authentication..."
if ! gh auth status > /dev/null 2>&1; then
    echo "${YELLOW}⚠️  Not authenticated with GitHub${NC}"
    echo "Please authenticate with GitHub:"
    echo "  gh auth login"
    echo ""
    echo "Choose:"
    echo "  - GitHub.com"
    echo "  - HTTPS"
    echo "  - Login with a web browser"
    echo ""
    read -p "Press Enter after completing GitHub authentication..."
fi

echo "${GREEN}✅ GitHub authenticated${NC}"

# Create GitHub repository
echo ""
echo "4️⃣  Creating GitHub Repository..."
echo "Repository name: ScoutIQ"
echo "Description: AI Property Intelligence Companion - React + Mapbox frontend with FastAPI backend"
echo "Visibility: Public (you can change this later)"
echo ""

# Create the repository
gh repo create ScoutIQ --public --description "AI Property Intelligence Companion - React + Mapbox frontend with FastAPI backend" --source=. --remote=origin --push

echo "${GREEN}✅ Repository created and pushed to GitHub${NC}"

# Add all files
echo ""
echo "5️⃣  Adding files to repository..."
git add .
git commit -m "Initial commit: ScoutIQ AI Property Intelligence Platform

- React + Mapbox GL JS frontend with Material-UI
- FastAPI backend with PostgreSQL + PostGIS
- AI-powered property analysis and insights
- Interactive map visualization with layer controls
- Property filtering and real-time analysis
- Professional investor-grade interface

Features:
- Property querying with county and valuation filters
- AI-generated investment recommendations (Buy/Hold/Watch)
- Interactive map with color-coded property markers
- Layer controls for heatmap, parcels, and flood zones
- Real-time AI insights panel
- Professional Material-UI design
- Responsive and mobile-friendly interface

Tech Stack:
- Frontend: React, Mapbox GL JS, Material-UI, Axios
- Backend: FastAPI, SQLAlchemy, PostgreSQL, PostGIS
- AI: Rule-based analysis with natural language generation
- Data: Travis County ATTOM property data"

echo "${GREEN}✅ Files committed${NC}"

# Push to GitHub
echo ""
echo "6️⃣  Pushing to GitHub..."
git push -u origin main

echo "${GREEN}✅ Pushed to GitHub${NC}"

# Display repository information
echo ""
echo "${GREEN}=========================================="
echo "🎉 ScoutIQ Repository Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "Repository URL: https://github.com/$(gh api user --jq .login)/ScoutIQ"
echo ""
echo "Next steps:"
echo "1. Visit your repository: https://github.com/$(gh api user --jq .login)/ScoutIQ"
echo "2. Update the README.md clone URL with your actual username"
echo "3. Share the repository with others"
echo "4. Set up GitHub Actions for CI/CD (optional)"
echo ""
echo "To clone on another device:"
echo "  git clone https://github.com/$(gh api user --jq .login)/ScoutIQ.git"
echo "  cd ScoutIQ"
echo "  ./START.sh"
echo ""
echo "${BLUE}Happy coding! 🚀${NC}"
