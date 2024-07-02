from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Grade, Group, Student, Subject, User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role",)}),)


class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "grade")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role != "student":
            return qs
        return qs.filter(student__user=request.user)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    list_filter = ("teacher",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == "teacher":
            return qs.filter(teacher=request.user)
        else:
            return qs.filter(groups__student__user=request.user)


admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(User, CustomUserAdmin)
