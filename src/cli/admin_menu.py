from services.admin_service import (
    list_users, add_user, delete_user,
    list_courses, add_course, delete_course,
    list_classes, add_class, delete_class,
    import_roster_from_file, get_system_statistics
)


def handle_manage_users():
    """Manage users (list, add, delete)."""
    while True:
        print("\n" + "="*80)
        print("--- QUAN LY NGUOI DUNG ---")
        print("="*80)
        print("(1) Xem danh sach nguoi dung")
        print("(2) Them nguoi dung moi")
        print("(3) Xoa nguoi dung")
        print("(0) Quay lai")
        print("="*80)

        choice = input("Lua chon: ").strip()

        if choice == "1":
            users = list_users()
            if not users:
                print("\nKhong co nguoi dung nao trong he thong.")
            else:
                print(f"\nTong so nguoi dung: {len(users)}\n")
                print(f"{'ID':<10} | {'Ten':<25} | {'Email':<30} | {'Vai tro':<10}")
                print("-" * 85)
                for u in users:
                    print(f"{u.id:<10} | {u.name:<25} | {u.email:<30} | {u.role:<10}")
                print("-" * 85)
            input("\nNhan Enter de tiep tuc...")

        elif choice == "2":
            print("\n--- THEM NGUOI DUNG MOI ---")
            name = input("Ten: ").strip()
            if not name:
                print("[ERROR] Ten khong duoc de trong.")
                continue

            email = input("Email: ").strip()
            if not email or "@" not in email:
                print("[ERROR] Email khong hop le.")
                continue

            password = input("Mat khau: ").strip()
            if not password:
                print("[ERROR] Mat khau khong duoc de trong.")
                continue

            print("Vai tro:")
            print("  1. student")
            print("  2. lecturer")
            print("  3. admin")
            role_choice = input("Chon: ").strip()

            role_map = {"1": "student", "2": "lecturer", "3": "admin"}
            role = role_map.get(role_choice)

            if not role:
                print("[ERROR] Lua chon khong hop le.")
                continue

            if add_user(name, email, password, role):
                print(f"[OK] Them nguoi dung thanh cong! (Role: {role})")
            else:
                print("[ERROR] Khong the them nguoi dung.")
            input("\nNhan Enter de tiep tuc...")

        elif choice == "3":
            print("\n--- XOA NGUOI DUNG ---")
            user_id = input("Nhap ID nguoi dung can xoa (hoac Enter de huy): ").strip()
            if not user_id:
                print("Huy thao tac.")
                continue

            confirm = input(f"Ban co chac chan muon xoa {user_id}? (y/n): ").strip().lower()
            if confirm == "y":
                if delete_user(user_id):
                    print(f"[OK] Da xoa nguoi dung {user_id}.")
                else:
                    print(f"[ERROR] Khong the xoa nguoi dung.")
            else:
                print("Huy thao tac.")
            input("\nNhan Enter de tiep tuc...")

        elif choice == "0":
            break
        else:
            print("[ERROR] Lua chon khong hop le.")


def handle_manage_courses():
    """Manage courses (list, add, delete)."""
    while True:
        print("\n" + "="*80)
        print("--- QUAN LY MON HOC ---")
        print("="*80)
        print("(1) Xem danh sach mon hoc")
        print("(2) Them mon hoc moi")
        print("(3) Xoa mon hoc")
        print("(0) Quay lai")
        print("="*80)

        choice = input("Lua chon: ").strip()

        if choice == "1":
            courses = list_courses()
            if not courses:
                print("\nKhong co mon hoc nao trong he thong.")
            else:
                print(f"\nTong so mon hoc: {len(courses)}\n")
                print(f"{'ID':<10} | {'Ten mon hoc':<40} | {'So tin chi':<10}")
                print("-" * 70)
                for c in courses:
                    print(f"{c['id']:<10} | {c['name']:<40} | {c['credits']:<10}")
                print("-" * 70)
            input("\nNhan Enter de tiep tuc...")

        elif choice == "2":
            print("\n--- THEM MON HOC MOI ---")
            name = input("Ten mon hoc: ").strip()
            if not name:
                print("[ERROR] Ten mon hoc khong duoc de trong.")
                continue

            credits = input("So tin chi: ").strip()
            if not credits:
                print("[ERROR] So tin chi khong duoc de trong.")
                continue

            if add_course(name, credits):
                print(f"[OK] Them mon hoc thanh cong!")
            else:
                print("[ERROR] Khong the them mon hoc.")
            input("\nNhan Enter de tiep tuc...")

        elif choice == "3":
            print("\n--- XOA MON HOC ---")
            course_id = input("Nhap ID mon hoc can xoa (hoac Enter de huy): ").strip()
            if not course_id:
                print("Huy thao tac.")
                continue

            confirm = input(f"Ban co chac chan muon xoa {course_id}? (y/n): ").strip().lower()
            if confirm == "y":
                if delete_course(course_id):
                    print(f"[OK] Da xoa mon hoc {course_id}.")
                else:
                    print(f"[ERROR] Khong the xoa mon hoc.")
            else:
                print("Huy thao tac.")
            input("\nNhan Enter de tiep tuc...")

        elif choice == "0":
            break
        else:
            print("[ERROR] Lua chon khong hop le.")


