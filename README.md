# نقشه گزارشات شهری مشهد 🗺️

سامانه ثبت و مشاهده گزارشات شهری با امکان تگ‌گذاری ارگان‌های مرتبط

## ویژگی‌ها ✨

- 🗺️ نمایش گزارشات روی نقشه OpenStreetMap
- 📝 ثبت گزارش با عکس و موقعیت جغرافیایی
- 👍 سیستم رای‌گیری (upvote)
- 🏢 تگ ارگان‌های مختلف (شهرداری، آتش‌نشانی، برق و...)
- 🔐 سیستم احراز هویت کاربران
- 👨‍💼 پنل مدیریت برای ادمین‌ها
- 📸 فشرده‌سازی خودکار تصاویر
- 📱 طراحی ریسپانسیو

## تکنولوژی‌ها 🛠️

### Backend

- Python 3.11+
- FastAPI
- PostgreSQL + PostGIS
- SQLAlchemy
- JWT Authentication
- Pillow (Image Processing)

### Frontend

- Vue 3
- Nuxt 3
- Tailwind CSS
- Leaflet.js
- Pinia

## نصب و راه‌اندازی 🚀

### پیش‌نیازها

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ با PostGIS Extension

### Backend

1. نصب PostgreSQL و ایجاد دیتابیس:

```bash
# در PostgreSQL:
CREATE DATABASE city_reports;
\c city_reports
CREATE EXTENSION postgis;
```

2. نصب وابستگی‌ها:

```bash
cd backend
pip install -r requirements.txt
```

3. تنظیم فایل `.env`:

```bash
cp .env.example .env
# فایل .env را ویرایش کنید
```

4. اجرای اسکریپت اولیه‌سازی دیتابیس:

```bash
python init_db.py
```

5. اجرای سرور:

```bash
python main.py
# یا
uvicorn main:app --reload
```

سرور روی `http://localhost:8000` اجرا می‌شود.
مستندات API: `http://localhost:8000/docs`

### Frontend

1. نصب وابستگی‌ها:

```bash
cd frontend
npm install
```

2. اجرای سرور توسعه:

```bash
npm run dev
```

فرانت‌اند روی `http://localhost:3000` اجرا می‌شود.

## اطلاعات ورود پیش‌فرض 🔑

**ادمین:**

- ایمیل: `admin@cityreports.com`
- رمز عبور: `admin123`

⚠️ **مهم:** قبل از استفاده در محیط واقعی، حتماً رمز ادمین را تغییر دهید!

## ساختار پروژه 📁

```
.
├── backend/
│   ├── app/
│   │   ├── routers/         # API endpoints
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── auth.py          # Authentication
│   │   ├── database.py      # Database config
│   │   ├── config.py        # Settings
│   │   └── utils.py         # Utilities
│   ├── main.py              # FastAPI app
│   ├── init_db.py           # Database initialization
│   └── requirements.txt
│
└── frontend/
    ├── pages/               # Nuxt pages
    ├── components/          # Vue components
    ├── stores/              # Pinia stores
    ├── composables/         # Composables
    ├── layouts/             # Layouts
    ├── plugins/             # Plugins
    └── assets/              # Static assets
```

## API Endpoints 📡

### Authentication

- `POST /api/auth/register` - ثبت‌نام
- `POST /api/auth/login` - ورود
- `GET /api/auth/me` - اطلاعات کاربر

### Reports

- `GET /api/reports/` - لیست گزارشات
- `GET /api/reports/{id}` - جزئیات گزارش
- `POST /api/reports/` - ثبت گزارش جدید
- `POST /api/reports/{id}/vote` - رای دادن
- `DELETE /api/reports/{id}/vote` - حذف رای

### Public

- `GET /api/organizations` - لیست ارگان‌ها
- `GET /api/categories` - لیست دسته‌بندی‌ها

### Admin

- `GET /api/admin/reports` - لیست کامل گزارشات
- `PATCH /api/admin/reports/{id}` - تغییر وضعیت
- `DELETE /api/admin/reports/{id}` - حذف گزارش
- `GET /api/admin/stats` - آمار کلی

## توسعه 🔧

### اضافه کردن ارگان جدید

در فایل `backend/init_db.py` ارگان جدید را اضافه کنید.

### اضافه کردن دسته‌بندی جدید

در فایل `backend/init_db.py` دسته‌بندی جدید را اضافه کنید.

### تغییر محدوده نقشه

در فایل `frontend/pages/index.vue` مختصات و zoom را تغییر دهید.

## استقرار (Deployment) 🌐

### Backend

- با Gunicorn یا Uvicorn
- نیاز به PostgreSQL با PostGIS
- تنظیم CORS برای فرانت‌اند

### Frontend

- Build: `npm run build`
- استقرار با Vercel, Netlify یا سرور Node.js

## مجوز 📄

این پروژه تحت مجوز MIT منتشر شده است.

## مشارکت 🤝

برای مشارکت:

1. Fork کنید
2. یک branch جدید بسازید
3. تغییرات خود را commit کنید
4. Push کنید و Pull Request ایجاد کنید

## تماس 📧

برای سوالات و پشتیبانی، با ما تماس بگیرید.
