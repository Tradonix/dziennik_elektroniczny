from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from main.models import Subjects, Grades


class SubjectAddView(PermissionRequiredMixin, View):
    permission_required = ['main.add_subjects']

    def get(self, request):
        context = {}
        context['btn'] = "Dodaj"
        context['title'] = 'Dodaj przedmiot'
        g = Group.objects.get(name='teachers')
        context['teachers'] = g.user_set.all()
        g = Group.objects.get(name='students')
        context['students'] = g.user_set.all()
        return render(request, 'teachers/subject_form.html', context)

    def post(self, request):
        context = {}
        context['btn'] = "Dodaj"
        context['title'] = 'Dodaj przedmiot'
        name = request.POST.get('name')
        context['name'] = name
        teacher = User.objects.get(pk=request.POST.get('teachers'))
        context['selected'] = teacher.id
        g = Group.objects.get(name='teachers')
        context['teachers'] = g.user_set.all()
        g = Group.objects.get(name='students')
        context['students'] = g.user_set.all()
        students_id = request.POST.getlist('students')
        context['selected_students'] = students_id
        if name and teacher and students_id:
            s = Subjects.objects.create(name=name, teacher=teacher)
            s.students.set(students_id)
            return redirect(reverse_lazy('subjects'))
        return render(request, 'teachers/subject_form.html', context)


class SubjectEditView(PermissionRequiredMixin, View):
    permission_required = ['main.change_subjects', 'main.view_subjects']

    def get(self, request, pk):
        context = {}
        context['btn'] = "Zmień"
        context['title'] = 'Zmień przedmiot'
        s = Subjects.objects.get(pk=pk)
        name = s.name
        context['name'] = name
        teacher = s.teacher
        context['selected'] = teacher.id
        g = Group.objects.get(name='teachers')
        context['teachers'] = g.user_set.all()
        g = Group.objects.get(name='students')
        context['students'] = g.user_set.all()
        students_id = []
        for student in s.students.all():
            students_id.append(str(student.id))
        context['selected_students'] = students_id
        return render(request, 'teachers/subject_form.html', context)

    def post(self, request, pk):
        context = {}
        context['btn'] = "Zmień"
        context['title'] = 'Zmień przedmiot'
        name = request.POST.get('name')
        context['name'] = name
        teacher = User.objects.get(pk=request.POST.get('teachers'))
        context['selected'] = teacher.id
        g = Group.objects.get(name='teachers')
        context['teachers'] = g.user_set.all()
        g = Group.objects.get(name='students')
        context['students'] = g.user_set.all()
        students_id = request.POST.getlist('students')
        context['selected_students'] = students_id
        if name and teacher and students_id:
            s = Subjects.objects.get(pk=pk)
            s.name = name
            s.teacher = teacher
            s.save()
            s.students.set(students_id)
            return redirect(reverse_lazy('subjects'))
        return render(request, 'teachers/subject_form.html', context)


class SubjectListView(PermissionRequiredMixin, View):
    permission_required = ['main.view_subjects']

    def get(self, request):
        context = {'subjects': Subjects.objects.all(), 'title': "Przedmioty"}
        return render(request, 'teachers/subject_list.html', context)


class GradeAddView(PermissionRequiredMixin, View):
    permission_required = ['main.add_grades']

    def get(self, request):
        context = {}
        context['title'] = 'Dodaj ocenę'
        context['btn'] = 'Dodaj'
        context['subjects'] = Subjects.objects.all()
        g = Group.objects.get(name='students')
        context['students'] = g.user_set.all()
        return render(request, 'teachers/grades_form.html', context)

    def post(self, request):
        context = {}
        context['title'] = 'Dodaj ocenę'
        context['btn'] = 'Dodaj'
        context['subjects'] = Subjects.objects.all()
        g = Group.objects.get(name='students')
        context['students'] = g.user_set.all()
        subject = request.POST.get('subject')
        context['selected_subject'] = subject
        student = request.POST.get('student')
        context['selected_student'] = student
        value = request.POST.get('value')
        context['value'] = value
        if value and student and subject:
            Grades.objects.create(value=value, student_id=student, subject_id=subject, graded_by=request.user)
            return redirect(reverse_lazy('grade_add'))
        return render(request, 'teachers/grades_form.html', context)


class GradeListView(PermissionRequiredMixin, View):
    permission_required = ['main.view_grades']

    def get(self, request):
        context = {}
        context['title'] = "Lista ocen"
        # subjects = [{
        #     'name': "bla",
        #     'students': [{'username': "dad",
        #                  'grades': [{
        #                      'id': 'id',
        #                      'value': 'value'
        #                  }]
        #                   }]
        # }]
        subjects = []
        for subject in Subjects.objects.all():
            subject_ = {}
            students = []
            for student in Group.objects.get(name='students').user_set.all():
                student_ = {}
                student_['username'] = student.username
                grades = []
                for grade in Grades.objects.filter(student_id=student.id, subject_id=subject.id):
                    grade_ = {}
                    grade_['id'] = grade.id
                    grade_['value'] = grade.value
                    grades.append(grade_)
                student_['grades'] = grades
                if student_['grades']:
                    students.append(student_)
            subject_['students'] = students
            subject_['name'] = subject.name
            subjects.append(subject_)
        context['subjects'] = subjects
        return render(request, 'teachers/grades_list.html', context)


class GradeView(PermissionRequiredMixin, View):
    permission_required = ['main.view_grades']

    def get(self, request, pk):
        grade = Grades.objects.get(pk=pk)
        context = {}
        context['value'] = grade.value
        context['student'] = grade.student.username
        context['teachers'] = grade.graded_by.username
        context['subject'] = grade.subject.name
        return render(request, 'teachers/grade_view.html', context)
