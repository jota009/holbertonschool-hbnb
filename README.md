# 🏠 HBnB – Technical Documentation

---

## 🚀 Context & Objective

This repository provides a comprehensive technical blueprint for the HBnB project, an Airbnb-inspired web application.
The documentation focuses on the overall architecture, detailed business logic design, and workflow of the system, with the goal of facilitating a clear, well-organized implementation phase.
Included are all architectural diagrams, business rules, and explanations necessary for understanding, designing, and building the HBnB system.

---

## 🤔 Problem Description

**HBnB** enables the following core operations:

- **User Management**: Register, update profiles, and identify as regular users or administrators.
- **Place Management**: List properties, each with details (title, description, price, location, amenities).
- **Review Management**: Leave ratings and comments on places.
- **Amenity Management**: Manage and associate amenities with places.

---

## 📐 Business Rules & Requirements

<details>
<summary>Click for details</summary>

### **User**
- Attributes: First name, last name, email, password, admin status (boolean)
- Actions: Register, update, delete

### **Place**
- Attributes: Title, description, price, latitude, longitude, owner (user), amenities
- Actions: Create, update, delete, list

### **Review**
- Attributes: Associated user and place, rating, comment
- Actions: Create, update, delete, list (by place)

### **Amenity**
- Attributes: Name, description
- Actions: Create, update, delete, list

> **All objects have unique IDs, and creation/update timestamps for auditability.**

</details>

---

## 🏛️ Architecture Overview

The HBnB application utilizes a **three-layer architecture**:

- **Presentation Layer:**
  Exposes APIs and services for user interaction.
- **Business Logic Layer:**
  Contains models, validation, and application rules.
- **Persistence Layer:**
  Handles data storage and retrieval from the database.

> **The data flow is organized using the Facade pattern, ensuring clear separation of responsibilities and streamlined communication between layers.**

---

## 🎯 Tasks & Diagrams

### **Part 1: Technical Documentation**

- **High-Level Package Diagram**
  _Illustrates the three-layer architecture and the connections between layers via the Facade pattern._

- **Detailed Class Diagram (Business Logic Layer)**
  _Displays the main entities (User, Place, Review, Amenity), their attributes, methods, and relationships._

- **Sequence Diagrams (API Flows)**
  _Depicts the data flow for key API calls: user registration, place creation, review submission, and fetching places._

- **Comprehensive Documentation**
  _All diagrams are compiled with clear explanatory notes for effective reference and onboarding._

---

## 🗂️ Documentation & Resources

### 📄 Full Technical Document

👉 [View the complete technical documentation (Google Docs, pageless, with diagrams)](https://docs.google.com/document/d/1ynYTWRd_IWtzCkeCUrOlqu1C_c3d0uksw3TOM17Tz6k/edit?usp=sharing)

> _For optimal viewing, use Google Docs in pageless mode. All diagrams are included and are never cut off._

---

### 🔗 Useful Resources

- [UML Basics](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-uml/)
- [UML Package Diagram Guide](https://www.lucidchart.com/pages/uml-package-diagram)
- [UML Class Diagram Tutorial](https://www.uml-diagrams.org/class-diagrams-overview.html)
- [UML Sequence Diagram Tutorial](https://www.uml-diagrams.org/sequence-diagrams.html)
- [Mermaid.js Documentation](https://mermaid-js.github.io/)
- [draw.io](https://app.diagrams.net/)
