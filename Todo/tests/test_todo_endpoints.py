import pytest

from django.urls import reverse
from django.contrib.auth.models import User

from Todo.models import Todo
from Todo.serializers import TodoSerializer

from rest_framework import status


@pytest.fixture
def create_todo(db):
    """
    Fixture to make a new todo object
    """

    def make_todo(**kwargs):
        return Todo.objects.create(**kwargs)
    return make_todo


@pytest.fixture
def auto_login_user(db, client):
    """
    Fixture to automatically log in a user using JWT authentication
    """

    def make_auto_login():
        # set password
        password = 'johnnyappleseed'
        # create user
        user = User.objects.create_user('johnsmith', 'johnsmith@gmail.com', password)
        # login using JWT authentication
        response = client.post(
                    reverse('token-obtain-pair'),
                    {
                        'username':user.username,
                        'password':password
                    }
                        
                )
        assert response.status_code == status.HTTP_200_OK
        # returns the access token and refresh tokens
        return response.json()['access'], response.json()['refresh']
    return make_auto_login


def test_todo_list(db, client, create_todo, auto_login_user):
    """
    Test that a list of todos are returned when GET request is made to '/api/todos'
    - @param client is a built-in fixture from pytest-django based off of django.test.client /
            which can be used for making requests to the app
    """
    
    # login user
    access_token, refresh_token = auto_login_user()
    # create a Todo object in db
    todo = create_todo(title="Learn how to use pytest", memo="Use the book 'Python Testing with Pytest'")
    # get the url to for getting the todo list
    url = reverse('todo-list')
    # returns the response object from endpoint
    response = client.get(url, headers={"Authorization":"Bearer " + access_token})
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['title'] == todo.title


def test_todo_list_unauthorized(db, client, create_todo):
    """
    Test that an unauthorized can't access the todo list when GET request is made to '/api/todos'
    """
    
    # User NOT logged in
    # create a Todo object in db
    todo = create_todo(title="Learn how to use pytest", memo="Use the book 'Python Testing with Pytest'")
    # get the url to for getting the todo list
    url = reverse('todo-list')
    # returns the response object from endpoint (no access token provided)
    response = client.get(url)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_todo_create(db, client):
    """
    Test that a new object is successfully created when POST request is made to '/api/todos' successfully
    """
    
    # login user
    access_token, refresh_token = auto_login_user()
    # should begin with zero Todo objects
    assert Todo.objects.count() == 0
    # define model values
    title = "Learn how to use pytest"
    memo = "Use the book 'Python Testing with Pytest'"
    # get the url to for creating the todo object
    url = reverse('todo-list')
    # returns the response object from endpoint
    response = client.post(
                            url, 
                            {
                                'title':title, 
                                "memo":memo,
                            },
                            headers={"Authorization":"Bearer " + access_token}
                        )
                            
    assert response.status_code == status.HTTP_201_CREATED
    assert Todo.objects.count() == 1


def test_todo_detail(db, client, create_todo):
    """
    Test that a get request can be made to '/api/todos/<id>' to obtain the detail page of a todo object successfully
    """

    # login user
    access_token, refresh_token = auto_login_user()
    # create todo object in db
    todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'")
    # get url for retrieving detail page for specific blog
    url = reverse('todo-detail', args=(todo.pk,))
    response = client.get(url, headers={"Authorization":"Bearer " + access_token})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == todo.pk


def test_todo_update(db, client, create_todo):
    """
    Test that a PUT request can be made to '/api/todos/<id>' to update a todo object successfully
    """

    # login user
    access_token, refresh_token = auto_login_user()
    # create todo object in db
    todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'")
    # set values to be updated
    new_title = 'Learn how to use pytest with DjangoRestFramework'
    new_memo = "Use the book 'Python Testing with Pytest and other resources'"
    # get url for updating the todo object
    url = reverse('todo-detail', args=(todo.pk,))
    response = client.put(
                        url, 
                        {
                            'title':new_title,
                            'memo':new_memo,
                        },
                        headers={"Authorization":"Bearer " + access_token},
                        content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    updated_todo = TodoSerializer(Todo.objects.get(pk=todo.pk)).data
    assert updated_todo['title'] == new_title
    assert updated_todo['memo'] == new_memo


def test_todo_delete(db, client, create_todo):
    """
    Test that a DELETE request can be made to '/api/todos/<id>' to destroy a todo object successfully
    """

    # login user
    access_token, refresh_token = auto_login_user()
    # create todo object in db
    todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'")
    # assert there are exactly 1 Todo objects
    assert Todo.objects.count() == 1

    # get url for updating the todo object
    url = reverse('todo-detail', args=(todo.pk,))
    # make delete request to '/api/todos/<id>'
    response = client.delete(url, headers={"Authorization":"Bearer " + access_token})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Todo.objects.count() == 0