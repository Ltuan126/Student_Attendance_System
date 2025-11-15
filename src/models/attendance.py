from enum import Enum
from datetime import datetime
from typing import Optional


TIME_FMT = "%Y-%m-%d %H:%M"


class AttendanceState(Enum):
    """Enum trạng thái điểm danh"""
    PRESENT = "Present"
    LATE = "Late"
    ABSENT = "Absent"


class AttendanceRecord:
    def __init__(
        self,
        record_id: str,
        student_id: str,
        session_id: str,
        check_in_time: Optional[datetime] = None,
        state: AttendanceState = AttendanceState.ABSENT,
        note: Optional[str] = None,
    ):
        self.record_id = record_id
        self.student_id = student_id
        self.session_id = session_id
        self.check_in_time = check_in_time
        self.state = state
        self.note = note or ""
    
    def to_line(self) -> str:
        # Format thời gian
        time_str = ""
        if self.check_in_time:
            time_str = self.check_in_time.strftime(TIME_FMT)
        
        # Xử lý note (thay dấu phẩy bằng dấu chấm phẩy để tránh lỗi CSV)
        note_clean = self.note.replace(",", ";").replace("\n", " ")
        
        return f"{self.record_id},{self.student_id},{self.session_id},{time_str},{self.state.value},{note_clean}"
    
    @classmethod
    def from_line(cls, line: str) -> "AttendanceRecord":
        parts = line.strip().split(",")
        
        # Đảm bảo có đủ 6 phần (padding nếu thiếu)
        while len(parts) < 6:
            parts.append("")
        
        record_id = parts[0].strip()
        student_id = parts[1].strip()
        session_id = parts[2].strip()
        time_str = parts[3].strip()
        state_str = parts[4].strip()
        note = parts[5].strip()
        
        # Parse thời gian
        check_in_time = None
        if time_str:
            try:
                check_in_time = datetime.strptime(time_str, TIME_FMT)
            except ValueError:
                # Thử format khác nếu có
                try:
                    check_in_time = datetime.fromisoformat(time_str)
                except:
                    pass
        
        # Parse state
        state = AttendanceState.ABSENT  # Default
        for s in AttendanceState:
            if s.value.lower() == state_str.lower():
                state = s
                break
        
        return cls(record_id, student_id, session_id, check_in_time, state, note)
    
    def __repr__(self) -> str:
        return (
            f"AttendanceRecord({self.record_id!r}, {self.student_id!r}, "
            f"{self.session_id!r}, {self.state!r})"
        )