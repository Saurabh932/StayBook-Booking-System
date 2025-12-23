# StayBook – Property Booking Platform

## 🚀 Overview
The **StayBook Property Booking Platform** is a full-stack, Airbnb-style application built using FastAPI and modern backend engineering practices.

It allows users to create and manage property listings, browse available stays, and submit reviews with star ratings. The platform enforces **strict ownership and authorization rules**, ensuring that listing owners control their properties and users can manage only their own reviews.

Designed as a **production-ready system**, StayBook features async APIs, secure JWT authentication, realistic relational data modeling, CI/CD readiness, and cloud deployment capability.

---

## 🛠 Tech Stack
- **Backend Framework:** FastAPI (Async)
- **Database:** PostgreSQL
- **ORM:** SQLModel + Async SQLAlchemy
- **Authentication:** JWT (Access Tokens)
- **Authorization:** Ownership-Based Access Control
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud Deployment:** AWS EC2
- **Frontend:** HTML, CSS, JavaScript
- **Language:** Python 3.10+

---

## 🔑 Key Features
- **JWT Authentication:** Secure login and protected routes using access tokens.
- **Ownership-Based Access Control:**
  - Only listing owners can edit or delete their properties.
  - Users can delete only the reviews they created.
- **Property Listings:**
  - Create, update, delete, and browse listings
  - Includes pricing, location, images, and descriptions
- **Review System:**
  - Star-based ratings (⭐ 1–5)
  - Comment-based reviews linked to users and listings
- **Async Backend:** Fully non-blocking database operations using async SQLAlchemy.
- **Frontend Authorization Logic:**
  - Edit/Delete buttons rendered conditionally based on logged-in user
- **Flash Messaging System:**
  - In-page success and error messages instead of browser alerts
- **Realistic Data Modeling:**
  - Proper foreign-key relationships between users, listings, and reviews

---

## 🗂 Database Design
- **User**
  - Authentication, identity, and ownership reference
- **Listing**
  - Owned by a single user
  - Stores property details (price, location, image, description, etc.)
- **Review**
  - Linked to both user and listing
  - Ownership enforced at database and service layer

All relationships are enforced using **foreign keys** and **ORM-level constraints**.

---

## 🏗 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/staybook-booking-platform.git
cd staybook-booking-platform
