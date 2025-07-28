# run_project.ps1
Write-Host "Temporarily allowing script execution..."
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Write-Host "Navigating to project folder..."
cd "C:\Users\gauta\OneDrive\Desktop\adobe_round2"

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Running main script..."
python apps\main.py
