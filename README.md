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

### روش اول: استفاده از Docker (توصیه می‌شود) 🐳

#### پیش‌نیازها

- Docker 20.10+
- Docker Compose 2.0+

#### راه‌اندازی سریع

1. **کلون کردن پروژه:**

```bash
git clone <repository-url>
cd "public reportation map"
```

2. **اجرای پروژه:**

```bash
# اجرای تمام سرویس‌ها (PostgreSQL, Backend, Frontend)
docker-compose up -d

# صبر برای بالا آمدن سرویس‌ها (حدود 30 ثانیه)
```

3. **مقداردهی اولیه دیتابیس:**

```bash
docker exec -it city_reports_backend python init_db.py
```

4. **دسترسی به برنامه:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

#### دستورات مفید Docker

```bash
# مشاهده وضعیت سرویس‌ها
docker-compose ps

# مشاهده لاگ‌ها
docker-compose logs -f

# توقف سرویس‌ها
docker-compose down

# ریبیلد و اجرای مجدد
docker-compose up -d --build
```

#### استقرار Production با Docker

1. **تنظیمات محیطی:**

```bash
cp .env.example .env
nano .env  # ویرایش و تغییر پسوردها و تنظیمات
```

2. **اجرا با Nginx:**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

برای راهنمای کامل Docker، فایل [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) را مطالعه کنید.

---

### روش دوم: نصب دستی (Manual Installation)

#### پیش‌نیازها

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ با PostGIS Extension

#### Backend

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

### با Docker (توصیه می‌شود)

#### Development

```bash
docker-compose up -d
docker exec -it city_reports_backend python init_db.py
```

#### Production

```bash
# تنظیمات .env
cp .env.example .env
# ویرایش .env و تغییر:
# - POSTGRES_PASSWORD
# - SECRET_KEY
# - NUXT_PUBLIC_API_BASE

# اجرا
docker-compose -f docker-compose.prod.yml up -d
docker exec -it city_reports_backend python init_db.py
```

**نکات امنیتی:**

- پسورد دیتابیس را تغییر دهید
- SECRET_KEY را با یک رشته تصادفی 32+ کاراکتری جایگزین کنید
- از HTTPS استفاده کنید (Let's Encrypt)
- پورت‌های غیرضروری را ببندید
- بکاپ منظم از دیتابیس بگیرید

### بدون Docker

#### Backend

- با Gunicorn یا Uvicorn
- نیاز به PostgreSQL با PostGIS
- تنظیم CORS برای فرانت‌اند

#### Frontend

- Build: `npm run build`
- استقرار با Vercel, Netlify یا سرور Node.js
