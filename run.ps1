# Run Backend and Frontend together
# اجرای همزمان Backend و Frontend

Write-Host "================================" -ForegroundColor Cyan
Write-Host "راه‌اندازی سامانه گزارشات شهری" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend
Write-Host "راه‌اندازی Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; python main.py"

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "راه‌اندازی Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "✓ سرویس‌ها در حال اجرا هستند!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "برای توقف، پنجره‌های PowerShell را ببندید." -ForegroundColor Yellow
