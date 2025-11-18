from models.user import User, Student, Lecturer, Admin
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.txt")


def load_users():
    users = []
    if not os.path.exists(USERS_FILE):
        return users

    with open(USERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            user_id, name, email, password, role = line.split(",")
            if role == "student":
                users.append(Student(user_id, name, email, password))
            elif role == "lecturer":
                users.append(Lecturer(user_id, name, email, password))
            elif role == "admin":
                users.append(Admin(user_id, name, email, password))
            else:
                users.append(User(user_id, name, email, password, role))
    return users


def save_users(users):
    with open(USERS_FILE, "w") as f:
        for u in users:
            f.write(f"{u.id},{u.name},{u.email},{u.password},{u.role}\n")


def register_user():
    users = load_users()
    email = input("Nhập email: ").strip()

    # Kiểm tra trùng email
    for u in users:
        if u.email == email:
            print("Email đã tồn tại. Vui lòng thử lại.")
            return

    # Kiểm tra định dạng email đơn giản
    if "@" not in email or "." not in email:
        print("Email sai định dạng.")
        return

    name = input("Nhập tên: ").strip()
    password = input("Nhập mật khẩu: ").strip()

    print("Chọn vai trò:")
    print("1. Student")
    print("2. Lecturer")
    print("3. Admin")
    role_choice = input("Nhập số: ").strip()

    # Generate new user ID (same logic as admin_service.py)
    max_id = 0
    for u in users:
        if u.id.startswith("U") and u.id[1:].isdigit():
            num = int(u.id[1:])
            if num > max_id:
                max_id = num
    new_id = f"U{max_id + 1:03d}"

    if role_choice == "1":
        role = "student"
        new_user = Student(new_id, name, email, password)
    elif role_choice == "2":
        role = "lecturer"
        new_user = Lecturer(new_id, name, email, password)
    elif role_choice == "3":
        role = "admin"
        new_user = Admin(new_id, name, email, password)
    else:
        print("Lựa chọn không hợp lệ .")
        return

    users.append(new_user)
    save_users(users)
    print(f"Đăng ký thành công! ({role})")


def login_user():
    users = load_users()
    email = input("Email: ").strip()
    password = input("Mật khẩu: ").strip()

    for u in users:
        if u.email == email and u.password == password:
            print(f"Đăng nhập thành công! Xin chào {u.name}.")
            return u
    print("Sai email hoặc mật khẩu .")
    return None
