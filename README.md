# 🏷️ Stockly - Inventory Management API

![Django](https://img.shields.io/badge/Django-5.2.6-green)
![DRF](https://img.shields.io/badge/DRF-3.16.1-blue)
![JWT](https://img.shields.io/badge/JWT-Auth-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue)

 An ***Inventory Management API*** using ***Django and Django REST Framework***. This API will allow users to manage inventory items by adding, updating, deleting, and viewing current inventory levels. A fully functional API that stores inventory data, manages users, and tracks inventory levels, simulating a real-world scenario in managing inventory for a store. The project will cover key aspects such as **CRUD** operations, database management, and user authentication.

---

## 🚀 Features

### 🔐 Authentication & Security
- **JWT Token Authentication** – Secure API access  
- **User Registration & Profile Management** – Complete user system  
- **Role-based Access Control** – Admin and regular user permissions  
- **Password Management** – Secure password change functionality  

### 📦 Inventory Management
- **Complete CRUD Operations** – Create, read, delete inventory items  
- **Real-time Stock Tracking** – Automatic quantity updates  
- **Low Stock Alerts** – Intelligent notifications for restocking  
- **Barcode Support** – Unique barcode tracking per user  
- **Category Management** – Organized product categorization  

### 🔍 Advanced Features
- **Audit Trail** – Complete inventory change history  
- **Supplier Management** – Vendor and supplier tracking  
- **Real-time Notifications** – In-app alert system  
- **Advanced Filtering & Search** – Multi-field search capabilities  
- **Inventory Analytics** – Comprehensive reporting and insights  
- **Pagination** – Efficient handling of large datasets  

### 📊 Business Intelligence
- **Inventory Valuation** – Total inventory value calculations  
- **Stock Movement Analysis** – Sales, restocks, returns, and damages tracking  
- **Low Stock Monitoring** – Automatic detection and alerts  
- **Business Profile Management** – Company information and branding  

---

## 🛠 Tech Stack
- **Backend**: Django 5.2.6, Django REST Framework 3.16.1  
- **Database**: PostgreSQL (with SQLite support for development)  
- **Authentication**: JWT Tokens with Simple JWT  
- **API Documentation**: DRF Spectacular  
- **Filtering**: Django Filter  
- **Image Handling**: Pillow  
- **UUID Generation**: ShortUUID for compact primary keys  

---

## 📋 Prerequisites
- Python 3.13+  
- PostgreSQL (recommended) or SQLite  
- pip (Python package manager)  

---

## 📚 API Endpoints

---

### 🔑 Authentication

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| POST | `/api/v1/register/` | User registration | Public |
| POST | `/api/v1/login/` | JWT token obtainment | Public |
| POST | `/api/v1/token/refresh/` | Token refresh | Authenticated |
| POST | `/api/v1/change-password/` | Password change | Authenticated |

---

### 👤 User Management

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/users/` | List all users | Admin Only |
| GET | `/api/v1/profile/` | User profile | Authenticated |
| PATCH | `/api/v1/profile/update/` | Update profile | Authenticated |

---

### 📦 Inventory Management

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/inventory/user/` | User's inventory items | Authenticated |
| POST | `/api/v1/inventory/create/` | Create inventory item | Authenticated |
| GET | `/api/v1/inventory/<id>/` | Get inventory item | Authenticated |
| PUT | `/api/v1/inventory/<id>/update/` | Update inventory item | Owner Only |
| DELETE | `/api/v1/inventory/<id>/delete/` | Delete inventory item | Owner Only |

---

### 🗂 Categories

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/categories/` | List categories | Authenticated |
| POST | `/api/v1/category/create/` | Create category | Admin Only |
| GET | `/api/v1/category/<id>/` | Get category | Authenticated |
| PUT | `/api/v1/category/<id>/update/` | Update category | Admin Only |
| DELETE | `/api/v1/category/<id>/delete/` | Delete category | Admin Only |

---

### 🧾 Suppliers

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/suppliers/` | List user's suppliers | Authenticated |
| POST | `/api/v1/supplier/create/` | Create supplier | Authenticated |
| GET | `/api/v1/supplier/<id>/` | Get supplier | Authenticated |
| PUT | `/api/v1/supplier/<id>/update/` | Update supplier | Owner Only |
| DELETE | `/api/v1/supplier/<id>/delete/` | Delete supplier | Owner Only |

---

### 🔁 Inventory Changes & History

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/inventory-changes/` | List inventory changes | Authenticated |
| POST | `/api/v1/inventory-changes/` | Create inventory change | Authenticated |
| GET | `/api/v1/inventory-changes/<id>/` | Get change details | Authenticated |

---

### 🔔 Notifications

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/notifications/` | List notifications | Authenticated |
| PUT | `/api/v1/notifications/<id>/` | Update notification | Owner Only |
| DELETE | `/api/v1/notifications/<id>/delete/` | Delete notification | Owner Only |

---

### 📈 Reports

| Method | Endpoint | Description | Access |
|--------|-----------|-------------|---------|
| GET | `/api/v1/inventory-report/` | Inventory analytics | Authenticated |

---

## 🗃 Data Models

### 🧩 Core Models

| Model | Description |
|--------|--------------|
| **CustomUser** | Extended Django user with UUID and profile linkage |
| **Profile** | Business information and company details |
| **Category** | Product categorization system |
| **InventoryItem** | Core inventory tracking with pricing and stock levels |
| **Supplier** | Vendor and supplier management |
| **InventoryChange** | Audit trail for all stock movements |
| **Notification** | Real-time alert system |

---

### ⚙️ Key Features in Models

| Feature | Description |
|----------|--------------|
| **UUID Primary Keys** | ShortUUID for compact, unique identifiers |
| **Automatic Timestamps** | `created_at` and `updated_at` tracking |
| **User-specific Data Isolation** | Users only access their own data |
| **Business Logic Properties** | Includes `is_low_stock` and `total_value` calculations |
| **Automatic Notifications** | Real-time alerts for inventory events |

---

## 🛡 Security Features

| Security Measure | Description |
|------------------|-------------|
| **JWT Authentication** | Secure token-based access |
| **Permission Classes** | Role-based access control |
| **Data Validation** | Comprehensive input validation |
| **User Isolation** | Users can only access their own data |
| **Password Security** | Secure hashing and validation |


---

## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone REPOSITORY URL
cd stockly-inventory-api

python -m venv venv
source venv/bin/activate