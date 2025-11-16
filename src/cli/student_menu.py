from services.timetable_service import get_student_timetable, load_courses, load_classes, get_session_by_id
from services.attendance_service import student_checkin, get_student_history
from services.correction_service import CorrectionService
def handle_view_timetable(current_user):
    print("\n--- THOI KHOA BIEU CUA BAN ---")

    student_id = current_user.user_id

    # Load real data from timetable_service
    sessions = get_student_timetable(student_id)

    if not sessions:
        print("Ban khong co lich hoc nao.")
        print("-" * 80)
        input("\nNhan Enter de quay lai...")
        return

    # Load courses and classes to join with session data
    courses = load_courses()
    classes = load_classes()

    # Create lookup maps
    course_map = {c["id"]: c["name"] for c in courses}
    class_map = {cl["id"]: cl for cl in classes}

    # Build schedule data with course names
    schedule_data = []
    for sess in sessions:
        class_id = sess.get("class_id")
        class_info = class_map.get(class_id)

        if class_info:
            course_id = class_info.get("course_id")
            course_name = course_map.get(course_id, "Unknown")
        else:
            course_name = "Unknown"

        schedule_data.append({
            "date": sess.get("date_str", ""),
            "time": sess.get("time_str", ""),
            "course_name": course_name,
            "room": sess.get("room", ""),
            "week": sess.get("week", "")
        })

    # Sort by date
    schedule_data.sort(key=lambda x: x['date'])

    # Display timetable: Time – Course – Room – Week
    print(f"{'Thoi gian':<10} | {'Mon hoc':<25} | {'Phong':<12} | {'Tuan':<10}")
    print("-" * 80)

    for item in schedule_data:
        print(f"{item['time']:<10} | {item['course_name']:<25} | {item['room']:<12} | {item['week']:<10}")

    print("-" * 80)
    input("\nNhan Enter de quay lai...")

def handle_check_in(current_user):
    print("\n--- 2. DIEM DANH (Student Check-in) ---")

    # Ask the student which session they want to check into.
    # We try to show their timetable first so they can pick a session id.
    sessions = get_student_timetable(current_user.user_id)
    if not sessions:
        print("Bạn không có lịch học. Không thể điểm danh.")
        input("Nhấn Enter để quay lại...")
        return

    print("Danh sách buổi học của bạn:")
    for s in sessions:
        print(f"- {s.get('id', '')}: {s.get('date_str','')} {s.get('time_str','')} | Room: {s.get('room','')} | Status: {s.get('status','')}")

    session_id = input("Nhập mã buổi (ví dụ S001) để điểm danh, hoặc Enter để hủy: ").strip()
    if not session_id:
        print("Hủy điểm danh.")
        return

    ok, msg = student_checkin(current_user.user_id, session_id)
    if ok:
        print(f"[OK] {msg}")
    else:
        print(f"[ERROR] {msg}")
    input("Nhấn Enter để quay lại...")

def handle_view_history(current_user):
   
    print("\n" + "="*80)
    print("--- LICH SU DIEM DANH CUA BAN ---")
    print("="*80)

    student_id = current_user.user_id

    # Get attendance history
    records, stats = get_student_history(student_id)

    if not records:
        print("\nBan chua co lich su diem danh nao.")
        input("\nNhan Enter de quay lai...")
        return

    # Display statistics
    print(f"\nTHONG KE TONG QUAN:")
    print(f"- Tong so buoi hoc: {stats['total']}")
    print(f"- Co mat (Present): {stats['present']}")
    print(f"- Di muon (Late): {stats['late']}")
    print(f"- Vang mat (Absent): {stats['absent']}")
    print(f"- Ty le diem danh: {stats['attendance_pct']}%")

    print("\n" + "-"*80)
    print(f"{'Ma buoi':<12} | {'Thoi gian':<20} | {'Trang thai':<15} | {'Ghi chu':<20}")
    print("-"*80)

    # Display records
    for rec in records:
        time_str = rec.check_in_time.strftime("%Y-%m-%d %H:%M") if rec.check_in_time else "N/A"
        note_str = (rec.note[:17] + "...") if rec.note and len(rec.note) > 20 else (rec.note or "")
        print(f"{rec.session_id:<12} | {time_str:<20} | {rec.state.value:<15} | {note_str:<20}")

    print("-"*80)
    input("\nNhan Enter de quay lai...")


