from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=200)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )

    start_date = models.DateField()
    biography = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=160, unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class CourseManager(models.Manager):
    def popular(self):
        return self.get_queryset().annotate(student_count=models.Count("students")).order_by("-student_count")

    def new(self):
        return self.get_queryset().order_by("-created_at")


class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    objects = CourseManager()
    title = models.CharField(max_length=200)

    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.PROTECT,
        related_name="courses",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="courses",
    )

    description = models.TextField()
    duration_hours = models.PositiveIntegerField()

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField(null=True, blank=True,)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title


    def available_spots(self):
        if self.capacity is None:
            return None

        all_enrollments = self.enrollments.count()
        cancelled = self.enrollments.filter(status="cancelled").count()

        return max(self.capacity - (all_enrollments - cancelled), 0)

    def average_rating(self):
        result = self.reviews.aggregate(average=Avg("rating"))
        return result["average"]



class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField(
        Course,
        through="Enrollment",
        related_name="students",
        blank=True,
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def completed_courses(self):
        return self.courses.filter(enrollments__student=self,enrollments__status="completed",).distinct()


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
    )

    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    grade = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    class Meta:
        ordering = ["-enrollment_date"]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.course}"




class Review(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.course} - {self.rating}"



class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f"{self.course} - {self.title}"

