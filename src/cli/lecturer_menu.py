from services.timetable_service import load_sessions, load_classes, load_courses, get_students_in_session
from services.attendance_service import lecturer_take_attendance, get_student_history
from services.correction_service import CorrectionService


def handle_view_teaching_schedule(current_user):
    print("\n" + "="*80)
    print("--- LICH GIANG DAY CUA BAN ---")
    print("="*80)

    lecturer_id = current_user.user_id

    # Load all classes taught by this lecturer
    all_classes = load_classes()
    lecturer_classes = [c for c in all_classes if c.get("lecturer_id") == lecturer_id]

    if not lecturer_classes:
        print("Ban khong co lop hoc nao duoc phan cong.")
        input("\nNhan Enter de quay lai...")
        return

    # Load all sessions for these classes
    all_sessions = load_sessions()
    courses = load_courses()

    # Create course lookup map
    course_map = {c["id"]: c["name"] for c in courses}
    class_ids = [c["id"] for c in lecturer_classes]

    lecturer_sessions = [s for s in all_sessions if s.get("class_id") in class_ids]

    if not lecturer_sessions:
        print("Khong co buoi hoc nao trong lich.")
        input("\nNhan Enter de quay lai...")
        return

    # Build schedule data
    schedule_data = []
    for sess in lecturer_sessions:
        class_id = sess.get("class_id")
        class_info = next((c for c in lecturer_classes if c["id"] == class_id), None)

        if class_info:
            course_id = class_info.get("course_id")
            course_name = course_map.get(course_id, "Unknown")
            class_name = class_info.get("name", "")
        else:
            course_name = "Unknown"
            class_name = ""

        schedule_data.append({
            "session_id": sess.get("id", ""),
            "date": sess.get("date_str", ""),
            "time": sess.get("time_str", ""),
            "course_name": course_name,
            "class_name": class_name,
            "room": sess.get("room", ""),
            "week": sess.get("week", ""),
            "status": sess.get("status", "")
        })

    # Sort by date
    schedule_data.sort(key=lambda x: x['date'])

    # Display schedule
    print(f"{'Ma buoi':<10} | {'Ngay':<12} | {'Gio':<8} | {'Mon hoc':<25} | {'Lop':<10} | {'Phong':<10} | {'Status':<10}")
    print("-" * 110)

    for item in schedule_data:
        print(f"{item['session_id']:<10} | {item['date']:<12} | {item['time']:<8} | {item['course_name']:<25} | {item['class_name']:<10} | {item['room']:<10} | {item['status']:<10}")

    print("-" * 110)
    input("\nNhan Enter de quay lai...")


def handle_take_attendance(current_user):
    """Take attendance for a session."""
    print("\n" + "="*80)
    print("--- DIEM DANH CHO BUOI HOC ---")
    print("="*80)

    lecturer_id = current_user.user_id

    # Show lecturer's upcoming/open sessions
    all_classes = load_classes()
    lecturer_classes = [c for c in all_classes if c.get("lecturer_id") == lecturer_id]

    if not lecturer_classes:
        print("Ban khong co lop hoc nao duoc phan cong.")
        input("\nNhan Enter de quay lai...")
        return

    all_sessions = load_sessions()
    class_ids = [c["id"] for c in lecturer_classes]
    lecturer_sessions = [s for s in all_sessions if s.get("class_id") in class_ids]

    if not lecturer_sessions:
        print("Khong co buoi hoc nao trong lich.")
        input("\nNhan Enter de quay lai...")
        return

    # Display available sessions
    print("\nDanh sach cac buoi hoc cua ban:")
    print(f"{'Ma buoi':<10} | {'Ngay':<12} | {'Gio':<8} | {'Phong':<10} | {'Status':<10}")
    print("-" * 60)

    for sess in lecturer_sessions:
        print(f"{sess.get('id', ''):<10} | {sess.get('date_str', ''):<12} | {sess.get('time_str', ''):<8} | {sess.get('room', ''):<10} | {sess.get('status', ''):<10}")

    print("-" * 60)

    # Ask for session ID
    session_id = input("\nNhap ma buoi hoc de diem danh (hoac Enter de huy): ").strip()
    if not session_id:
        print("Huy diem danh.")
        input("Nhan Enter de quay lai...")
        return

    # Verify this session belongs to the lecturer
    if session_id not in [s.get("id") for s in lecturer_sessions]:
        print(f"[ERROR] Buoi hoc {session_id} khong thuoc ve ban.")
        input("Nhan Enter de quay lai...")
        return

    # Call the attendance service
    print(f"\n--- Diem danh cho buoi {session_id} ---\n")
    lecturer_take_attendance(session_id)

    print("\n[OK] Hoan thanh diem danh!")
    input("Nhan Enter de quay lai...")


