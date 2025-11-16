import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

from models.attendance import AttendanceRecord, AttendanceState
from services.timetable_service import load_sessions, load_classes, load_courses



def _data_path(filename: str) -> str:
    """Get absolute path to data file."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return os.path.join(root, filename)


def _load_all_attendance_records() -> List[AttendanceRecord]:
    """Load all attendance records from attendance.txt."""
    records = []
    path = _data_path("attendance.txt")

    if not os.path.exists(path):
        return records

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = AttendanceRecord.from_line(line)
                records.append(record)
            except Exception:
                continue

    return records


def _get_students_in_class(class_id: str) -> List[tuple]:
    """Get all students enrolled in a class.

    Returns: list of (student_id, student_name) tuples
    """
    cs_path = _data_path("class_student.txt")
    users_path = _data_path("users.txt")

    student_ids = []
    try:
        with open(cs_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) >= 2 and parts[0].strip() == class_id:
                    student_ids.append(parts[1].strip())
    except FileNotFoundError:
        return []

    # Build id->name map
    id_name = {}
    try:
        with open(users_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) >= 2:
                    id_name[parts[0].strip()] = parts[1].strip()
    except FileNotFoundError:
        pass

    return [(sid, id_name.get(sid, "Unknown")) for sid in student_ids]


def generate_report_by_class(class_id: str) -> Dict:
    """Generate attendance report for a specific class.

    Returns a dict with:
    - class_info: dict with class details
    - sessions: list of session dicts for this class
    - student_stats: list of dicts with student attendance statistics
    - summary: overall class statistics
    """
    # Load class info
    classes = load_classes()
    class_info = next((c for c in classes if c["id"] == class_id), None)

    if not class_info:
        return {
            "error": f"Class {class_id} not found",
            "class_info": None,
            "sessions": [],
            "student_stats": [],
            "summary": {}
        }

    # Load course info
    courses = load_courses()
    course = next((c for c in courses if c["id"] == class_info["course_id"]), None)
    course_name = course["name"] if course else "Unknown"

    # Get all sessions for this class
    all_sessions = load_sessions()
    class_sessions = [s for s in all_sessions if s["class_id"] == class_id]

    # Get all students in this class
    students = _get_students_in_class(class_id)

    # Load all attendance records
    all_records = _load_all_attendance_records()

    # Get session IDs for this class
    session_ids = [s["id"] for s in class_sessions]

    # Filter attendance records for this class's sessions
    class_records = [r for r in all_records if r.session_id in session_ids]

    # Build student statistics
    student_stats = []

    for student_id, student_name in students:
        # Get this student's records for this class
        student_records = [r for r in class_records if r.student_id == student_id]

        total_sessions = len(class_sessions)
        attended_sessions = len(student_records)

        present_count = sum(1 for r in student_records if r.state == AttendanceState.PRESENT)
        late_count = sum(1 for r in student_records if r.state == AttendanceState.LATE)
        absent_count = total_sessions - attended_sessions + sum(1 for r in student_records if r.state == AttendanceState.ABSENT)

        # Calculate attendance percentage
        attendance_pct = 0.0
        if total_sessions > 0:
            attendance_pct = ((present_count + late_count) / total_sessions) * 100

        student_stats.append({
            "student_id": student_id,
            "student_name": student_name,
            "total_sessions": total_sessions,
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
            "attendance_pct": round(attendance_pct, 2)
        })

    # Calculate overall summary
    total_students = len(students)
    avg_attendance = 0.0
    if total_students > 0:
        avg_attendance = sum(s["attendance_pct"] for s in student_stats) / total_students

    summary = {
        "total_students": total_students,
        "total_sessions": len(class_sessions),
        "average_attendance_pct": round(avg_attendance, 2)
    }

    return {
        "error": None,
        "class_info": {
            "id": class_id,
            "name": class_info["name"],
            "semester": class_info["semester"],
            "course_name": course_name,
            "lecturer_id": class_info["lecturer_id"]
        },
        "sessions": class_sessions,
        "student_stats": student_stats,
        "summary": summary
    }


def generate_report_by_student(student_id: str) -> Dict:
    """Generate attendance report for a specific student across all classes.

    Returns a dict with:
    - student_info: dict with student details
    - class_stats: list of dicts with attendance per class
    - overall_summary: overall statistics across all classes
    """
    # Load student info
    users_path = _data_path("users.txt")
    student_name = "Unknown"

    try:
        with open(users_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[0].strip() == student_id:
                    student_name = parts[1].strip()
                    break
    except FileNotFoundError:
        pass

    # Find all classes this student is enrolled in
    cs_path = _data_path("class_student.txt")
    student_classes = []

    try:
        with open(cs_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[1].strip() == student_id:
                    student_classes.append(parts[0].strip())
    except FileNotFoundError:
        pass

    # Load all attendance records for this student
    all_records = _load_all_attendance_records()
    student_records = [r for r in all_records if r.student_id == student_id]

    # Load class and course info
    classes = load_classes()
    courses = load_courses()
    all_sessions = load_sessions()

    course_map = {c["id"]: c["name"] for c in courses}

    # Build stats per class
    class_stats = []

    for class_id in student_classes:
        class_info = next((c for c in classes if c["id"] == class_id), None)
        if not class_info:
            continue

        # Get sessions for this class
        class_sessions = [s for s in all_sessions if s["class_id"] == class_id]
        session_ids = [s["id"] for s in class_sessions]

        # Get records for this class
        class_records = [r for r in student_records if r.session_id in session_ids]

        total_sessions = len(class_sessions)
        present_count = sum(1 for r in class_records if r.state == AttendanceState.PRESENT)
        late_count = sum(1 for r in class_records if r.state == AttendanceState.LATE)
        absent_count = total_sessions - len(class_records) + sum(1 for r in class_records if r.state == AttendanceState.ABSENT)

        attendance_pct = 0.0
        if total_sessions > 0:
            attendance_pct = ((present_count + late_count) / total_sessions) * 100

        course_name = course_map.get(class_info["course_id"], "Unknown")

        class_stats.append({
            "class_id": class_id,
            "class_name": class_info["name"],
            "course_name": course_name,
            "semester": class_info["semester"],
            "total_sessions": total_sessions,
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
            "attendance_pct": round(attendance_pct, 2)
        })

    # Calculate overall summary
    total_classes = len(class_stats)
    total_sessions_all = sum(c["total_sessions"] for c in class_stats)
    total_present = sum(c["present"] for c in class_stats)
    total_late = sum(c["late"] for c in class_stats)
    total_absent = sum(c["absent"] for c in class_stats)

    overall_pct = 0.0
    if total_sessions_all > 0:
        overall_pct = ((total_present + total_late) / total_sessions_all) * 100

    overall_summary = {
        "total_classes": total_classes,
        "total_sessions": total_sessions_all,
        "total_present": total_present,
        "total_late": total_late,
        "total_absent": total_absent,
        "overall_attendance_pct": round(overall_pct, 2)
    }

    return {
        "student_info": {
            "id": student_id,
            "name": student_name
        },
        "class_stats": class_stats,
        "overall_summary": overall_summary
    }


def export_report_to_file(report_data: Dict, output_path: str, report_type: str = "class") -> bool:
    """Export report data to a text file.

    Args:
        report_data: Report dict from generate_report_by_class or generate_report_by_student
        output_path: Path to output file
        report_type: "class" or "student"

    Returns:
        True if export successful, False otherwise
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("="*80 + "\n")
            f.write("BAO CAO DIEM DANH\n")
            f.write("="*80 + "\n")
            f.write(f"Ngay tao: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")

            if report_type == "class":
                if report_data.get("error"):
                    f.write(f"[ERROR] {report_data['error']}\n")
                    return False

                class_info = report_data["class_info"]
                f.write(f"LOP: {class_info['name']} ({class_info['id']})\n")
                f.write(f"Mon hoc: {class_info['course_name']}\n")
                f.write(f"Hoc ky: {class_info['semester']}\n")
                f.write(f"Giang vien: {class_info['lecturer_id']}\n\n")

                summary = report_data["summary"]
                f.write(f"TONG QUAN:\n")
                f.write(f"- Tong so sinh vien: {summary['total_students']}\n")
                f.write(f"- Tong so buoi hoc: {summary['total_sessions']}\n")
                f.write(f"- Ty le diem danh trung binh: {summary['average_attendance_pct']:.2f}%\n\n")

                f.write("-"*80 + "\n")
                f.write(f"{'Ma SV':<10} | {'Ten SV':<25} | {'Tong':<6} | {'P':<5} | {'L':<5} | {'A':<5} | {'%':<8}\n")
                f.write("-"*80 + "\n")

                for stat in report_data["student_stats"]:
                    f.write(f"{stat['student_id']:<10} | {stat['student_name']:<25} | {stat['total_sessions']:<6} | "
                           f"{stat['present']:<5} | {stat['late']:<5} | {stat['absent']:<5} | {stat['attendance_pct']:<8.2f}\n")

                f.write("-"*80 + "\n")

            elif report_type == "student":
                student_info = report_data["student_info"]
                f.write(f"SINH VIEN: {student_info['name']} ({student_info['id']})\n\n")

                summary = report_data["overall_summary"]
                f.write(f"TONG QUAN:\n")
                f.write(f"- Tong so lop: {summary['total_classes']}\n")
                f.write(f"- Tong so buoi hoc: {summary['total_sessions']}\n")
                f.write(f"- Tong Present: {summary['total_present']}\n")
                f.write(f"- Tong Late: {summary['total_late']}\n")
                f.write(f"- Tong Absent: {summary['total_absent']}\n")
                f.write(f"- Ty le diem danh: {summary['overall_attendance_pct']:.2f}%\n\n")

                f.write("-"*80 + "\n")
                f.write(f"{'Ma lop':<10} | {'Mon hoc':<30} | {'Tong':<6} | {'P':<5} | {'L':<5} | {'A':<5} | {'%':<8}\n")
                f.write("-"*80 + "\n")

                for stat in report_data["class_stats"]:
                    f.write(f"{stat['class_id']:<10} | {stat['course_name']:<30} | {stat['total_sessions']:<6} | "
                           f"{stat['present']:<5} | {stat['late']:<5} | {stat['absent']:<5} | {stat['attendance_pct']:<8.2f}\n")

                f.write("-"*80 + "\n")

            f.write(f"\n--- End of Report ---\n")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to export report: {e}")
        return False


