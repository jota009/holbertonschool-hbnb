# 🏠 HBnB – Technical Documentation

---

## 🚀 Context & Objective

This repository provides a comprehensive technical blueprint for the HBnB project, an Airbnb-inspired web application. The documentation focuses on the overall architecture, detailed business logic design, workflow of the system, and persistence layer, with the goal of facilitating a clear, well-organized implementation phase. Included are all architectural diagrams, business rules, and explanations necessary for understanding, designing, building, and persisting data in the HBnB system.

---

## 🤔 Problem Description

**HBnB** enables the following core operations:

- **User Management:** Register, update profiles, admin vs regular users
- **Place Management:** CRUD on properties with title, description, price, geo-coordinates, amenities
- **Review Management:** Guests leave ratings & comments on places
- **Amenity Management:** Define and associate amenities (e.g. Wi-Fi, Pool)

---

## 📐 Business Rules & Requirements

<details>
<summary>Click for details</summary>

### **User**
- **Attributes:** `first_name` (≤50 chars), `last_name` (≤50 chars), `email` (unique, valid), `is_admin`
- **Actions:** Create, Read, Update

### **Place**
- **Attributes:** `title` (≤100 chars), `description`, `price` (≥0), `latitude` (–90…90), `longitude` (–180…180), `owner` (User), `amenities`
- **Actions:** Create, Read, Update, List

### **Review**
- **Attributes:** `text` (non-empty), `rating` (1…5), `user` (User), `place` (Place)
- **Actions:** Create, Read, Update, Delete, List (by place)

### **Amenity**
- **Attributes:** `name` (≤50 chars)
- **Actions:** Create, Read, Update

> All entities use UUIDs and carry `created_at` / `updated_at` timestamps.

</details>

---

## 🏛️ Architecture Overview

The HBnB application follows a **three-layer architecture**:

1. **Presentation Layer (Flask-RESTX)**
   Exposes versioned RESTful APIs
2. **Business Logic Layer (Models + Facade)**
   OOP classes with validation, relationships, in-memory storage
3. **Persistence Layer (In-Memory → DB)**
   Repository interface + swappable SQLite/SQLAlchemy backend

> Layers communicate via the **Facade pattern** for decoupling and testability.

---

## 🎯 Tasks & Diagrams

### **Part 1: Technical Documentation**
- **Package & Class Diagrams**
- **Sequence Diagrams** (registration, place creation, review flow)
- **Business Rules** & ER diagrams (Mermaid.js)

### **Part 2: API Implementation** 🚀
- **Project Scaffold** & In-Memory Repository
- **Business Logic Classes** (`BaseModel`, `User`, `Place`, `Review`, `Amenity`)
- **RESTful Endpoints** (CRUD for all entities)
- **Validation & Error Handling**
- **Testing** (unit + smoke tests, e.g. `smoke_review.sh`)

### **Part 3: Database Integration** 🛢️
- **Database Engine:** SQLite with SQLAlchemy ORM
- **Models & Mappings:** Python classes → tables (`User`, `Place`, `Review`, `Amenity`, `PlaceAmenity`)
- **Schema Creation & Migrations:** auto-create tables, manage schema changes
- **CRUD Operations:** scripts & examples for Create, Read, Update, Delete
- **SQL Scripts:** import/export via SQL dumps; custom queries (e.g. list Comedy shows, join genres)
- **ER Diagrams:** visualize relationships with Mermaid.js
- **Testing:** model tests (pytest), SQL script validations, integration tests

### Part 4 – Frontend
- Simple, framework-free UI (HTML/CSS/JS)
- Login/Register with **JWT stored in a cookie**
- Pages for **Places list**, **Place details**, **Reviews**, and basic static pages
- Clear **loading / error / empty** states
- Accessible, responsive layout
- Small utilities for API calls and auth state

## ▶️ How to Use (High Level)
1. **Start the backend API** (Parts 2–3).
2. **Open the frontend** (Part 4) in a browser as a static site.
3. **Configure the API URL** in the frontend config file (see Part 4 README).
4. **Login/Register** to unlock authenticated actions (e.g., adding reviews).

## 🧪 Testing
- Backend: unit/integration tests for services and endpoints.
- Frontend: manual verification in the browser; E2E tools can be added later.

## 📎 Documentation
- Diagrams & notes: `docs/`
- API details: `part2/README.md`
- Database notes: `part3/README.md`
- Frontend details: `part4/README.md`
---

✍️ **Author**
**Josniel Ramos** • Student at Holberton School
GitHub: [@jota009](https://github.com/jota009)
