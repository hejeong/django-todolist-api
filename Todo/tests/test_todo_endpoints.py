import pytest

from django.urls import reverse

from Todo.models import Todo

from rest_framework import status


@pytest.fixture
def create_todo(db):
    """
    Fixture to make a new todo object
    """

    def make_todo(**kwargs):
        return Todo.objects.create(**kwargs)
    return make_todo


def test_todo_list(db, client, create_todo):
    """
    Test that a list of todos are returned when GET request is made to '/api/todos'
    - @param client is a built-in fixture from pytest-django based off of django.test.client /
            which can be used for making requests to the app
    """
    
    # create a Todo object in db
    todo = create_todo(title="Learn how to use pytest", memo="Use the book 'Python Testing with Pytest'")
    
    # get the url to for getting the todo list
    url = reverse('todo-list-or-create')
    # returns the response object from endpoint
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['title'] == todo.title


def test_todo_create(db, client):
    """
    Test that a new object is successfully created when POST request is made to '/api/todos' successfully
    """
    
    # should begin with zero Todo objects
    assert Todo.objects.count() == 0
    # define model values
    title = "Learn how to use pytest"
    memo = "Use the book 'Python Testing with Pytest'"
    # get the url to for creating the todo object
    url = reverse('todo-list-or-create')
    # returns the response object from endpoint
    response = client.post(
                            url, 
                            {
                                'title':title, 
                                "memo":memo,
                            })
                            
    assert response.status_code == status.HTTP_201_CREATED
    assert Todo.objects.count() == 1
    assert Todo.objects.all()[0]['title'] == title
    assert Todo.objects.all()[0]['memo'] == memo


def test_todo_detail(db, client, create_todo):
    """
    Test that a get request can be made to '/api/todos/<id>' to obtain the detail page of a todo object successfully
    """

    # create todo object in db
    todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'")
    # get url for retrieving detail page for specific blog
    url = reverse('todo-detail-get-update-delete', args=(todo.pk,))
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == todo.pk


def test_todo_update(db, client, create_todo):
    """
    Test that a PUT request can be made to '/api/todos/<id>' to update a todo object successfully
    """

    # create todo object in db
    todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'")
    # set values to be updated
    new_title = 'Learn how to use pytest with DjangoRestFramework'
    new_memo = "Use the book 'Python Testing with Pytest and other resources'"
    # get url for updating the todo object
    url = reverse('todo-detail-get-update-delete', args=(todo.pk,))
    response = client.put(
                        url, 
                        {
                            'title':new_title,
                            'memo':new_memo,
                        })
    assert response.status_code == status.HTTP_202_ACCEPTED

    updated_todo = Todo.objects.get(pk=todo.pk)
    assert updated_todo.title == new_title
    assert updated_todo.memo == new_memo


def test_todo_delete(db, client, create_todo):
    """
    Test that a DELETE request can be made to '/api/todos/<id>' to destroy a todo object successfully
    """

    # create todo object in db
    todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'")
    # assert there are exactly 1 Todo objects
    assert Todo.objects.count() == 1

    # get url for updating the todo object
    url = reverse('todo-detail-get-update-delete', args=(todo.pk,))
    # make delete request to '/api/todos/<id>'
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Todo.objects.count() == 0