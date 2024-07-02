from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def create_groups(apps, schema_editor):
    # Создание группы Director
    director_group, _ = Group.objects.get_or_create(name="Director")
    teacher_group, _ = Group.objects.get_or_create(name="Teacher")
    student_group, _ = Group.objects.get_or_create(name="Student")

    # Назначение разрешений группе Director
    director_permissions = Permission.objects.all()
    director_group.permissions.set(director_permissions)

    # Назначение разрешений группе Teacher
    # Разрешения на просмотр групп и предметов
    group_content_type = ContentType.objects.get(app_label="core", model="group")
    subject_content_type = ContentType.objects.get(app_label="core", model="subject")
    grade_content_type = ContentType.objects.get(app_label="core", model="grade")

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
    student_group.permissions.set(student_permissions, view_subject_permission)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
