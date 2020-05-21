import pytest

from django.urls import reverse
from Todo.models import Todo


@pytest.mark.django_db
def test_todo_list(client):
    """
    Test that a list of todos are returned when GET request is made to '/api/todos'
    - @param client is a built-in fixture from pytest-django based off of django.test.client /
            which can be used for making requests to the app
    """
    
    # create a Todo object in db
    Todo.objects.create(
        title="Learn how to use pytest",
        memo="Use the book 'Python Testing with Pytest'",
    )
    # get the url to for getting the todo list
    url = reverse('todo-list-or-create')
    # returns the response object from endpoint
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()[0]['title'] == "Learn how to use pytest"


@pytest.mark.django_db
def test_todo_list(client):
    """
    Test that a new object is successfully created when POST request is made to '/api/todos'
    """
    
    # should begin with zero Todo objects
    assert Todo.objects.count() == 0
    # define model values
    title = "Learn how to use pytest"
    memo = "Use the book 'Python Testing with Pytest'"
    # get the url to for getting the todo list
    url = reverse('todo-list-or-create')
    # returns the response object from endpoint
    response = client.post(
                            url, 
                            {
                                'title':title, 
                                "memo":memo,
                            })
    assert response.status_code == 200
    assert Todo.objects.count() == 1
    assert Todo.objects.all()[0]['title'] == title
    assert Todo.objects.all()[0]['memo'] == memo