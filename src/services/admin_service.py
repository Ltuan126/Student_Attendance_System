import os
from typing import List, Optional

from models.user import User, Student, Lecturer, Admin

def _data_path(filename: str) -> str:
    """Get absolute path to data file."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return os.path.join(root, filename)


# ============================================================================
# USER MANAGEMENT
# ============================================================================

def list_users() -> List[User]:
    """Load and return all users from users.txt."""
    users = []
    path = _data_path("users.txt")

    if not os.path.exists(path):
        return users

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 5:
                user_id, name, email, password, role = parts[0], parts[1], parts[2], parts[3], parts[4]
                if role == "student":
                    users.append(Student(user_id, name, email, password))
                elif role == "lecturer":
                    users.append(Lecturer(user_id, name, email, password))
                elif role == "admin":
                    users.append(Admin(user_id, name, email, password))
                else:
                    users.append(User(user_id, name, email, password, role))
    return users


def save_users(users: List[User]) -> bool:
    """Save all users to users.txt."""
    path = _data_path("users.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for u in users:
                f.write(f"{u.id},{u.name},{u.email},{u.password},{u.role}\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save users: {e}")
        return False


def add_user(name: str, email: str, password: str, role: str) -> bool:
    """Add a new user to the system."""
    users = list_users()

    # Check for duplicate email
    for u in users:
        if u.email == email:
            print(f"[ERROR] Email {email} already exists.")
            return False

    # Validate role
    if role not in ["student", "lecturer", "admin"]:
        print(f"[ERROR] Invalid role: {role}")
        return False

    # Generate new user ID
    max_id = 0
    for u in users:
        if u.id.startswith("U") and u.id[1:].isdigit():
            num = int(u.id[1:])
            if num > max_id:
                max_id = num
    new_id = f"U{max_id + 1:03d}"

    # Create user object
    if role == "student":
        new_user = Student(new_id, name, email, password)
    elif role == "lecturer":
        new_user = Lecturer(new_id, name, email, password)
    elif role == "admin":
        new_user = Admin(new_id, name, email, password)
    else:
        new_user = User(new_id, name, email, password, role)

    users.append(new_user)
    return save_users(users)


def delete_user(user_id: str) -> bool:
    """Delete a user by ID."""
    users = list_users()
    original_count = len(users)
    users = [u for u in users if u.id != user_id]

    if len(users) == original_count:
        print(f"[ERROR] User {user_id} not found.")
        return False

    return save_users(users)


# ============================================================================
# COURSE MANAGEMENT
# ============================================================================

def list_courses() -> List[dict]:
    """Load and return all courses from courses.txt."""
    courses = []
    path = _data_path("courses.txt")

    if not os.path.exists(path):
        return courses

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 3:
                courses.append({
                    "id": parts[0].strip(),
                    "name": parts[1].strip(),
                    "credits": parts[2].strip()
                })
    return courses


def save_courses(courses: List[dict]) -> bool:
    """Save all courses to courses.txt."""
    path = _data_path("courses.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for c in courses:
                f.write(f"{c['id']},{c['name']},{c['credits']}\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save courses: {e}")
        return False


def add_course(name: str, credits: str) -> bool:
    """Add a new course to the system."""
    courses = list_courses()

    # Generate new course ID
    max_id = 0
    for c in courses:
        cid = c["id"]
        if cid.startswith("C") and cid[1:].isdigit():
            num = int(cid[1:])
            if num > max_id:
                max_id = num
    new_id = f"C{max_id + 1:03d}"

    new_course = {
        "id": new_id,
        "name": name,
        "credits": credits
    }

    courses.append(new_course)
    return save_courses(courses)


def delete_course(course_id: str) -> bool:
    """Delete a course by ID."""
    courses = list_courses()
    original_count = len(courses)
    courses = [c for c in courses if c["id"] != course_id]

    if len(courses) == original_count:
        print(f"[ERROR] Course {course_id} not found.")
        return False

    return save_courses(courses)


# ============================================================================
# CLASS MANAGEMENT
# ============================================================================

def list_classes() -> List[dict]:
    """Load and return all classes from classes.txt."""
    classes = []
    path = _data_path("classes.txt")

    if not os.path.exists(path):
        return classes

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 5:
                classes.append({
                    "id": parts[0].strip(),
                    "name": parts[1].strip(),
                    "semester": parts[2].strip(),
                    "course_id": parts[3].strip(),
                    "lecturer_id": parts[4].strip()
                })
    return classes


def save_classes(classes: List[dict]) -> bool:
    """Save all classes to classes.txt."""
    path = _data_path("classes.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for c in classes:
                f.write(f"{c['id']},{c['name']},{c['semester']},{c['course_id']},{c['lecturer_id']}\n")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save classes: {e}")
        return False


def add_class(name: str, semester: str, course_id: str, lecturer_id: str) -> bool:
    """Add a new class to the system."""
    classes = list_classes()

    # Generate new class ID
    max_id = 0
    for c in classes:
        cid = c["id"]
        if cid.startswith("CL") and cid[2:].isdigit():
            num = int(cid[2:])
            if num > max_id:
                max_id = num
    new_id = f"CL{max_id + 1:03d}"

    new_class = {
        "id": new_id,
        "name": name,
        "semester": semester,
        "course_id": course_id,
        "lecturer_id": lecturer_id
    }

    classes.append(new_class)
    return save_classes(classes)


def delete_class(class_id: str) -> bool:
    """Delete a class by ID."""
    classes = list_classes()
    original_count = len(classes)
    classes = [c for c in classes if c["id"] != class_id]

    if len(classes) == original_count:
        print(f"[ERROR] Class {class_id} not found.")
        return False

    return save_classes(classes)


# ============================================================================
# SYSTEM REPORTS
# ============================================================================

def get_system_statistics() -> dict:
    """Get basic system statistics."""
    users = list_users()
    courses = list_courses()
    classes = list_classes()

    # Count users by role
    student_count = sum(1 for u in users if u.role == "student")
    lecturer_count = sum(1 for u in users if u.role == "lecturer")
    admin_count = sum(1 for u in users if u.role == "admin")

    return {
        "total_users": len(users),
        "students": student_count,
        "lecturers": lecturer_count,
        "admins": admin_count,
        "total_courses": len(courses),
        "total_classes": len(classes)
    }
