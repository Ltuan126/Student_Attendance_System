# cli/main.py
from services.auth_service import register_user, login_user

def student_menu():
    print("🎓 Student Dashboard")
    input("Nhấn Enter để quay lại menu chính...")

def lecturer_menu():
    print("Lecturer Dashboard")
    input("Nhấn Enter để quay lại menu chính...")

def admin_menu():
    print("🛠️ Admin Dashboard")
    input("Nhấn Enter để quay lại menu chính...")

def main():
    while True:
        print("="*35)
        print("Hệ THỐNG ĐIỂM DANH - LOGIN INTERFACE")
        print("="*35)
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        choice = input("👉 Chọn: ").strip()

        if choice == "1":
            user = login_user()
            if user:
                if user.role == "student":
                    student_menu()
                elif user.role == "lecturer":
                    lecturer_menu()
                elif user.role == "admin":
                    admin_menu()
        elif choice == "2":
            register_user()
        elif choice == "0":
            print("Tạm biệt ")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")

if __name__ == "__main__":
    main()

