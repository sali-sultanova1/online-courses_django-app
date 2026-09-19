# Online Courses

Приложение для управления онлайн-курсами с использованием Django ORM.

## Запуск проекта

1. Установить Django:

```bash
pip install django
```

2. Выполнить миграции:

```bash
python manage.py migrate
```

3. Создать админа:

```bash
python manage.py createsuperuser
```

4. Запустить сервер:

```bash
python manage.py runserver
```

5. Открыть админ-панель:

```text
http://127.0.0.1:8000/admin/
```

## Основные модели

- Instructor
- Category
- Course
- Student
- Enrollment

## Дополнительные модели

- Review
- Lesson

## Реализовано

- связи между моделями;
- ManyToMany связь Student и Course через Enrollment;
- категории и подкатегории;
- QuerySet-запросы в файле `courses/queries.py`;
- Django Admin;
- inline для Enrollment;
- подсчет количества свободных мест курса;
- получение завершенных курсов студента;
- отзывы и подсчет среднего рейтинга курса;
- уроки курса;
- custom manager для получения популярных и новых курсов.

## QuerySet-запросы

В файле `courses/queries.py` реализованы функции:

- `get_published_courses()`
- `get_courses_by_level(level)`
- `get_instructor_courses(instructor_id)`
- `get_popular_courses(min_students)`
- `get_student_active_courses(student_id)`
- `get_category_with_subcategories(category_id)`
- `get_expensive_courses(min_price)`
- `get_instructors_by_rating(min_rating)`
- `get_courses_with_available_spots()`
- `update_enrollment_progress(enrollment_id, progress)`
- `complete_enrollment(enrollment_id, grade)`
- `get_student_statistics(student_id)`
- `get_instructor_statistics(instructor_id)`


## Примеры использования

Примеры вызова функций из `courses/queries.py` находятся в файле:

`examples.py`

Запуск:

```bash
python examples.py
```

## Доступ к админ-панели

Админ-панель:

http://127.0.0.1:8000/admin/

Тестовый администратор:

- Username: admin
- Password: CourseAdmin2026!