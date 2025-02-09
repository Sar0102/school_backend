from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.login_view import TokenObtainPairView, TokenRefreshView
from core.views import (
    GradeViewSet,
    GroupAverageGradesView,
    GroupListView,
    GroupViewSet,
    StudentAverageGradesView,
    StudentListView,
    StudentViewSet,
    SubjectViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("groups", GroupViewSet)
router.register("students", StudentViewSet)
router.register("subjects", SubjectViewSet)
router.register("grades", GradeViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path(
        "students/<int:student_id>/average/",
        StudentAverageGradesView.as_view(),
        name="student_average_grades",
    ),
    path(
        "groups/<int:group_id>/average/",
        GroupAverageGradesView.as_view(),
        name="group_average_grades",
    ),
]
