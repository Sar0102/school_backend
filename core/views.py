from django.db.models import Avg, F, Value
from django.db.models.functions import Concat
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Grade
from .models import Group
from .models import Group as StudentGroup
from .models import Student, Subject, User
from .permissions import IsDirector, IsTeacher, IsTeacherOrDirector
from .serializers import (
    GradeSerializer,
    GroupSerializer,
    StudentSerializer,
    SubjectSerializer,
    UserSerializer,
)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDirector]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDirector]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDirector]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTeacher]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDirector]


class GroupListView(ListAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrDirector]


class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrDirector]


class StudentAverageGradesView(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    def get(self, request, student_id):
        grades = Grade.objects.filter(student_id=student_id).select_related(
            "subject", "student__group", "student__user"
        )
        avg_grades = (
            grades.values(
                subject_name=F("subject__name"),
                group=F("student__group__name"),
                full_name=Concat(
                    F("student__user__first_name"),
                    Value(" "),
                    F("student__user__last_name"),
                ),
            )
            .annotate(avg_grade=Avg("grade"))
            .order_by("subject__name")
        )
        return Response(avg_grades)


class GroupAverageGradesView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrDirector]

    def get(self, request, group_id):
        group_name = (
            Group.objects.filter(id=group_id).values_list("name", flat=True).first()
        )
        avg_grades = Grade.objects.raw(
            """
            SELECT 1 as id, subject_id, AVG(grade) as avg_grade
            FROM core_grade
            WHERE student_id IN (SELECT id FROM core_student WHERE group_id = %s)
            GROUP BY subject_id
            """,
            [group_id],
        )
        return Response(
            [
                {
                    "group_name": group_name,
                    "subject": g.subject.name,
                    "avg_grade": g.avg_grade,
                }
                for g in avg_grades
            ]
        )
