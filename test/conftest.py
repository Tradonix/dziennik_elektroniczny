from random import randint, shuffle, choice

from faker.providers.person.en import Provider
from faker import Faker

import pytest

from django.test import Client
from django.contrib.auth.models import User, Permission, Group

from main.models import Messages, Subjects, Grades


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User(username='Qwerty')
    user.set_password('qwerty')
    user.save()
    return user


@pytest.fixture
def groups():
    teacher = Group.objects.create(name='teachers')
    teacher.permissions.set(Permission.objects.filter(id__in=[25, 26, 27, 28, 29, 30, 31, 32]))
    student = Group.objects.create(name='students')
    student.permissions.set(Permission.objects.filter(id__in=[28, 32]))
    return teacher, student


@pytest.fixture
def user_student(groups):
    user_student = User(username='Student')
    user_student.set_password('student')
    user_student.save()
    user_student.groups.set([groups[1]])  # set oczekuje czegoś iterowalnego
    return user_student


@pytest.fixture
def user_teacher(groups):
    user_teacher = User(username='Teacher')
    user_teacher.set_password('teacher')
    user_teacher.save()
    user_teacher.groups.set([groups[0]])  # set oczekuje czegoś iterowalnego
    return user_teacher


@pytest.fixture
def messages(user_student, user):
    messages = []
    fake = Faker('pl_Pl')
    for _ in range(10):
        # faker.sentence zrwazca zdania dluzsze niz 32 znaki (limit pola title modelu Messages)
        # dlatego obcinam do 32 znakow
        messages.append(Messages.objects.create(title=fake.sentence()[:32], message=fake.text,
                                                send_to=user, send_by=user_student))
    return messages


@pytest.fixture
def set_up(groups):
    fake = Faker()
    subjects = []
    teachers = []
    students = []
    grades = []

    first_names = list(set(Provider.first_names))
    shuffle(first_names)
    # robione w taki sposob zeby dostac unikalne wartosci

    for _ in range(2):
        t = User.objects.create(username=first_names.pop())
        t.set_password(fake.password)
        t.save()
        t.groups.set([groups[0]])
        teachers.append(t)
    for _ in range(8):
        student = User.objects.create(username=first_names.pop())
        student.set_password(fake.password)
        student.save()
        student.groups.set([groups[1]])
        students.append(student)
    for _ in range(5):
        # uzywam first_names.pop() bo nie mam lepszego pomyslu i nie ma to znaczenia
        s = Subjects.objects.create(name=first_names.pop(), teacher=choice(teachers))
        s.students.set([choice(students) for _ in range(4)])
        subjects.append(s)
    for _ in range(40):
        subject = choice(subjects)
        grades.append(Grades.objects.create(value=randint(1, 6), subject=subject, graded_by=subject.teacher,
                                            student=choice(subject.students.all())))
    return grades


@pytest.fixture
def grades_as_in_view_student(set_up, user_student):
    # musze tak robic przez sposób w jaki wyświetlam to w widoku
    for subject in Subjects.objects.all():
        for _ in range(randint(1, 5)):
            Grades.objects.create(value=randint(1, 6), subject=subject, graded_by=subject.teacher,
                                  student=user_student)

    subjects = []
    for subject in Subjects.objects.all():
        subject_ = {}
        subject_['name'] = subject.name
        grades = []
        for grade in Grades.objects.filter(student=user_student, subject=subject):
            grades.append(grade.value)
        subject_['grades'] = grades
        subjects.append(subject_)
    return subjects


@pytest.fixture
def grades_as_in_view_teacher(set_up):
    subjects = []
    for subject in Subjects.objects.all():
        subject_ = {}
        students = []
        for student in Group.objects.get(name='students').user_set.all():
            student_ = {}
            student_['username'] = student.username
            student_['grades'] = Grades.objects.filter(student_id=student.id, subject_id=subject.id)
            if student_['grades']:
                students.append(student_)
        subject_['students'] = students
        subject_['name'] = subject.name
        subjects.append(subject_)
    return subjects
