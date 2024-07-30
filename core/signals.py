from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from core.models import Student, User


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    # Проверяем, что ContentType для моделей создан
    try:
        group_content_type = ContentType.objects.get(app_label="core", model="group")
        subject_content_type = ContentType.objects.get(
            app_label="core", model="subject"
        )
        grade_content_type = ContentType.objects.get(app_label="core", model="grade")
    except ContentType.DoesNotExist:
        # Если ContentType не существует, просто возвращаемся
        return

    # Создание групп
    director_group, created = Group.objects.get_or_create(name="Director")
    teacher_group, created = Group.objects.get_or_create(name="Teacher")
    student_group, created = Group.objects.get_or_create(name="Student")

    # Назначение разрешений группе Director (проверка существования)
    if director_group.permissions.count() == 0:
        director_permissions = Permission.objects.all()
        director_group.permissions.set(director_permissions)

    # Назначение разрешений группе Teacher
    # Разрешения на просмотр групп и предметов
    view_group_permission = Permission.objects.get(
        content_type=group_content_type, codename="view_group"
    )
    view_subject_permission = Permission.objects.get(
        content_type=subject_content_type, codename="view_subject"
    )

    # Разрешения на просмотр, добавление и изменение оценок
    view_grade_permission = Permission.objects.get(
        content_type=grade_content_type, codename="view_grade"
    )
    add_grade_permission = Permission.objects.get(
        content_type=grade_content_type, codename="add_grade"
    )
    change_grade_permission = Permission.objects.get(
        content_type=grade_content_type, codename="change_grade"
    )

    if teacher_group.permissions.count() == 0:
        teacher_group.permissions.set(
            [
                view_group_permission,
                view_subject_permission,
                view_grade_permission,
                add_grade_permission,
                change_grade_permission,
            ]
        )

    # Назначение разрешений группе Student
    student_permissions = Permission.objects.filter(
        content_type=grade_content_type, codename__startswith="view_"
    )
    if student_group.permissions.count() == 0:
        student_group.permissions.set(student_permissions)
        student_group.permissions.add(view_subject_permission)


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "student":
        Student.objects.create(user=instance)
