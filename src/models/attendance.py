"""Simplified attendance model.

This version keeps things intentionally minimal:
- check_in_time is stored as a plain string (no datetime parsing)
- note is a simple optional string
- serialization is a simple comma-separated line; commas inside note are replaced
  with semicolons to keep parsing trivial.
"""

from enum import Enum
from typing import Optional


class AttendanceState(Enum):
	PRESENT = "Present"
	LATE = "Late"
	ABSENT = "Absent"


class AttendanceRecord:
	"""Minimal attendance record used for storage in attendance.txt.

	Fields order in file: record_id,student_id,session_id,check_in_time,state,note
	check_in_time is a string like "2024-11-10 08:01" or empty when not available.
	"""

	def __init__(
		self,
		record_id: str,
		student_id: str,
		session_id: str,
		check_in_time: str = "",
		state: AttendanceState = AttendanceState.ABSENT,
		note: Optional[str] = None,
	):
		self.record_id = record_id
		self.student_id = student_id
		self.session_id = session_id
		self.check_in_time = check_in_time
		self.state = state
		self.note = note

	def to_line(self) -> str:
		"""Serialize to a simple CSV line. Replace commas in note with semicolons."""
		note_part = (self.note or "")
		note_part = note_part.replace("\n", " ").replace(",", ";")
		return f"{self.record_id},{self.student_id},{self.session_id},{self.check_in_time},{self.state.value},{note_part}"

	@classmethod
	def from_line(cls, line: str) -> "AttendanceRecord":
		"""Parse a line (simple split). Returns AttendanceRecord.

		This is intentionally lenient and simple.
		"""
		parts = line.rstrip("\n").split(",")
		# ensure at least 6 elements (pad missing with empty strings)
		parts += [""] * (6 - len(parts))
		record_id, student_id, session_id, check_in_time, state_str, note = [p.strip() for p in parts[:6]]

		# map state_str to AttendanceState (case-insensitive)
		state = AttendanceState.ABSENT
		for s in AttendanceState:
			if s.value.lower() == state_str.lower():
				state = s
				break

		# restore note as-is (commas were replaced on write)
		note = note or None

		return cls(record_id, student_id, session_id, check_in_time, state, note)

	def __repr__(self) -> str:
		return (
			f"AttendanceRecord({self.record_id!r}, {self.student_id!r}, {self.session_id!r}, "
			f"{self.check_in_time!r}, {self.state!r}, {self.note!r})"
		)

