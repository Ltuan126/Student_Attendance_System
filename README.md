 # 🧾 Student Attendance System (CLI Version)

## 📌 1. Giới thiệu
Hệ thống **Student Attendance System (SAS)** được phát triển để hỗ trợ việc **điểm danh và quản lý điểm danh** cho sinh viên và giảng viên.  
Chương trình chạy bằng **Command Line Interface (CLI)**, lưu trữ dữ liệu bằng file `.txt`, không cần cơ sở dữ liệu.

---

## ⚙️ 2. Cấu trúc thư mục

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

## 👨‍💻 3. Cách chạy chương trình

### 🔧 Yêu cầu môi trường
- Python **>= 3.11**
- Đã cài **pytest** (nếu muốn chạy test)
- Hệ điều hành: Windows / macOS / Linux

### 🚀 Chạy chương trình chính

Mở terminal trong thư mục dự án và chạy:
```bash
python main.py
```

Sau khi khởi động, hệ thống sẽ hiển thị:
```
===========================
Student Attendance System – CLI Version
===========================
(1) Login
(2) Register
(0) Exit
```

- Nếu đăng nhập là **Student**, vào menu:
  ```
  (1) View Timetable
  (2) Check-in Attendance
  (3) View Attendance History
  (4) Request Attendance Correction
  (0) Logout
  ```
- Nếu đăng nhập là **Lecturer**, vào menu:
  ```
  (1) View Teaching Schedule
  (2) Take Attendance
  (3) Review Correction Requests
  (4) Generate Attendance Report
  (0) Logout
  ```
- Nếu đăng nhập là **Admin**, vào menu:
  ```
  (1) Manage Users
  (2) Manage Courses
  (3) Manage Classes
  (4) Import Roster
  (5) View System Reports
  (0) Logout
  ```

---

## 🧩 4. Các chức năng chính

| Nhóm chức năng | Mô tả |
|----------------|-------|
| **1. Authentication** | Đăng ký và đăng nhập người dùng (Student, Lecturer, Admin). |
| **2. Timetable Management** | Sinh viên xem thời khóa biểu, dữ liệu lấy từ `sessions.txt`. |
| **3. Attendance Management** | Sinh viên tự điểm danh, giảng viên điểm danh lớp, xem lịch sử. |
| **4. Correction Handling** | Sinh viên gửi yêu cầu sửa điểm danh; giảng viên duyệt. |
| **5. Attendance Reporting** | Giảng viên / Admin tạo báo cáo điểm danh. |
| **6. Administration** | Admin quản lý Users, Courses, Classes. |

---

## 📚 5. Dữ liệu mẫu (trong thư mục `/data/`)

| File | Dữ liệu mẫu |
|------|--------------|
| `users.txt` | `U001,Nguyen Van A,student01@gmail.com,123456,student` |
| `courses.txt` | `C001,Python Programming,3` |
| `classes.txt` | `CL001,CN1,2024A,C001,U002` |
| `sessions.txt` | `S001,CL001,2024-11-10,08:00,Week1,RoomA,Open` |
| `class_student.txt` | `CL001,U001` |
| `attendance.txt` | `A001,U001,S001,2024-11-10 08:01,Present` |
| `corrections.txt` | `CR001,A001,U001,U002,Pending,Was late due to traffic,` |

---

## 🧪 6. Kiểm thử

Chạy tất cả các test:
```bash
pytest -v
```

Hoặc chạy riêng 1 module:
```bash
pytest tests/test_attendance.py -v
```


---

## 👥 7. Phân công nhóm

| Thành viên | Phụ trách chính | Trọng tâm |
|-------------|-----------------|------------|
| **Bảo** | Authentication + CLI routing | Đăng ký, đăng nhập, điều hướng dashboard |
| **Bình** | Academic domain | Xử lý Course, Class, Session, cung cấp dữ liệu cho điểm danh |
| **Tuấn** | Attendance Management | Check-in Attendance, Take Attendance, View Attendance History |
| **Kiệt** | Correction & Reporting | Request/Approve Correction, Generate Report, Admin CRUD cơ bản |

---

## 🧰 8. Công cụ phát triển
- **IDE:** Visual Studio Code / PyCharm  
- **Version control:** GitHub  
- **Diagram tool:** Draw.io  
- **Testing tool:** pytest + Excel test cases  
- **Optional:** Docker

---

## 🏁 9. Ghi chú
- Dữ liệu nằm trong thư mục `data/`, phải tồn tại trước khi chạy.  
- Có thể thêm code khởi tạo file trống nếu chưa có dữ liệu.  
- Nếu dùng Docker, lệnh mặc định:
  ```bash
  python main.py
  ```
