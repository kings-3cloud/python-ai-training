import pytest
from grade_tracker import GradeTracker


# ---------- Fixtures ----------

@pytest.fixture
def tracker():
    return GradeTracker()


# ---------- add_student ----------

def test_add_student_success(tracker):
    tracker.add_student("Alice")
    assert "Alice" in tracker._students


def test_add_student_duplicate(tracker):
    tracker.add_student("Alice")
    with pytest.raises(ValueError, match="already exists"):
        tracker.add_student("Alice")


# ---------- record_grade ----------

def test_record_grade_success(tracker):
    tracker.add_student("Alice")
    tracker.record_grade("Alice", "Math", 90)

    assert tracker._students["Alice"] == [("Math", 90)]


def test_record_grade_student_not_found(tracker):
    with pytest.raises(ValueError, match="not found"):
        tracker.record_grade("Bob", "Math", 80)


def test_record_grade_invalid_score(tracker):
    tracker.add_student("Alice")

    with pytest.raises(ValueError, match="between 0 and 100"):
        tracker.record_grade("Alice", "Math", 150)

    with pytest.raises(ValueError, match="between 0 and 100"):
        tracker.record_grade("Alice", "Math", -10)


# ---------- get_average ----------

def test_get_average_success(tracker):
    tracker.add_student("Alice")
    tracker.record_grade("Alice", "Math", 80)
    tracker.record_grade("Alice", "Science", 100)

    assert tracker.get_average("Alice") == 90


def test_get_average_student_not_found(tracker):
    with pytest.raises(ValueError, match="not found"):
        tracker.get_average("Bob")


def test_get_average_no_grades(tracker):
    tracker.add_student("Alice")
    with pytest.raises(ValueError, match="no grades"):
        tracker.get_average("Alice")


# ---------- get_top_student ----------

def test_get_top_student_success(tracker):
    tracker.add_student("Alice")
    tracker.add_student("Bob")

    tracker.record_grade("Alice", "Math", 80)
    tracker.record_grade("Bob", "Math", 90)

    assert tracker.get_top_student() == "Bob"


def test_get_top_student_skips_no_grades(tracker):
    tracker.add_student("Alice")  # no grades
    tracker.add_student("Bob")

    tracker.record_grade("Bob", "Math", 90)

    assert tracker.get_top_student() == "Bob"


def test_get_top_student_no_students(tracker):
    with pytest.raises(ValueError, match="No students"):
        tracker.get_top_student()


def test_get_top_student_no_grades_anyone(tracker):
    tracker.add_student("Alice")
    tracker.add_student("Bob")

    with pytest.raises(ValueError, match="No students have grades"):
        tracker.get_top_student()


# ---------- get_failing_students ----------

def test_get_failing_students_default_threshold(tracker):
    tracker.add_student("Alice")
    tracker.add_student("Bob")

    tracker.record_grade("Alice", "Math", 50)
    tracker.record_grade("Bob", "Math", 70)

    failing = tracker.get_failing_students()
    assert failing == ["Alice"]


def test_get_failing_students_custom_threshold(tracker):
    tracker.add_student("Alice")
    tracker.record_grade("Alice", "Math", 65)

    failing = tracker.get_failing_students(threshold=70)
    assert failing == ["Alice"]


def test_get_failing_students_skips_no_grades(tracker):
    tracker.add_student("Alice")  # no grades

    assert tracker.get_failing_students() == []

