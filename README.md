
# 💆 MasseuseShop Backend

RESTful Backend สำหรับระบบร้านนวด  
พัฒนาโดยใช้ **Django + Django REST Framework + PostgreSQL**  
พร้อมระบบ Authentication (JWT + Cookie), Booking และ Swagger Docs  

---

## 🚀 Tech Stack
- **Python 3.12+**
- **Django 5.2**
- **Django REST Framework**
- **Poetry** (ใช้จัดการ dependencies)
- **PostgreSQL**
- **drf-yasg** (Swagger API Docs)
- **JWT (djangorestframework-simplejwt)**

---

## ⚙️ การติดตั้งและใช้งาน

### 🧩 1. Clone โปรเจกต์
```
git clone https://github.com/thanawatJP/MasseuseShop-Backend.git
```
```
cd MasseuseShop-Backend
```
### 🧩 2. ติดตั้ง Poetry
ถ้ายังไม่มี Poetry ให้ติดตั้งก่อน (ใช้แค่ครั้งแรกเท่านั้น)
```
pip install poetry
```
ตรวจสอบว่าใช้งานได้:
```
poetry --version
```
### 🧩 3. ติดตั้ง Dependencies
```
poetry install --no-root
```
### 🧩 4. ตั้งค่า Environment Variables
สร้างไฟล์ `.env` ใน root directory แล้วใส่ค่า:
```
DB_NAME=masseuseshop
DB_USER=postgres
DB_PASSWORD=supersecretpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-xxxxxx
DEBUG=True
```
### 🧩 5. เตรียม Database
เข้า virtual environment ด้วย command ด้านล่าง เมื่อใส่เสร็จจะได้ path file ให้ copy path นั้นแล้ววางลง command แล้ว enter
```
poetry env activate
```
ตรวจสอบว่า PostgreSQL รันอยู่ แล้วสั่ง:
```
python manage.py migrate
```
สร้าง superuser (optional):
```
python manage.py createsuperuser
```
### 🧩 6. รันเซิร์ฟเวอร์
```
python manage.py runserver
```

 - **http://127.0.0.1:8000/swagger/** – Swagger API Docs
 - **http://127.0.0.1:8000/redoc/** – ReDoc API Docs
 - **http://127.0.0.1:8000/api/** – API routes ทั้งหมด
