from rest_framework import serializers

from .models import Grade, Group, Student, Subject, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Student
        fields = ["id", "name", "group_id"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"


class LoginPayloadSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
