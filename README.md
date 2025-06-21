# 🏠 HBnB – Technical Documentation

---

## 🚀 Context & Objective

This repository provides a comprehensive technical blueprint for the HBnB project, an Airbnb-inspired web application. The documentation focuses on the overall architecture, detailed business logic design, and workflow of the system, with the goal of facilitating a clear, well-organized implementation phase. Included are all architectural diagrams, business rules, and explanations necessary for understanding, designing, and building the HBnB system.

---

## 🤔 Problem Description

**HBnB** enables the following core operations:

- **User Management**: Register, update profiles, admin vs regular users
- **Place Management**: CRUD on properties with title, description, price, geo-coordinates, amenities
- **Review Management**: Guests leave ratings & comments on places
- **Amenity Management**: Define and associate amenities (e.g. Wi-Fi, Pool)

---

## 📐 Business Rules & Requirements

<details>
<summary>Click for details</summary>

### **User**
- **Attributes:** `first_name` (≤50 chars), `last_name` (≤50 chars), `email` (unique, valid format), `is_admin`
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

> All entities use UUIDs for global uniqueness and carry `created_at` / `updated_at` timestamps.

</details>

---

## 🏛️ Architecture Overview

The HBnB application follows a **three-layer architecture**:

1. **Presentation Layer (Flask-RESTX)**
   - Exposes versioned RESTful APIs
2. **Business Logic Layer (Models + Facade)**
   - OOP classes with validation, relationships, in-memory storage
3. **Persistence Layer (In-Memory → DB)**
   - Repository interface (add/get/update/delete, get_by_attribute)
   - Swappable for a future SQLAlchemy backend

> Communication between layers is orchestrated via the **Facade pattern**, keeping each layer decoupled and testable.

---

## 🎯 Tasks & Diagrams

### **Part 1: Technical Documentation**
- **Package & Class Diagrams**: Three-layer layout + entities (User, Place, Review, Amenity)
- **Sequence Diagrams**: API flows for registration, place creation, review submission
- **Business Rules**: Detailed attribute constraints & relationships

### 🚧 **Part 2: API Implementation** 🚀

- 🏗️ **Project Scaffold**


- 💾 **In-Memory Repository**
- Abstract `Repository` interface + `InMemoryRepository` for object storage & lookup

- 🧱 **Business Logic Classes**
- `BaseModel` with UUID, `created_at`, `updated_at`, `save()`, `update()`
- Entities (`User`, `Place`, `Amenity`, `Review`) with validation & relationships

- 🛠️ **RESTful Endpoints**
- **Users**: POST / GET(all) / GET(id) / PUT
- **Amenities**: POST / GET(all) / GET(id) / PUT
- **Places**: POST / GET(all) / GET(id) / PUT (partial updates)
- **Reviews**: POST / GET(all) / GET(id) / PUT / DELETE + GET by place

- ⚙️ **Validation & Error Handling**
- Email uniqueness, name-length, geo-bounds, rating ranges
- `ValueError` → `400 Bad Request`, missing resources → `404 Not Found`

- 🧪 **Testing**
- **Unit tests** for models (pytest)
- **API tests** for end-to-end flows
- **Shell script** (`smoke_review.sh`) for quick curl smoke-tests

---

✍️ **Author**
**Josniel Ramos** • Student at Holberton School
GitHub: [@jota009](https://github.com/jota009)