def handle_submit_correction(current_user):

    print("\n" + "="*80)
    print("--- GUI YEU CAU DIEU CHINH DIEM DANH ---")
    print("="*80)

    student_id = current_user.user_id

    # Show student's attendance records first
    records, _ = get_student_history(student_id)

    if not records:
        print("\nBan chua co lich su diem danh nao de dieu chinh.")
        input("\nNhan Enter de quay lai...")
        return

    # Display recent records
    print("\nCac buoi hoc gan day:")
    print(f"{'STT':<5} | {'Ma record':<12} | {'Ma buoi':<12} | {'Thoi gian':<20} | {'Trang thai':<12}")
    print("-"*75)

    for idx, rec in enumerate(records[-10:], 1):  # Show last 10 records
        time_str = rec.check_in_time.strftime("%Y-%m-%d %H:%M") if rec.check_in_time else "N/A"
        print(f"{idx:<5} | {rec.record_id:<12} | {rec.session_id:<12} | {time_str:<20} | {rec.state.value:<12}")

    print("-"*75)

    # Ask for record to correct
    record_id = input("\nNhap ma record can dieu chinh (hoac Enter de huy): ").strip()
    if not record_id:
        print("Huy thao tac.")
        input("\nNhan Enter de quay lai...")
        return

    # Verify record belongs to student
    record = next((r for r in records if r.record_id == record_id), None)
    if not record:
        print(f"[ERROR] Khong tim thay record {record_id} trong lich su cua ban.")
        input("\nNhan Enter de quay lai...")
        return

    # Get session info to find lecturer
    session = get_session_by_id(record.session_id)
    if not session:
        print("[ERROR] Khong tim thay thong tin buoi hoc.")
        input("\nNhan Enter de quay lai...")
        return

    # Get lecturer from session's class
    classes = load_classes()
    class_info = next((c for c in classes if c["id"] == session["class_id"]), None)
    lecturer_id = class_info["lecturer_id"] if class_info else "UNKNOWN"

    # Ask for reason
    print(f"\nBan dang yeu cau dieu chinh cho:")
    print(f"- Buoi hoc: {record.session_id}")
    print(f"- Trang thai hien tai: {record.state.value}")
    print(f"- Thoi gian: {record.check_in_time.strftime('%Y-%m-%d %H:%M') if record.check_in_time else 'N/A'}")

    reason = input("\nNhap ly do yeu cau dieu chinh: ").strip()
    if not reason:
        print("[ERROR] Ly do khong duoc de trong.")
        input("\nNhan Enter de quay lai...")
        return

    # Submit correction request
    correction_service = CorrectionService()
    if correction_service.request_correction(
        student_id=student_id,
        session_id=record.session_id,
        record_id=record_id,
        reason=reason,
        lecturer_id=lecturer_id
    ):
        print("\n[OK] Yeu cau dieu chinh da duoc gui thanh cong!")
        print("Giang vien se xem xet va phan hoi som.")
    else:
        print("\n[ERROR] Khong the gui yeu cau dieu chinh.")

    input("\nNhan Enter de quay lai...")

def student_menu(current_user):
    
    while True:
        print("\n" + "="*80)
        print(f"--- MENU SINH VIEN (Chao {current_user.username}) ---")
        print("="*80)
        print("(1) Xem thoi khoa bieu")
        print("(2) Thuc hien diem danh")
        print("(3) Xem lich su diem danh")
        print("(4) Gui yeu cau dieu chinh diem danh")
        print("(0) Dang xuat")
        print("="*80)

        choice = input("Vui long chon chuc nang: ").strip()

        if choice == '1':
            handle_view_timetable(current_user)
        elif choice == '2':
            handle_check_in(current_user)
        elif choice == '3':
            handle_view_history(current_user)
        elif choice == '4':
            handle_submit_correction(current_user)
        elif choice == '0':
            print("\n[OK] Dang xuat thanh cong.")
            break
        else:
            print("\n[ERROR] Lua chon khong hop le. Vui long chon lai.")