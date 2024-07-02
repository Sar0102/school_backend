from rest_framework.permissions import BasePermission


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "director"


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "teacher"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "student"


class IsTeacherOrDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["teacher", "director"]
