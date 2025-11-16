from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class CorrectionStatus(Enum):
    """Trạng thái yêu cầu chỉnh sửa điểm danh"""
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    
    @classmethod
    def from_string(cls, value: str) -> 'CorrectionStatus':
        """Parse string thành CorrectionStatus"""
        mapping = {
            'PENDING': cls.PENDING,
            'APPROVED': cls.APPROVED,
            'REJECTED': cls.REJECTED
        }
        upper_value = value.upper().strip()
        if upper_value not in mapping:
            raise ValueError(f"Invalid correction status: {value}")
        return mapping[upper_value]


@dataclass
class CorrectionRequest:
    """
    Yêu cầu chỉnh sửa điểm danh
    
    Format trong file: request_id|student_id|session_id|record_id|reason|status|note|timestamp|lecturer_id
    VD: CR0001|SV001|S001|REC005|Quen check-in do ket xe|Pending||2025-11-15 10:30:00|LEC001
    """
    request_id: str
    student_id: str
    session_id: str
    record_id: str
    reason: str
    status: CorrectionStatus
    lecturer_id: str
    note: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate và set default values"""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        
        # Convert string status to enum if needed
        if isinstance(self.status, str):
            self.status = CorrectionStatus.from_string(self.status)
    
    def to_line(self) -> str:
        """Chuyển request thành 1 dòng text để ghi file"""
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        note_str = self.note or ""
        return f"{self.request_id}|{self.student_id}|{self.session_id}|{self.record_id}|{self.reason}|{self.status.value}|{note_str}|{timestamp_str}|{self.lecturer_id}"
    
    @classmethod
    def from_line(cls, line: str) -> 'CorrectionRequest':
        """Parse 1 dòng text thành CorrectionRequest"""
        parts = line.strip().split('|')
        if len(parts) != 9:
            raise ValueError(f"Invalid correction request format: {line}")
        
        request_id, student_id, session_id, record_id, reason, status_str, note, timestamp_str, lecturer_id = parts
        
        try:
            status = CorrectionStatus.from_string(status_str)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid data in correction request: {line}") from e
        
        return cls(
            request_id=request_id,
            student_id=student_id,
            session_id=session_id,
            record_id=record_id,
            reason=reason,
            status=status,
            lecturer_id=lecturer_id,
            note=note if note else None,
            timestamp=timestamp
        )