# Python Generators – Task 0: Database Seeding

## 📌 Project Overview

This project is part of the **ALX Backend Python – Generators** module. Task 0 focuses on setting up a MySQL database and seeding it with user data in preparation for later tasks that will introduce **Python generators** for efficient data streaming.

At this stage, the goal is to:

* Create a MySQL database
* Create a table with the required schema
* Populate the table using data from a CSV file

This database will later be used to demonstrate **memory‑efficient data processing using generators**.

---

## 🎯 Objective (Task 0)

Create a Python script (`seed.py`) that:

1. Connects to a MySQL server
2. Creates a database called `ALX_prodev` (if it does not exist)
3. Creates a table called `user_data`
4. Populates the table using data from `user_data.csv`

---

## 🗄️ Database Schema

**Database:** `ALX_prodev`

**Table:** `user_data`

| Field   | Type         | Constraints                 |
| ------- | ------------ | --------------------------- |
| user_id | CHAR(36)     | Primary Key, Indexed (UUID) |
| name    | VARCHAR(255) | NOT NULL                    |
| email   | VARCHAR(255) | NOT NULL                    |
| age     | DECIMAL      | NOT NULL                    |

---

## 📁 Project Structure

```
python-generators-0x00/
│
├── 0-main.py        # Test script provided by ALX
├── seed.py          # Database setup and seeding logic
├── user_data.csv    # Sample user data
└── README.md        # Project documentation
```

---

## 🛠️ Requirements

* Python 3.x
* MySQL Server
* `mysql-connector-python`

Install the MySQL connector if needed:

```bash
pip install mysql-connector-python
```

---

## ▶️ How to Run

1. Ensure MySQL server is running
2. Update your MySQL credentials in `seed.py`
3. Run the test script:

```bash
chmod +x 0-main.py
./0-main.py
```

### Expected Output

```
connection successful
Table user_data created successfully
Database ALX_prodev is present
[(...), (...), ...]
```


