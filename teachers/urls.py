from django.urls import path
from teachers import views

urlpatterns = [
    # path('subject/<int:pk>', views.SubjectView.as_view(), name='subject'),
    path('subjects/', views.SubjectListView.as_view(), name='subjects'),
    path('subject/add/', views.SubjectAddView.as_view(), name='subject_add'),
    path('subject/edit/<int:pk>/', views.SubjectEditView.as_view(), name='subject_edit'),
    path('grade/<int:pk>', views.GradeView.as_view(), name='grade'),
    path('grades/', views.GradeListView.as_view(), name='grades'),
    path('grade/add/', views.GradeAddView.as_view(), name='grade_add'),
    # path('grade/edit/<int:pk>/', views.GradeEditView.as_view(), name='grade_edit'),
]
