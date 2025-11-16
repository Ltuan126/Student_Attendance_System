# 🧾 Student Attendance System (CLI Version)

## 📌 1. Introduction
The Student Attendance System (SAS) is developed to support attendance recording and management for students and lecturers. The application runs as a Command Line Interface (CLI) and stores data in plain `.txt` files — no database is required.

---

## ⚙️ 2. Project structure

```
SAS_Project/
 ├── main.py
 ├── models/
 │    ├── user.py
 │    ├── academic.py
 │    ├── attendance.py
 │    └── correction.py
 ├── services/
 │    ├── auth_service.py
 │    ├── timetable_service.py
 │    ├── attendance_service.py
 │    ├── correction_service.py
 │    ├── report_service.py
 │    └── admin_service.py
 ├── cli/
 │    ├── main_menu.py
 │    ├── student_menu.py
 │    ├── lecturer_menu.py
 │    └── admin_menu.py
 ├── data/
 │    ├── users.txt
 │    ├── courses.txt
 │    ├── classes.txt
 │    ├── sessions.txt
 │    ├── class_student.txt
 │    ├── attendance.txt
 │    └── corrections.txt
 ├── tests/
 │    ├── test_auth.py
 │    ├── test_timetable.py
 │    ├── test_attendance.py
 │    └── test_correction_report.py
 └── README.md
```

---

## 👨‍💻 3. How to run

### 🔧 Requirements
- Python **>= 3.11**
- `pytest` (optional, for running tests)
- OS: Windows / macOS / Linux

### 🚀 Run the application

Open a terminal in the project folder and run:
```bash
python main.py
```

On startup the program shows:
```
===========================
Student Attendance System – CLI Version
===========================
(1) Login
(2) Register
(0) Exit
```

- If logged in as a **Student**, the menu contains:
  ```
  (1) View Timetable
  (2) Check-in Attendance
  (3) View Attendance History
  (4) Request Attendance Correction
  (0) Logout
  ```
- If logged in as a **Lecturer**, the menu contains:
  ```
  (1) View Teaching Schedule
  (2) Take Attendance
  (3) Review Correction Requests
  (4) Generate Attendance Report
  (0) Logout
  ```
- If logged in as an **Admin**, the menu contains:
  ```
  (1) Manage Users
  (2) Manage Courses
  (3) Manage Classes
  (4) Import Roster
  (5) View System Reports
  (0) Logout
  ```

### Docker

Build the CLI image (context is the project root):
```bash
docker build -t sas-cli .
```

Run the CLI inside a disposable container:
```bash
docker run -it --rm sas-cli
```

---

## 🧩 4. Main features

| Feature group | Description |
|---------------|-------------|
| **1. Authentication** | User registration and login (Student, Lecturer, Admin). |
| **2. Timetable Management** | Students can view timetables; data comes from `sessions.txt`. |
| **3. Attendance Management** | Students can check in; lecturers can take attendance and view history. |
| **4. Correction Handling** | Students can request attendance corrections; lecturers can review requests. |
| **5. Attendance Reporting** | Lecturers / Admin can generate attendance reports. |
| **6. Administration** | Admin manages users, courses, and classes. |

---

## 📚 5. Sample data (in `/data/`)

| File | Sample entry |
|------|--------------|
| `users.txt` | `U001,Nguyen Van A,student01@gmail.com,123456,student` |
| `courses.txt` | `C001,Python Programming,3` |
| `classes.txt` | `CL001,CN1,2024A,C001,U002` |
| `sessions.txt` | `S001,CL001,2024-11-10,08:00,Week1,RoomA,Open` |
| `class_student.txt` | `CL001,U001` |
| `attendance.txt` | `A001,U001,S001,2024-11-10 08:01,Present` |
| `corrections.txt` | `CR001,A001,U001,U002,Pending,Was late due to traffic,` |

---

## 🧪 6. Testing

Run all tests:
```bash
pytest -v
```

Or run a single test module:
```bash
pytest tests/test_attendance.py -v
```

---

## 👥 7. Team responsibilities

| Member | Primary responsibility | Focus |
|--------|----------------------|-------|
| **Bảo** | Authentication + CLI routing | Registration, login, dashboard navigation |
| **Bình** | Academic domain | Handling Course, Class, Session data used by attendance features |
| **Tuấn** | Attendance Management | Check-in, Take Attendance, View Attendance History |
| **Kiệt** | Correction & Reporting | Request/Approve Correction, Generate Reports, basic Admin CRUD |

---

## 🧰 8. Development tools
- **IDE:** Visual Studio Code / PyCharm
- **Version control:** GitHub
- **Diagram tool:** Draw.io
- **Testing tool:** pytest
- **Optional:** Docker

---

## 🏁 9. Notes
- Data files are stored in the `data/` folder and should exist before running the app.
- You can add initialization code to create empty files if they are missing.
- To run via Docker or directly, the entry command is:
  ```bash
  python main.py
  ```
