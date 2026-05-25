"""
Exercise 1 Solution: Student Grade Tracker
======================================================
"""


class GradeTracker:
    """Tracks students and their grades across subjects."""

    def __init__(self):
        self._students: dict[str, list[tuple[str, float]]] = {}

    def add_student(self, name: str):
        """Add a student. Raises ValueError if already exists."""
        if name in self._students:
            raise ValueError(f"Student '{name}' already exists")
        self._students[name] = []

    def record_grade(self, name: str, subject: str, score: float):
        """
        Record a grade (0-100) for a student in a subject.
        Raises ValueError if student not found or score out of range.
        """
        if name not in self._students:
            raise ValueError(f"Student '{name}' not found")
        if not (0 <= score <= 100):
            raise ValueError(f"Score must be between 0 and 100, got {score}")
        self._students[name].append((subject, score))

    def get_average(self, name: str) -> float:
        """Return the student's average grade. Raises ValueError if not found or no grades."""
        if name not in self._students:
            raise ValueError(f"Student '{name}' not found")
        grades = self._students[name]
        if not grades:
            raise ValueError(f"Student '{name}' has no grades recorded")
        return sum(score for _, score in grades) / len(grades)

    def get_top_student(self) -> str:
        """Return the name of the student with the highest average."""
        if not self._students:
            raise ValueError("No students in tracker")

        best_name = None
        best_avg = -1

        for name in self._students:
            try:
                avg = self.get_average(name)
                if avg > best_avg:
                    best_avg = avg
                    best_name = name
            except ValueError:
                continue  # skip students with no grades

        if best_name is None:
            raise ValueError("No students have grades recorded")
        return best_name

    def get_failing_students(self, threshold: float = 60) -> list[str]:
        """Return a list of students with average below the threshold."""
        failing = []
        for name in self._students:
            try:
                if self.get_average(name) < threshold:
                    failing.append(name)
            except ValueError:
                continue  # skip students with no grades
        return failing
