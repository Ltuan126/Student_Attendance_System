import os
from datetime import datetime, timedelta
from typing import List, Optional

try:
    # package-style imports when running `python -m src.main`
    from src.models.attendance import AttendanceRecord, AttendanceState, TIME_FMT
    from src.services.timetable_service import get_session_by_id, get_students_in_session
except Exception:
    # script-style imports when running `python main.py` from inside src/
    from models.attendance import AttendanceRecord, AttendanceState, TIME_FMT
    from services.timetable_service import get_session_by_id, get_students_in_session


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


def student_checkin(student_id: str, session_id: str) -> tuple[bool, str]:
    sess = get_session_by_id(session_id)
    if not sess:
        return False, f"Session {session_id} not found."
    if sess.get("status", "").lower() != "open":
        return False, f"Session {session_id} is not open for check-in."

    # Check if student already checked in for this session
    path = _data_path("attendance.txt")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    _, sid, sess_id = parts[0], parts[1], parts[2]
                    if sid == student_id and sess_id == session_id:
                        return False, "You have already checked in for this session."
    except FileNotFoundError:
        pass  # File doesn't exist yet, first record

    now = datetime.now()
    start: datetime = sess["start_datetime"]
    # simple rule: <= start + 15 minutes => PRESENT, else LATE
    if now <= start + timedelta(minutes=15):
        state = AttendanceState.PRESENT
    else:
        state = AttendanceState.LATE

    rid = _next_record_id()
    record = AttendanceRecord(rid, student_id, session_id, now, state, None)

    line = record.to_line()
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")

    return True, f"Checked in as {state.value}."


def lecturer_take_attendance(session_id: str) -> None:
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

    # Read all existing records first to get the max ID
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
            next_id_num = max_num + 1
    except FileNotFoundError:
        next_id_num = 1

    # Now write all records with sequential IDs
    with open(path, "a", encoding="utf-8") as fh:
        for sid, resp in answers:
            state = AttendanceState.PRESENT if resp == "P" else AttendanceState.LATE if resp == "L" else AttendanceState.ABSENT
            rid = f"A{next_id_num:03d}"
            next_id_num += 1
            rec = AttendanceRecord(rid, sid, session_id, start if resp != "A" else None, state, None)
            fh.write(rec.to_line() + "\n")


def get_student_history(student_id: str) -> tuple[List[AttendanceRecord], dict]:
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
        return [], {"total": 0, "present": 0, "late": 0, "absent": 0, "attendance_pct": 0.0}
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
