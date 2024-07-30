from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("director", "Director"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.role == "director":
            self.is_staff = True
            self.is_superuser = True
        elif self.role == "teacher":
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super(User, self).save(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "teacher"}
    )
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return f"{self.name}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.subject}: {self.grade}"
