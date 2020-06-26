from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from main.models import Subjects, Grades


class GradeView(PermissionRequiredMixin, View):
    permission_required = ['main.view_grades']

    def get(self, request):
        context = {}
        context['title'] = "Oceny"
        subjects = []
        for subject in Subjects.objects.all():
            subject_ = {}
            subject_['name'] = subject.name
            grades = []
            for grade in Grades.objects.filter(student=request.user, subject=subject):
                grades.append(grade.value)
            subject_['grades'] = grades
            subjects.append(subject_)
        context['subjects'] = subjects
        return render(request, 'students/grade_list.html', context)
