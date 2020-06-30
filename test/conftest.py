import pytest
from django.test import Client
from django.contrib.auth.models import User, Permission


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