def handle_review_corrections(current_user):
    """Review and approve/reject correction requests."""
    print("\n" + "="*80)
    print("--- DUYET YEU CAU DIEU CHINH DIEM DANH ---")
    print("="*80)

    lecturer_id = current_user.user_id
    correction_service = CorrectionService()

    # Get pending requests for this lecturer
    pending_requests = correction_service.list_pending_requests(lecturer_id)

    if not pending_requests:
        print("\nKhong co yeu cau nao dang cho duyet.")
        input("\nNhan Enter de quay lai...")
        return

    # Display pending requests
    print(f"\nCo {len(pending_requests)} yeu cau dang cho duyet:\n")
    print(f"{'Ma YC':<10} | {'SV ID':<10} | {'Buoi':<10} | {'Ly do':<40}")
    print("-" * 80)

    for req in pending_requests:
        reason_short = req.reason[:37] + "..." if len(req.reason) > 40 else req.reason
        print(f"{req.request_id:<10} | {req.student_id:<10} | {req.session_id:<10} | {reason_short:<40}")

    print("-" * 80)

    # Ask which request to process
    request_id = input("\nNhap ma yeu cau de xu ly (hoac Enter de huy): ").strip()
    if not request_id:
        print("Huy xu ly.")
        input("Nhan Enter de quay lai...")
        return

    # Find the request
    request = next((r for r in pending_requests if r.request_id == request_id), None)
    if not request:
        print(f"[ERROR] Khong tim thay yeu cau {request_id}.")
        input("Nhan Enter de quay lai...")
        return

    # Show details
    print(f"\n--- Chi tiet yeu cau {request_id} ---")
    print(f"Sinh vien: {request.student_id}")
    print(f"Buoi hoc: {request.session_id}")
    print(f"Record ID: {request.record_id}")
    print(f"Ly do: {request.reason}")
    print(f"Thoi gian: {request.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    # Ask for decision
    print("\n(1) Duyet")
    print("(2) Tu choi")
    print("(0) Huy")

    choice = input("Lua chon cua ban: ").strip()

    if choice == "1":
        note = input("Ghi chu (optional): ").strip()
        if correction_service.approve_request(request_id, note):
            print("\n[OK] Da duyet yeu cau thanh cong!")
        else:
            print("\n[ERROR] Khong the duyet yeu cau.")
    elif choice == "2":
        note = input("Ghi chu (optional): ").strip()
        if correction_service.reject_request(request_id, note):
            print("\n[OK] Da tu choi yeu cau.")
        else:
            print("\n[ERROR] Khong the tu choi yeu cau.")
    else:
        print("Huy xu ly.")

    input("\nNhan Enter de quay lai...")


def handle_generate_report(current_user):
    """Generate attendance report for a class."""
    print("\n" + "="*80)
    print("--- TAO BAO CAO DIEM DANH ---")
    print("="*80)

    lecturer_id = current_user.user_id

    # Show lecturer's classes
    all_classes = load_classes()
    lecturer_classes = [c for c in all_classes if c.get("lecturer_id") == lecturer_id]

    if not lecturer_classes:
        print("Ban khong co lop hoc nao duoc phan cong.")
        input("\nNhan Enter de quay lai...")
        return

    courses = load_courses()
    course_map = {c["id"]: c["name"] for c in courses}

    # Display classes
    print("\nDanh sach lop hoc cua ban:")
    print(f"{'Ma lop':<10} | {'Ten lop':<15} | {'Mon hoc':<30}")
    print("-" * 65)

    for cls in lecturer_classes:
        course_name = course_map.get(cls.get("course_id"), "Unknown")
        print(f"{cls.get('id', ''):<10} | {cls.get('name', ''):<15} | {course_name:<30}")

    print("-" * 65)

    # Ask for class ID
    class_id = input("\nNhap ma lop de tao bao cao (hoac Enter de huy): ").strip()
    if not class_id:
        print("Huy tao bao cao.")
        input("Nhan Enter de quay lai...")
        return

    # Verify class belongs to lecturer
    if class_id not in [c.get("id") for c in lecturer_classes]:
        print(f"[ERROR] Lop {class_id} khong thuoc ve ban.")
        input("Nhan Enter de quay lai...")
        return

    # Get all students in this class and their attendance
    print(f"\n--- BAO CAO DIEM DANH LOP {class_id} ---\n")

    students = get_students_in_session_by_class(class_id)

    if not students:
        print("Khong co sinh vien nao trong lop.")
        input("\nNhan Enter de quay lai...")
        return

    # Generate report for each student
    print(f"{'SV ID':<10} | {'Ten':<25} | {'Tong':<6} | {'P':<5} | {'L':<5} | {'A':<5} | {'Ty le %':<8}")
    print("-" * 85)

    for student_id, student_name in students:
        records, stats = get_student_history(student_id)
        # Filter to only this class's sessions
        # (Simplified: showing all attendance for now)
        print(f"{student_id:<10} | {student_name:<25} | {stats['total']:<6} | {stats['present']:<5} | {stats['late']:<5} | {stats['absent']:<5} | {stats['attendance_pct']:<8.2f}")

    print("-" * 85)
    print("\n[OK] Bao cao hoan tat!")
    input("\nNhan Enter de quay lai...")


def get_students_in_session_by_class(class_id):
    """Helper to get all students in a class (not session-specific)."""
    import os
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    cs_path = os.path.join(data_dir, "class_student.txt")
    users_path = os.path.join(data_dir, "users.txt")

    student_ids = []
    try:
        with open(cs_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if parts[0] == class_id and len(parts) > 1:
                    student_ids.append(parts[1])
    except FileNotFoundError:
        return []

    # Build id->name map
    id_name = {}
    try:
        with open(users_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 2:
                    id_name[parts[0]] = parts[1]
    except FileNotFoundError:
        pass

    return [(sid, id_name.get(sid, "")) for sid in student_ids]


def lecturer_menu(current_user):
    """Main menu for lecturer users."""
    while True:
        print("\n" + "="*80)
        print(f"--- MENU GIANG VIEN (Chao {current_user.name}) ---")
        print("="*80)
        print("(1) Xem lich giang day")
        print("(2) Diem danh cho buoi hoc")
        print("(3) Duyet yeu cau dieu chinh diem danh")
        print("(4) Tao bao cao diem danh")
        print("(0) Dang xuat")
        print("="*80)

        choice = input("Vui long chon chuc nang: ").strip()

        if choice == '1':
            handle_view_teaching_schedule(current_user)
        elif choice == '2':
            handle_take_attendance(current_user)
        elif choice == '3':
            handle_review_corrections(current_user)
        elif choice == '4':
            handle_generate_report(current_user)
        elif choice == '0':
            print("\n[OK] Dang xuat thanh cong.")
            break
        else:
            print("\n[ERROR] Lua chon khong hop le. Vui long chon lai.")
