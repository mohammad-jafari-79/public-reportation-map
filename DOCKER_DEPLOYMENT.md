# راهنمای استقرار با Docker

این راهنما نحوه اجرای پروژه نقشه گزارشات شهری مشهد با Docker را توضیح می‌دهد.

## پیش‌نیازها

- Docker (نسخه 20.10 یا بالاتر)
- Docker Compose (نسخه 2.0 یا بالاتر)

## نصب Docker

### Windows

1. [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) را دانلود و نصب کنید
2. Docker Desktop را راه‌اندازی کنید

### Linux (Ubuntu/Debian)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### macOS

1. [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) را دانلود و نصب کنید

## راه‌اندازی در محیط Development

### 1. کلون کردن پروژه

```bash
git clone <repository-url>
cd "public reportation map"
```

### 2. اجرای پروژه با Docker Compose

```bash
docker-compose up -d
```

این دستور سه سرویس را راه‌اندازی می‌کند:

- **PostgreSQL با PostGIS**: پایگاه داده (پورت 5433)
- **Backend (FastAPI)**: API سرور (پورت 8000)
- **Frontend (Nuxt 3)**: رابط کاربری (پورت 3000)

### 3. مقداردهی اولیه دیتابیس

بعد از راه‌اندازی، باید دیتابیس را مقداردهی کنید:

```bash
# ورود به کانتینر backend
docker exec -it city_reports_backend bash

# اجرای اسکریپت مقداردهی
python init_db.py

# خروج از کانتینر
exit
```

### 4. دسترسی به برنامه

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### اطلاعات ورود Admin

- ایمیل: `admin@cityreports.com`
- رمز عبور: `admin123`

## راه‌اندازی در محیط Production

### 1. کپی کردن فایل محیطی

```bash
cp .env.example .env
```

### 2. ویرایش فایل .env

فایل `.env` را ویرایش کنید و مقادیر زیر را تغییر دهید:

```env
# پسورد دیتابیس را تغییر دهید
POSTGRES_PASSWORD=your-strong-password-here

# کلید امنیتی را تغییر دهید (حداقل 32 کاراکتر)
SECRET_KEY=your-very-long-secret-key-at-least-32-characters

# دامنه سرور خود را وارد کنید
NUXT_PUBLIC_API_BASE=https://your-domain.com/api
DOMAIN=your-domain.com
```

### 3. اجرای با docker-compose.prod.yml

```bash
docker-compose -f docker-compose.prod.yml up -d
```

این حالت شامل Nginx به عنوان Reverse Proxy است.

### 4. مقداردهی دیتابیس (مشابه Development)

```bash
docker exec -it city_reports_backend bash
python init_db.py
exit
```

### 5. تنظیم SSL (اختیاری اما توصیه می‌شود)

برای استفاده از HTTPS، می‌توانید از Let's Encrypt استفاده کنید:

```bash
# نصب certbot
sudo apt-get install certbot

# دریافت گواهی SSL
sudo certbot certonly --standalone -d your-domain.com

# کپی گواهی‌ها به پوشه nginx
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./nginx/ssl/
```

## دستورات مفید Docker

### مشاهده لاگ‌ها

```bash
# همه سرویس‌ها
docker-compose logs -f

# فقط backend
docker-compose logs -f backend

# فقط frontend
docker-compose logs -f frontend
```

### توقف سرویس‌ها

```bash
docker-compose down
```

### توقف و حذف کامل (با حذف volumes)

```bash
docker-compose down -v
```

### ری‌استارت سرویس خاص

```bash
docker-compose restart backend
docker-compose restart frontend
```

### ریبیلد کردن ایمیج‌ها

```bash
docker-compose build
docker-compose up -d
```

### مشاهده وضعیت سرویس‌ها

```bash
docker-compose ps
```

### ورود به کانتینر

```bash
# Backend
docker exec -it city_reports_backend bash

# Frontend
docker exec -it city_reports_frontend sh

# Database
docker exec -it city_reports_db psql -U postgres -d city_reports
```

## بکاپ و بازیابی

### بکاپ دیتابیس

```bash
docker exec city_reports_db pg_dump -U postgres city_reports > backup_$(date +%Y%m%d).sql
```

### بازیابی دیتابیس

```bash
cat backup_20250101.sql | docker exec -i city_reports_db psql -U postgres -d city_reports
```

### بکاپ فایل‌های آپلود شده

```bash
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz backend/uploads/
```

## عیب‌یابی

### مشکل در اتصال به دیتابیس

```bash
# بررسی وضعیت دیتابیس
docker-compose logs postgres

# تست اتصال
docker exec city_reports_db pg_isready -U postgres
```

### مشکل در بیلد کردن

```bash
# حذف ایمیج‌های قدیمی
docker-compose down
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

### مشکل در فضای دیسک

```bash
# حذف تمام ایمیج‌ها و کانتینرهای استفاده نشده
docker system prune -a --volumes
```

## بروزرسانی برنامه

```bash
# دریافت آخرین تغییرات
git pull

# ریبیلد و راه‌اندازی مجدد
docker-compose down
docker-compose build
docker-compose up -d
```

## نکات امنیتی برای Production

1. **تغییر پسوردهای پیش‌فرض**: حتماً پسورد دیتابیس و SECRET_KEY را تغییر دهید
2. **استفاده از HTTPS**: با Let's Encrypt یا گواهی SSL خود
3. **محدود کردن دسترسی پورت‌ها**: فقط پورت‌های 80 و 443 را از بیرون باز کنید
4. **بکاپ منظم**: روزانه یا هفتگی از دیتابیس بکاپ بگیرید
5. **آپدیت منظم**: Docker images را به‌روز نگه دارید
6. **Firewall**: از فایروال برای محافظت از سرور استفاده کنید

## مانیتورینگ

برای مانیتورینگ می‌توانید از ابزارهای زیر استفاده کنید:

- **Portainer**: رابط گرافیکی برای مدیریت Docker
- **Grafana + Prometheus**: مانیتورینگ پیشرفته
- **Docker Stats**: مانیتورینگ ساده

```bash
# مشاهده مصرف منابع
docker stats
```

## پشتیبانی

در صورت بروز مشکل، لاگ‌ها را بررسی کنید:

```bash
docker-compose logs -f --tail=100
```
