from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_, name="logout"),
    path(
        "absence_table/<int:grade_id>/<int:section_id>/<int:group_id>/",
        views.absence_table,
        name="students_table",
    ),
    path("chose_grade/", views.chose_grade, name="chose_grade"),
    #     path('test/', views.test, name='test'),
    path(
        "single_student/<int:student_id>/",
        views.edit_student_information,
        name="student_information_edit",
    ),
    path(
        "participation/<int:grade_id>/<int:section_id>/<int:group_id>/",
        views.participation_table,
        name="participation_table",
    ),
]
