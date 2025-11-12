import os
from datetime import datetime, timedelta
from typing import List, Optional

from src.models.attendance import AttendanceRecord, AttendanceState, TIME_FMT
from src.services.timetable_service import get_session_by_id


def _data_path(filename: str) -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return os.path.join(root, filename)


def _next_record_id() -> str:
    path = _data_path("attendance.txt")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            max_num = 0
            for line in fh:
                parts = line.strip().split(",")
                if not parts:
                    continue
                rid = parts[0]
                if rid.startswith("A") and rid[1:].isdigit():
                    num = int(rid[1:])
                    if num > max_num:
                        max_num = num
            return f"A{max_num+1:03d}"
    except FileNotFoundError:
        return "A001"


def student_checkin(student_id: str, session_id: str) -> bool:
    """Student checks in for a session.

    Logic (simple):
    - call get_session_by_id(session_id)
    - ensure session exists and status == 'Open'
    - compare now with session start: within 15 minutes => PRESENT else LATE
    - append record to attendance.txt
    - return True on success, False on failure
    """
    sess = get_session_by_id(session_id)
    if not sess:
        return False
    if sess.get("status", "").lower() != "open":
        return False

    now = datetime.now()
    start: datetime = sess["start_datetime"]
    # simple rule: <= start + 15 minutes => PRESENT, else LATE
    if now <= start + timedelta(minutes=15):
        state = AttendanceState.PRESENT
    else:
        state = AttendanceState.LATE

    rid = _next_record_id()
    record = AttendanceRecord(rid, student_id, session_id, now, state, None)

    path = _data_path("attendance.txt")
    line = record.to_line()
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")

    return True


def lecturer_take_attendance(session_id: str) -> None:
    """Lecturer takes attendance for a session.

    Behavior:
    - get list of (student_id, name) via get_students_in_session
    - for each student prompt the lecturer to enter P/L/A (default P)
    - write all entered records to attendance.txt
    """
    from src.services.timetable_service import get_students_in_session

    sess = get_session_by_id(session_id)
    if not sess or sess.get("status", "").lower() != "open":
        print(f"Session {session_id} not found or not open")
        return

    students = get_students_in_session(session_id)
    if not students:
        print("No students found for this session")
        return

    print("Enter attendance for each student: P = Present, L = Late, A = Absent (press Enter for P)")
    answers: List[tuple] = []
    for sid, name in students:
        while True:
            resp = input(f"{sid} - {name} [P/L/A]: ").strip().upper()
            if resp == "":
                resp = "P"
            if resp in ("P", "L", "A"):
                answers.append((sid, resp))
                break
            print("Invalid input. Please enter P, L or A.")

    # append all records
    path = _data_path("attendance.txt")
    start: datetime = sess["start_datetime"]
    with open(path, "a", encoding="utf-8") as fh:
        for sid, resp in answers:
            state = AttendanceState.PRESENT if resp == "P" else AttendanceState.LATE if resp == "L" else AttendanceState.ABSENT
            rid = _next_record_id()
            rec = AttendanceRecord(rid, sid, session_id, start if resp != "A" else None, state, None)
            fh.write(rec.to_line() + "\n")


def get_student_history(student_id: str) -> List[AttendanceRecord]:
    """Return list of AttendanceRecord objects for the student (all records).

    Reads attendance.txt and parses lines with AttendanceRecord.from_line.
    """
    path = _data_path("attendance.txt")
    out: List[AttendanceRecord] = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                try:
                    rec = AttendanceRecord.from_line(line)
                except Exception:
                    continue
                if rec.student_id == student_id:
                    out.append(rec)
    except FileNotFoundError:
        return []
    # compute stats
    total = len(out)
    present = sum(1 for r in out if r.state == AttendanceState.PRESENT)
    late = sum(1 for r in out if r.state == AttendanceState.LATE)
    absent = sum(1 for r in out if r.state == AttendanceState.ABSENT)
    attendance_pct = 0.0
    if total > 0:
        attendance_pct = (present + late) / total * 100.0

    stats = {
        "total": total,
        "present": present,
        "late": late,
        "absent": absent,
        "attendance_pct": round(attendance_pct, 2),
    }
    return out, stats
