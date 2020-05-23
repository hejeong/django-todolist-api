import pytest

from Todo.models import Todo
from Todo.tests.test_todo_endpoints import auto_login_user

@pytest.mark.django_db
def test_todo_create(auto_login_user):
    """ 
    Test a Todo object can be created successfully 
    """

    # login user
    user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
    todo = Todo.objects.create(
        title="Learn how to use pytest",
        memo="Use the book 'Python Testing with Pytest'",
        owner=user,
    )
    assert Todo.objects.count() == 1

@pytest.mark.django_db
def test_todo_create_without_memo(auto_login_user):
    """
    Test creating a Todo object can be created successfully without a memo
    """

    # login user
    user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
    Todo.objects.create(
        title="Learn how to use pytest",
        owner=user,
    )
    assert Todo.objects.count() == 1    