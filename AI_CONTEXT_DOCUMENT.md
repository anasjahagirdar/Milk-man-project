# AI Context Document - MilkMan Project

This document provides a comprehensive overview of the MilkMan repository, designed for AI coding agents to understand the project's architecture, workflows, and runtime behavior.

---

## 1. Project Overview

**MilkMan** is a farm-to-table dairy subscription and management platform. It solves the problem of local dairy distribution by connecting farms directly to customers through a recurring delivery model.

- **Type**: Full-stack Web Application (SaaS-style)
- **Core Features**:
  - **Customer Subscriptions**: Recurring daily/weekly delivery of dairy products.
  - **Product Catalog**: Dynamic management of dairy items (Milk, Ghee, Butter, etc.).
  - **Admin Dashboard**: Comprehensive management of customers, staff, inventory, and orders.
  - **Staff Operations**: Interface for delivery staff to manage daily deployments.
  - **Automated Logging**: History of delivered supplies and payment status.

---

## 2. High-Level Architecture

The project follows a decoupled client-server architecture with two distinct frontend applications.

### System Flow
`Client (Browser) -> Frontend (Static/Express) -> Backend (Flask API) -> Database (SQLite/SQLAlchemy)`

### Components
- **Backend**: Python Flask REST API handling business logic, authentication, and database operations.
- **Customer Site**: A "Golden Morning" themed, vanilla JS/HTML frontend for end-users.
- **Admin/Staff Frontend**: A separate administrative interface built with vanilla JS and Express as a static server.
- **Database**: SQLite (default) using SQLAlchemy ORM for relational data management.

---

## 3. Directory Structure

```text
MilkMan/
├── backend/                # Flask REST API
│   ├── app/                # Application logic
│   │   ├── models/         # SQLAlchemy models (Customer, Product, Subscription, etc.)
│   │   ├── routes/         # API endpoints grouped by resource
│   │   ├── authz.py        # RBAC (Role-Based Access Control) decorators
│   │   └── main.py         # Entry point for the Flask server
│   ├── config.py           # Environment and app configuration
│   ├── run.py              # Development server script
│   └── seed.py             # Database initialization and seeding script
├── customer-site/          # Vanilla JS/HTML frontend for customers
│   ├── assets/             # Images and global configurations
│   ├── app.js              # Core customer-side logic and API communication
│   ├── dashboard.html      # Customer "Command Center"
│   └── products.html       # Product catalog and subscription initialization
├── frontend/               # Admin and Staff management interface
│   ├── controllers/        # JS logic for admin views
│   ├── views/              # HTML templates for admin/staff functions
│   ├── server.js           # Express.js server for serving static files
│   └── app.js              # Global frontend utilities
└── ecosystem.config.js     # PM2 process management configuration
```

---

## 4. Backend Analysis

- **Entry Point**: `backend/app/main.py`
- **Framework**: Flask
- **Authentication**: JWT (JSON Web Tokens) using `flask-jwt-extended`. Identity is stored as a stringified ID in the token.
- **Authorization**: Custom RBAC implemented in `app/authz.py` with `@require_roles("admin", "staff", "customer")`.
- **Database**: SQLite using SQLAlchemy. Auto-migration logic exists in `app/__init__.py` for specific schema updates.
- **Request Flow**:
  1. Request received at `routes/`.
  2. RBAC check via `@require_roles`.
  3. Logic processed using `models/`.
  4. Response returned as JSON.

---

## 5. Frontend Analysis

### Customer Site (`customer-site/`)
- **Framework**: Vanilla JS, HTML5, CSS3 (Bootstrap 5 + Custom Design System).
- **Theme**: "Golden Morning" - Warm, natural, light-themed aesthetic.
- **Communication**: Uses `window.MilkMan.apiFetch` (wrapper around `fetch`) to communicate with the Flask API.
- **State**: Session-based storage for JWT tokens (`customer_token`).

