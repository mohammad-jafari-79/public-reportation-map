# Setup Script for City Reports Platform
# راهنمای نصب خودکار

Write-Host "================================" -ForegroundColor Cyan
Write-Host "نصب سامانه گزارشات شهری" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "بررسی Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python نصب شده: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python یافت نشد. لطفا Python 3.11+ نصب کنید." -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "بررسی Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js نصب شده: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js یافت نشد. لطفا Node.js 18+ نصب کنید." -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "بررسی PostgreSQL..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✓ PostgreSQL نصب شده: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ PostgreSQL یافت نشد. لطفا اطمینان حاصل کنید که PostgreSQL نصب شده است." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "نصب Backend" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Backend setup
Set-Location backend

Write-Host "ایجاد محیط مجازی Python..." -ForegroundColor Yellow
python -m venv venv

Write-Host "فعال‌سازی محیط مجازی..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "نصب وابستگی‌های Python..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "کپی فایل .env..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✓ فایل .env ایجاد شد. لطفا آن را ویرایش کنید." -ForegroundColor Green
} else {
    Write-Host "✓ فایل .env از قبل وجود دارد." -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "نصب Frontend" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Frontend setup
Set-Location frontend

Write-Host "نصب وابستگی‌های Node.js..." -ForegroundColor Yellow
npm install

Write-Host "کپی فایل .env..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✓ فایل .env ایجاد شد." -ForegroundColor Green
} else {
    Write-Host "✓ فایل .env از قبل وجود دارد." -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✓ نصب با موفقیت انجام شد!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "مراحل بعدی:" -ForegroundColor Yellow
Write-Host "1. دیتابیس PostgreSQL با نام 'city_reports' بسازید"
Write-Host "2. فایل backend/.env را ویرایش کنید"
Write-Host "3. python backend/init_db.py را اجرا کنید"
Write-Host "4. Backend: cd backend && python main.py"
Write-Host "5. Frontend: cd frontend && npm run dev"
Write-Host ""
Write-Host "برای راهنمای کامل، فایل QUICKSTART.md را مطالعه کنید."
