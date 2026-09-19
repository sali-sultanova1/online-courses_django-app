from django.contrib import admin
from .models import Instructor, Category, Course, Student, Enrollment, Review, Lesson

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "specialization", "rating", "is_active")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "category", "level", "price", "is_published", "capacity")
    inlines = [EnrollmentInline]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "registration_date")
    inlines = [EnrollmentInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "progress", "grade", "enrollment_date")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "rating", "comment")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "duration_minutes")