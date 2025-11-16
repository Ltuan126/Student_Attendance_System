
from services.auth_service import register_user, login_user
from cli.student_menu import student_menu
from cli.lecturer_menu import lecturer_menu
from cli.admin_menu import admin_menu

def main_menu():
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
                    student_menu(user)
                elif user.role == "lecturer":
                    lecturer_menu(user)
                elif user.role == "admin":
                    admin_menu(user)
        elif choice == "2":
            register_user()
        elif choice == "0":
            print("Tạm biệt ")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")

if __name__ == "__main__":
    main_menu()