### Admin Frontend (`frontend/`)
- **Framework**: Vanilla JS with Express.js server.
- **Routing**: Client-side logic handles view switching; Express handles static file serving and SPA-style fallback.
- **Controllers**: Modular JS files in `controllers/` managing specific entities like `staffController.js` or `productController.js`.

---

## 6. Database Structure

- **Type**: SQLite (Relational)
- **ORM**: SQLAlchemy
- **Key Models**:
  - **Admin**: System administrators.
  - **Staff**: Delivery and operations personnel.
  - **Customer**: End-users with profiles and addresses.
  - **Product**: Dairy items with pricing, unit, and stock.
  - **Category**: Product groupings (e.g., "Cow Milk").
  - **Subscription**: The core link between Customer and Product with `frequency` (daily, alternate, weekly) and `status`.
  - **Order**: Historical logs of individual deliveries generated from subscriptions.

---

## 7. API Design (Major Endpoints)

| Endpoint | Method | Role | Description |
|----------|--------|------|-------------|
| `/api/auth/login` | POST | All | General login (Admin/Staff/Customer) |
| `/api/products/` | GET | All | List all active dairy products |
| `/api/customers/` | POST/GET | Admin/Staff | Manage customer profiles |
| `/api/subscriptions/`| POST/GET | All | Manage recurring delivery pipelines |
| `/api/orders/` | GET | Admin/Staff | Track delivery history and logs |

---

## 8. Deployment & Infrastructure

- **Local Development**:
  - Backend: `python backend/run.py` (Port 5000)
  - Frontend: `node frontend/server.js` (Port 3000)
- **Process Manager**: PM2 configuration in `ecosystem.config.js` for multi-service management.
- **Environment Variables**:
  - `DATABASE_URL`: Path to SQLite file.
  - `JWT_SECRET_KEY`: Security key for tokens.
  - `CORS_ORIGINS`: Allowed frontend URLs.

---

## 9. Data Flow (Request Lifecycle)

1. **User Action**: Customer clicks "Subscribe Now" in `products.html`.
2. **Frontend API Call**: `app.js` triggers `apiFetch` to `/api/subscriptions/`.
3. **Backend Route**: `routes/subscription.py` receives POST request.
4. **Logic & DB**: Route validates data, checks `current_user_id()`, and saves `Subscription` model to SQLite.
5. **Response**: Backend returns JSON of the new subscription.
6. **UI Update**: Frontend displays "Success" celebration overlay and redirects to Dashboard.

---

## 10. Security

- **JWT Usage**: All protected routes require `Authorization: Bearer <token>`.
- **Password Hashing**: `werkzeug.security` (pbkdf2:sha256).
- **CORS**: Strict origin checking configured in `backend/app/__init__.py`.
- **RBAC**: Multi-tier access control (Admin > Staff > Customer).

---

## 11. Summary for AI Agents

### Architecture Summary
MilkMan is a decoupled Flask/VanillaJS application. The backend is the source of truth for all business logic and data. Frontends are thin clients that manage presentation and local state (JWT).

### Key Files to Watch
- `backend/app/models/`: Schema definitions.
- `backend/app/routes/`: Business logic entry points.
- `customer-site/app.js`: Global customer-side API wrapper.
- `customer-site/style.css`: The "Golden Morning" design system tokens.

### Development Patterns
- **API Interaction**: Always use the `MilkMan.apiFetch` wrapper in the customer-site to ensure JWT headers are handled.
- **Naming Convention**:
  - "Pipelines" / "Chapters" are legacy cinematic terms. 
  - Use **"Subscriptions"**, **"Orders"**, and **"Products"** in natural language.
- **Modifying UI**: The customer-facing UI uses a specific CSS variable system in `style.css` (`--bg-primary`, `--accent-primary`). Do not use hardcoded hex codes.

### Safety Rules
1. **API Compatibility**: Never change backend response structures without checking both the Admin and Customer frontends.
2. **Image Fallbacks**: Always include `onerror` handlers for images using `MilkMan.products.defaultImage`.
3. **RBAC**: When adding new routes, always use the `@require_roles` decorator.