def print_class_report(class_id: str) -> None:
    """Print formatted class attendance report to console."""
    report = generate_report_by_class(class_id)

    if report.get("error"):
        print(f"[ERROR] {report['error']}")
        return

    class_info = report["class_info"]
    print("\n" + "="*80)
    print(f"BAO CAO DIEM DANH LOP: {class_info['name']} ({class_info['id']})")
    print("="*80)
    print(f"Mon hoc: {class_info['course_name']}")
    print(f"Hoc ky: {class_info['semester']}")
    print(f"Giang vien: {class_info['lecturer_id']}")

    summary = report["summary"]
    print(f"\nTONG QUAN:")
    print(f"- Tong so sinh vien: {summary['total_students']}")
    print(f"- Tong so buoi hoc: {summary['total_sessions']}")
    print(f"- Ty le diem danh trung binh: {summary['average_attendance_pct']:.2f}%")

    print("\n" + "-"*80)
    print(f"{'Ma SV':<10} | {'Ten SV':<25} | {'Tong':<6} | {'P':<5} | {'L':<5} | {'A':<5} | {'%':<8}")
    print("-"*80)

    for stat in report["student_stats"]:
        print(f"{stat['student_id']:<10} | {stat['student_name']:<25} | {stat['total_sessions']:<6} | "
              f"{stat['present']:<5} | {stat['late']:<5} | {stat['absent']:<5} | {stat['attendance_pct']:<8.2f}")

    print("-"*80)


