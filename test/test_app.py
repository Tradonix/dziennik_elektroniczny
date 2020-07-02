import pytest


@pytest.mark.django_db
def test_main(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_msg(client, user, messages):
    client.login(username='Qwerty', password='qwerty')
    response = client.get('/messages/')

    assert response.status_code == 200

    assert len(response.context['messages']) == 10

    for i in range(len(messages)):
        assert messages[i] in response.context['messages']


@pytest.mark.django_db
def test_student_grades(client, grades_as_in_view_student, user_student):
    client.login(username='Student', password='student')
    response = client.get('/students/grades/')

    assert response.status_code == 200

    assert len(response.context['subjects']) == len(grades_as_in_view_student)

    for i in range(len(grades_as_in_view_student)):
        assert grades_as_in_view_student[i] in response.context['subjects']


@pytest.mark.django_db
def test_teacher_grades(client, grades_as_in_view_teacher, user_teacher):
    client.login(username='Teacher', password='teacher')
    response = client.get('/teachers/grades/')

    assert response.status_code == 200

    assert len(response.context['subjects']) == len(grades_as_in_view_teacher)

    # for i in range(len(grades_as_in_view_teacher)):
    #     for element in grades_as_in_view_teacher[i]:
    #         assert element in response.context['subjects'][i]

    for i, subject in enumerate(grades_as_in_view_teacher):
        for element in subject:
            assert element in response.context['subjects'][i]
