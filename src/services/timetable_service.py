import os
from datetime import datetime
from typing import Optional

from src.models.attendance import TIME_FMT


def _data_path(filename: str) -> str:
	root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
	return os.path.join(root, filename)


def get_session_by_id(session_id: str) -> Optional[dict]:
	"""Return session info as a dict or None if not found.

	Reads `src/data/sessions.txt` which uses the format:
	S001,CL001,2024-11-10,08:00,Week1,Room A,Open
	Returned dict keys: id, class_id, date_str, time_str, start_datetime, status
	"""
	path = _data_path("sessions.txt")
	try:
		with open(path, "r", encoding="utf-8") as fh:
			for raw in fh:
				line = raw.strip()
				if not line:
					continue
				parts = [p.strip() for p in line.split(",")]
				if parts[0] == session_id:
					# parts: id, class_id, date(YYYY-MM-DD), time(HH:MM), ... , status
					sid = parts[0]
					class_id = parts[1]
					date_str = parts[2]
					time_str = parts[3]
					status = parts[-1]
					try:
						start_dt = datetime.strptime(f"{date_str} {time_str}", TIME_FMT)
					except Exception:
						# fallback: try iso
						start_dt = datetime.fromisoformat(f"{date_str}T{time_str}")
					return {
						"id": sid,
						"class_id": class_id,
						"date_str": date_str,
						"time_str": time_str,
						"start_datetime": start_dt,
						"status": status,
					}
	except FileNotFoundError:
		return None


	def get_students_in_session(session_id: str) -> list[tuple]:
		"""Return list of (student_id, student_name) for the session's class.

		Reads `class_student.txt` and `users.txt` to map student ids to names.
		"""
		sess = get_session_by_id(session_id)
		if not sess:
			return []
		class_id = sess.get("class_id")
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

		# build id->name map
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
	return None
