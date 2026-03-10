# 🥛 MilkMan — Milk Delivery Management System

MilkMan is a **local milk delivery management system** designed to streamline operations for dairy vendors.  
It includes an **admin dashboard**, **customer portal**, and a **backend API** for managing products, subscriptions, and orders.

The system allows dairy businesses to manage customers, staff, recurring milk subscriptions, and product deliveries efficiently.

---

# 🚀 Features

### 🛠 Admin Dashboard
- Secure admin authentication
- Manage customers and staff
- Manage product categories
- Add/edit/delete products
- Manage subscriptions
- Manage orders and delivery tracking
- Operational dashboard with system data

### 👤 Customer Website
- Customer signup and login
- Browse milk and dairy products
- Start recurring subscriptions
- View subscription plans
- Manage profile
- View order history

### ⚙ Backend API
- JWT-based authentication
- Role-based access control
- RESTful APIs for all entities
- Subscription lifecycle management
- Order management system

---

# 🏗 System Architecture

```
Customer Browser
      │
      ▼
Customer Website (HTML + JS)
      │
      │ HTTP API Calls
      ▼
Flask Backend (Port 5000)
      │
      ▼
SQLite Database

Admin Browser
      │
      ▼
AngularJS Admin Dashboard
      │
      │ HTTP API Calls
      ▼
Flask Backend
```

---

# 🧰 Tech Stack

## Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- SQLite
- python-dotenv

## Admin Frontend
- AngularJS
- ngRoute
- Bootstrap
- JavaScript
- HTML / CSS

## Customer Website
- HTML
- CSS
- JavaScript
- Bootstrap

## Local Development
- Node.js
- npm
- Express static server

---

# 📂 Project Structure

```
Milk-Man-Project/
│
├── AI_CONTEXT.md
├── README.md
├── milk man run process.md
├── venv/
│
└── MilkMan/
    │
    ├── backend/
    │   ├── run.py
    │   ├── seed.py
    │   ├── manage_accounts.py
    │   ├── config.py
    │   ├── requirements.txt
    │   ├── milkman.db
    │   │
    │   └── app/
    │       ├── __init__.py
    │       ├── authz.py
    │       ├── models/
    │       └── routes/
    │
    ├── frontend/
    │   ├── package.json
    │   ├── server.js
    │   ├── app.js
    │   ├── controllers/
    │   ├── views/
    │   └── assets/
    │
    └── customer-site/
        ├── app.js
        ├── index.html
        ├── products.html
        ├── login.html
        ├── dashboard.html
        ├── style.css
        └── assets/images/products/
```

---

# ⚡ Quick Start

Follow these steps to run the project locally.

---

# 1️⃣ Start Backend

Open terminal in project root:

```bash
cd MilkMan/backend
..\..\venv\Scripts\python.exe seed.py
..\..\venv\Scripts\python.exe manage_accounts.py
..\..\venv\Scripts\python.exe run.py
```

Backend will start at:

```
http://127.0.0.1:5000
```

---

# 2️⃣ Start Admin Dashboard

Open another terminal:

```bash
cd MilkMan/frontend
npm install
npm start
```

Admin dashboard will run at:

```
http://127.0.0.1:3000/
```

---

# 3️⃣ Open Customer Website

The customer website is served by the same frontend server:

```
http://127.0.0.1:3000/customer/
```

---

# 🔐 Default Credentials

### Admin

```
Email: admin@milkman.com
Password: MilkManAdmin@2026
```

### Customer

```
Email: customer@milkman.com
Password: MilkManUser@2026
```

Running `manage_accounts.py` resets these credentials.

---

# 🧀 Product Image System

Product images are stored in:

```
MilkMan/customer-site/assets/images/products/
```

### Image Priority

1️⃣ Backend image field  
2️⃣ Local fallback image  
3️⃣ Default fallback image  

Supported formats:

```
jpg
jpeg
png
webp
avif
svg
```

Example filenames:

```
milk.jpg
curd.jpg
paneer.jpg
ghee.jpg
butter.jpg
default-dairy.jpg
```

---

# 🧠 Development Notes

- Admin frontend communicates directly with Flask API
- Customer site uses plain JavaScript
- JWT tokens are used for authentication
- Admin token stored in `localStorage`
- Customer token stored in cookies/session storage

---

# 🔧 Extending the Project

### Add Backend Feature

Add new routes in:

```
backend/app/routes/
```

Add new models in:

```
backend/app/models/
```

---

### Add Admin Page

1. Add route in:

```
frontend/app.js
```

2. Add controller in:

```
frontend/controllers/
```

3. Add view in:

```
frontend/views/
```

---

### Add Customer Feature

Modify:

```
customer-site/app.js
customer-site/*.html
customer-site/style.css
```

---

# 📸 Screenshots

Add screenshots here to showcase the project:

- Admin Dashboard
- Customer Website
- Product Page
- Subscription Flow

---

# 🧪 API

Backend API base URL:

```
http://127.0.0.1:5000
```

Example endpoints:

```
POST /api/auth/admin/login
POST /api/auth/customer/login
GET /api/products
GET /api/orders
GET /api/subscriptions
```

---

# 🛠 Troubleshooting

### Backend not starting

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Frontend not loading

Delete node modules and reinstall:

```bash
rm -rf node_modules
npm install
```

---

### Product images not appearing

Check images exist in:

```
MilkMan/customer-site/assets/images/products/
```

Use filenames like:

```
milk.jpg
curd.jpg
paneer.jpg
```

---

# 📜 License

This project is for educational and development purposes.

---

# 👨‍💻 Author

Developed by **Anas Jahagirdar**
