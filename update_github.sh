#!/bin/bash
# Quick script to update GitHub repository

echo "🔄 Updating GitHub repository..."

# Add all changes
echo "📝 Adding changes..."
git add .

# Ask for commit message
echo "💬 Enter commit message (or press Enter for default):"
read -r commit_message

if [ -z "$commit_message" ]; then
    commit_message="Update project files"
fi

# Commit changes
echo "💾 Committing changes..."
git commit -m "$commit_message"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push

echo "✅ Repository updated successfully!"