def handle_manage_classes():
    """Manage classes (list, add, delete)."""
    while True:
        print("\n" + "="*80)
        print("--- QUAN LY LOP HOC ---")
        print("="*80)
        print("(1) Xem danh sach lop hoc")
        print("(2) Them lop hoc moi")
        print("(3) Xoa lop hoc")
        print("(0) Quay lai")
        print("="*80)

        choice = input("Lua chon: ").strip()

        if choice == "1":
            classes = list_classes()
            if not classes:
                print("\nKhong co lop hoc nao trong he thong.")
            else:
                print(f"\nTong so lop hoc: {len(classes)}\n")
                print(f"{'ID':<10} | {'Ten lop':<15} | {'Hoc ky':<10} | {'Ma mon':<10} | {'Ma GV':<10}")
                print("-" * 70)
                for c in classes:
                    print(f"{c['id']:<10} | {c['name']:<15} | {c['semester']:<10} | {c['course_id']:<10} | {c['lecturer_id']:<10}")
                print("-" * 70)
            input("\nNhan Enter de tiep tuc...")

        elif choice == "2":
            print("\n--- THEM LOP HOC MOI ---")
            name = input("Ten lop: ").strip()
            if not name:
                print("[ERROR] Ten lop khong duoc de trong.")
                continue

            semester = input("Hoc ky (VD: 2024A): ").strip()
            if not semester:
                print("[ERROR] Hoc ky khong duoc de trong.")
                continue

            course_id = input("Ma mon hoc (VD: C001): ").strip()
            if not course_id:
                print("[ERROR] Ma mon hoc khong duoc de trong.")
                continue

            lecturer_id = input("Ma giang vien (VD: U002): ").strip()
            if not lecturer_id:
                print("[ERROR] Ma giang vien khong duoc de trong.")
                continue

            if add_class(name, semester, course_id, lecturer_id):
                print(f"[OK] Them lop hoc thanh cong!")
            else:
                print("[ERROR] Khong the them lop hoc.")
            input("\nNhan Enter de tiep tuc...")

        elif choice == "3":
            print("\n--- XOA LOP HOC ---")
            class_id = input("Nhap ID lop hoc can xoa (hoac Enter de huy): ").strip()
            if not class_id:
                print("Huy thao tac.")
                continue

            confirm = input(f"Ban co chac chan muon xoa {class_id}? (y/n): ").strip().lower()
            if confirm == "y":
                if delete_class(class_id):
                    print(f"[OK] Da xoa lop hoc {class_id}.")
                else:
                    print(f"[ERROR] Khong the xoa lop hoc.")
            else:
                print("Huy thao tac.")
            input("\nNhan Enter de tiep tuc...")

        elif choice == "0":
            break
        else:
            print("[ERROR] Lua chon khong hop le.")


def handle_import_roster():
    """Import student roster from CSV file."""
    print("\n" + "="*80)
    print("--- IMPORT DANH SACH SINH VIEN ---")
    print("="*80)
    print("\nDinh dang file: class_id,student_id")
    print("Vi du: CL001,U001")
    print("-" * 80)

    file_path = input("\nNhap duong dan file CSV (hoac Enter de huy): ").strip()
    if not file_path:
        print("Huy thao tac.")
        input("\nNhan Enter de tiep tuc...")
        return

    if import_roster_from_file(file_path):
        print("\n[OK] Import thanh cong!")
    else:
        print("\n[ERROR] Import that bai.")

    input("\nNhan Enter de tiep tuc...")


def handle_view_system_reports():
    """View system statistics."""
    print("\n" + "="*80)
    print("--- BAO CAO HE THONG ---")
    print("="*80)

    stats = get_system_statistics()

    print(f"\nTONG QUAN HE THONG:")
    print("-" * 50)
    print(f"Tong so nguoi dung:    {stats['total_users']}")
    print(f"  - Sinh vien:         {stats['students']}")
    print(f"  - Giang vien:        {stats['lecturers']}")
    print(f"  - Quan tri vien:     {stats['admins']}")
    print(f"\nTong so mon hoc:       {stats['total_courses']}")
    print(f"Tong so lop hoc:       {stats['total_classes']}")
    print("-" * 50)

    input("\nNhan Enter de quay lai...")


def admin_menu(current_user):
    """Main menu for admin users."""
    while True:
        print("\n" + "="*80)
        print(f"--- MENU QUAN TRI VIEN (Chao {current_user.name}) ---")
        print("="*80)
        print("(1) Quan ly nguoi dung")
        print("(2) Quan ly mon hoc")
        print("(3) Quan ly lop hoc")
        print("(4) Import danh sach sinh vien")
        print("(5) Xem bao cao he thong")
        print("(0) Dang xuat")
        print("="*80)

        choice = input("Vui long chon chuc nang: ").strip()

        if choice == '1':
            handle_manage_users()
        elif choice == '2':
            handle_manage_courses()
        elif choice == '3':
            handle_manage_classes()
        elif choice == '4':
            handle_import_roster()
        elif choice == '5':
            handle_view_system_reports()
        elif choice == '0':
            print("\n[OK] Dang xuat thanh cong.")
            break
        else:
            print("\n[ERROR] Lua chon khong hop le. Vui long chon lai.")