def print_student_report(student_id: str) -> None:
    """Print formatted student attendance report to console."""
    report = generate_report_by_student(student_id)

    student_info = report["student_info"]
    print("\n" + "="*80)
    print(f"BAO CAO DIEM DANH SINH VIEN: {student_info['name']} ({student_info['id']})")
    print("="*80)

    summary = report["overall_summary"]
    print(f"TONG QUAN:")
    print(f"- Tong so lop: {summary['total_classes']}")
    print(f"- Tong so buoi hoc: {summary['total_sessions']}")
    print(f"- Tong Present: {summary['total_present']}")
    print(f"- Tong Late: {summary['total_late']}")
    print(f"- Tong Absent: {summary['total_absent']}")
    print(f"- Ty le diem danh: {summary['overall_attendance_pct']:.2f}%")

    print("\n" + "-"*80)
    print(f"{'Ma lop':<10} | {'Mon hoc':<30} | {'Tong':<6} | {'P':<5} | {'L':<5} | {'A':<5} | {'%':<8}")
    print("-"*80)

    for stat in report["class_stats"]:
        print(f"{stat['class_id']:<10} | {stat['course_name']:<30} | {stat['total_sessions']:<6} | "
              f"{stat['present']:<5} | {stat['late']:<5} | {stat['absent']:<5} | {stat['attendance_pct']:<8.2f}")

    print("-"*80)
