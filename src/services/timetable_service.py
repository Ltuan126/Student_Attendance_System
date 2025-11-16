import os
from datetime import datetime
from typing import Optional

from models.attendance import TIME_FMT

def _data_path(filename: str) -> str:
	root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
	return os.path.join(root, filename)


def load_courses() -> list[dict]:

	path = _data_path("courses.txt")
	courses = []
	try:
		with open(path, "r", encoding="utf-8") as fh:
			for raw in fh:
				line = raw.strip()
				if not line:
					continue
				parts = [p.strip() for p in line.split(",")]
				if len(parts) >= 3:
					courses.append({
						"id": parts[0],
						"name": parts[1],
						"credits": parts[2]
					})
	except FileNotFoundError:
		pass
	return courses


def load_classes() -> list[dict]:

	path = _data_path("classes.txt")
	classes = []
	try:
		with open(path, "r", encoding="utf-8") as fh:
			for raw in fh:
				line = raw.strip()
				if not line:
					continue
				parts = [p.strip() for p in line.split(",")]
				if len(parts) >= 5:
					classes.append({
						"id": parts[0],
						"name": parts[1],
						"semester": parts[2],
						"course_id": parts[3],
						"lecturer_id": parts[4]
					})
	except FileNotFoundError:
		pass
	return classes


def load_sessions() -> list[dict]:

	path = _data_path("sessions.txt")
	sessions = []
	try:
		with open(path, "r", encoding="utf-8") as fh:
			for raw in fh:
				line = raw.strip()
				if not line:
					continue
				parts = [p.strip() for p in line.split(",")]
				if len(parts) >= 7:
					sessions.append({
						"id": parts[0],
						"class_id": parts[1],
						"date_str": parts[2],
						"time_str": parts[3],
						"week": parts[4],
						"room": parts[5],
						"status": parts[6]
					})
	except FileNotFoundError:
		pass
	return sessions


def get_session_by_id(session_id: str) -> Optional[dict]:
	
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


def get_student_timetable(student_id: str) -> list[dict]:
	
	# Find all classes this student is enrolled in
	cs_path = _data_path("class_student.txt")
	student_classes = []
	try:
		with open(cs_path, "r", encoding="utf-8") as fh:
			for raw in fh:
				line = raw.strip()
				if not line:
					continue
				parts = [p.strip() for p in line.split(",")]
				if len(parts) >= 2 and parts[1] == student_id:
					student_classes.append(parts[0])
	except FileNotFoundError:
		return []

	# Get all sessions for these classes
	all_sessions = load_sessions()
	student_sessions = [
		sess for sess in all_sessions
		if sess.get("class_id") in student_classes
	]

	return student_sessions


def get_students_in_session(session_id: str) -> list[tuple]:
	
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
