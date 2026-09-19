from .models import Course, Category, Instructor, Enrollment, Student
from django.db.models import Count, Q, F, Avg

def get_published_courses():
    return Course.objects.filter(is_published=True)

def get_courses_by_level(level):
    return Course.objects.filter(level=level)

def get_instructor_courses(instructor_id):
    return Course.objects.filter(instructor_id=instructor_id)

def get_popular_courses(min_students):
    return Course.objects.annotate(student_count=Count("students")).filter(student_count__gte=min_students)

def get_student_active_courses(student_id):
    return Course.objects.filter(enrollments__student_id=student_id, enrollments__status="in_progress",)

def get_category_with_subcategories(category_id):
    return Category.objects.filter(Q(id=category_id) | Q(parent_id=category_id))

def get_expensive_courses(min_price):
    return Course.objects.filter(price__gt=min_price)

def get_instructors_by_rating(min_rating):
    return Instructor.objects.filter(rating__gt=min_rating)

def get_courses_with_available_spots():
    return Course.objects.annotate(
        enrolled_count=Count(
            "enrollments",
            filter=~Q(enrollments__status="cancelled")
        )
    ).filter(
        Q(capacity__isnull=True) |
        Q(capacity__gt=F("enrolled_count"))
    )


def update_enrollment_progress(enrollment_id, progress):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollment.progress = progress
    enrollment.save()

    return enrollment

def complete_enrollment(enrollment_id, grade):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollment.status = "completed"
    enrollment.progress = 100
    enrollment.grade = grade
    enrollment.save()

    return enrollment


def get_student_statistics(student_id):
    enrollments = Enrollment.objects.filter(student_id=student_id)
    total_courses = enrollments.count()
    completed_courses = enrollments.filter(status="completed").count()
    average_grade = enrollments.filter(status="completed", grade__isnull=False,).aggregate(avg_grade=Avg("grade"))["avg_grade"]

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "average_grade": average_grade,
    }


def get_instructor_statistics(instructor_id):
    courses = Course.objects.filter(instructor_id=instructor_id)
    courses_count = courses.count()

    students_count = Student.objects.filter(courses__instructor_id=instructor_id).distinct().count()

    average_rating = courses.aggregate(avg_rating=Avg("reviews__rating"))["avg_rating"]

    return {
        "courses_count": courses_count,
        "students_count": students_count,
        "average_rating": average_rating,
    }