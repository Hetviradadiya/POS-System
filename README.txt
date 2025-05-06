
# 🍽️ POS Restaurant System

A Point of Sale system for managing restaurant operations including table orders, inventory, billing, and reports. Built using **Django**, **PostgreSQL**, and **Bootstrap**.

## 🚀 Features

- Admin & Staff panel
- Manage tables, categories, inventory
- Add customer orders
- Print invoices
- Sales & profit reports
- Role-based access
- OTP email verification

## 📦 Technologies

- Python 3.10
- Django
- PostgreSQL / MySQL
- Bootstrap, HTML, CSS
- JavaScript (basic)
- Git

## 🛠️ Setup Instructions

### 1. Create Virtual Environment
```
python -m venv POS
POS\Scripts\activate   # On Windows
# OR
source POS/bin/activate   # On Linux/macOS

cd POS
```

### 2. Clone the Repository
```
git clone https://github.com/Hetviradadiya/POS-System
cd POS-System
```

### 3. Install Requirements
```
pip install -r requirements.txt
```

### 4. Database Setup

Ensure PostgreSQL (or MySQL) is running and create a database.

Edit `settings.py` with your DB credentials:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'posdb',
        'USER': 'yourusername',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run:
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```
python manage.py createsuperuser
```

### 6. Collect Static Files (if needed)
```
python manage.py collectstatic
```

### 7. Run the Server
```
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

## 📂 Project Structure
```
pos/
├── accounts/
    ├── templates/
    ├── static/
├── adminside/
    ├── templates/
    ├── static/
├── staffside/
    ├── templates/
    ├── static/
├── media/
├── manage.py
└── requirements.txt
```

## ✉️ Contact
For any queries, email: radadiyahetvi85@gmail.com
