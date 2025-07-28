@echo off
echo 🔄 Updating GitHub repository...

REM Add all changes
echo 📝 Adding changes...
git add .

REM Ask for commit message
set /p commit_message="💬 Enter commit message (or press Enter for default): "

if "%commit_message%"=="" (
    set commit_message=Update project files
)

REM Commit changes
echo 💾 Committing changes...
git commit -m "%commit_message%"

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push

echo ✅ Repository updated successfully!
pause
