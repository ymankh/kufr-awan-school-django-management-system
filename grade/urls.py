from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout_, name="logout"),
    path('students_tabels/<int:grade_id>/<int:section_id>/', views.students_table, name="students_table"),
    path('chose_grade/', views.chose_grade, name="chose_grade"),
]
