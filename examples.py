import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from courses.queries import (
    get_published_courses,
    get_courses_by_level,
    get_instructor_courses,
    get_popular_courses,
    get_student_active_courses,
    get_category_with_subcategories,
    get_expensive_courses,
    get_instructors_by_rating,
    get_courses_with_available_spots,
    get_student_statistics,
    get_instructor_statistics,
    update_enrollment_progress,
    complete_enrollment,
)

print("Published courses:")
print(get_published_courses())

print("\nBeginner courses:")
print(get_courses_by_level("beginner"))

print("\nInstructor 1 courses:")
print(get_instructor_courses(1))

print("\nPopular courses:")
print(get_popular_courses(2))

print("\nStudent 1 active courses:")
print(get_student_active_courses(1))

print("\nCategory with subcategories:")
print(get_category_with_subcategories(1))

print("\nExpensive courses:")
print(get_expensive_courses(2000))

print("\nInstructors with rating > 4:")
print(get_instructors_by_rating(4))

print("\nCourses with available spots:")
print(get_courses_with_available_spots())

print("\nStudent 1 statistics:")
print(get_student_statistics(1))

print("\nInstructor 1 statistics:")
print(get_instructor_statistics(1))

print("\nUpdate enrollment progress:")
print(update_enrollment_progress(1, 80))

print("\nComplete enrollment:")
print(complete_enrollment(1, 95))