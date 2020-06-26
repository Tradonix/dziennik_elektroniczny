from django.urls import path
from students import views

urlpatterns = [
    path('grades/', views.GradeView.as_view(), name='student_grades'),
]
