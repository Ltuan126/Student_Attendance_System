from enum import Enum


class SessionStatus(Enum):
    """Enum để quản lý trạng thái của buổi học."""
    OPEN = "Open"      # Cho phép điểm danh
    LOCKED = "Locked"  # Không cho phép điểm danh


class Course:
  
    def __init__(self, course_id, name, credits):
        self.course_id = course_id  # Mã môn, VD: CS101
        self.name = name            # Tên môn
        self.credits = credits      # Số tín chỉ

class Class:
  
    def __init__(self, class_id, course_id, lecturer_id, student_ids):
        self.class_id = class_id        # Mã lớp, VD: CS101_N1
        self.course_id = course_id      # Mã môn học (tham chiếu tới Course)
        self.lecturer_id = lecturer_id  # ID giảng viên
        self.student_ids = student_ids  # Danh sách [ID sinh viên 1, ID sinh viên 2, ...]

class Session:
  
    def __init__(self, session_id, class_id, session_date, start_time, end_time, room):
        self.session_id = session_id    # Mã buổi học, VD: SS001
        self.class_id = class_id        # Mã lớp học (tham chiếu tới Class)
        self.session_date = session_date # Ngày học (dạng chuỗi, VD: "2025-10-28")
        self.start_time = start_time    # Giờ bắt đầu (dạng chuỗi, VD: "07:30")
        self.end_time = end_time        # Giờ kết thúc (dạng chuỗi, VD: "09:00")
        self.room = room                # Phòng học, VD: A1-201
        
        # Trạng thái "Open" (cho phép điểm danh) hoặc "Locked" (không cho phép)
        # Mặc định là "Locked" khi mới tạo
        self.status = SessionStatus.LOCKED