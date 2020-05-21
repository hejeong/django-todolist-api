import pytest

from Todo.models import Todo


@pytest.mark.django_db
def test_todo_create():
    """ 
    Test a Todo object can be created successfully 
    """

    todo = Todo.objects.create(
        title="Learn how to use pytest",
        memo="Use the book 'Python Testing with Pytest'",
    )
    assert Todo.objects.count() == 1

@pytest.mark.django_db
def test_todo_create_without_memo():
    """
    Test creating a Todo object can be created successfully without a memo
    """

    Todo.objects.create(
        title="Learn how to use pytest"
    )
    assert Todo.objects.count() == 1