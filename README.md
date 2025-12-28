# 📦 CLI Asset Management System

A robust, robust command-line application built with Python and SQLite to help IT teams track hardware assets, manage employee assignments, and handle asset lifecycles.

This project features strong data validation, persistent storage, and a comprehensive automated tests (Pytest).

## 🚀 Features

* **Asset Management:** Add new assets, view all assets, and update status (Available, Assigned, Maintenance, Retired).
* **Employee Management:** Add employees, view directory, and offboard employees (prevents assignment to inactive staff).
* **Assignment Lifecycle:** Assign assets to employees and return them.
* **Smart Validation:**
    * Prevents assigning "Ghost" assets or employees.
    * Prevents assigning broken or already-assigned assets.
    * Validates names (no numbers allowed in employee names) and dates.
* **Input Handling:** Robust CLI interface that can handle invalid inputs 
* **Persistent Storage:** Data is saved automatically to `data.db` (SQLite).

### 🐍 Modern Python Practices
- **Type Safety:** Extensive use of `Type Hinting` and `Dataclasses` for strict data validation before it hits the database.
- **Context Managers:** Custom database connectivity using `with sqlite3.connect(...)` to ensure safe connection closing even during crashes.
- **Automated Testing:** Comprehensive test suite using `pytest` covering 100% of business logic and database integration.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Database:** SQLite3 (Native)
- **Testing:** Pytest & Pytest-Fixtures


---

## 📂 Project Structure

```text
Asset-Tracking-System/
├── src/
│   ├── database.py       # Direct SQL implementation & Schema definition
│   ├── models.py         # Data Validation Layer (Dataclasses)
├── tests/
│   ├── test_models.py    # Unit tests for logic validation
│   └── test_database.py  # Integration tests with isolation fixtures
├── main.py               # CLI Interface & Entry Point
├── requirements.txt      # Dependency list
└── README.md             # Documentation
```

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Aman00240/Asset-Tracking-System.git
cd Asset-Tracking-System
```
### 2. Set Up Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Application
```bash
python main.py
```
### 5. Run Tests
```bash
python -m pytest
```
## 📖 User Guide

Once you run `main.py`, follow the on-screen menu:

1. **Add New Asset:** Create items like Laptops, Monitors, etc.
2. **Add New Employee:** Add staff members.
3. **Assign Asset:** Link an Asset ID to an Employee ID.
4. **Return Asset:** Free up an asset to be used again.
5. **Offboard Employee:** Marks employee as inactive (cannot hold assets).
6. **View Active Assignments:** See who has what.
7. **View All Assets:** Look up IDs and Statuses.
8. **View All Employees:** Look up Employee IDs.
9. **Set Asset Status:** Mark items as MAINTENANCE or RETIRED.

## 🛡️ Validation Rules

* **Strict Typing:** Asset/Employee IDs must be numbers.
* **Name Logic:** Employee names cannot contain numbers (e.g., "Aman123" is blocked).
* **Status Check:** You cannot assign an asset unless its status is `AVAILABLE`.
* **Employee Status:** You cannot assign assets to offboarded (inactive) employees.