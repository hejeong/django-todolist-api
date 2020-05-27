import pytest

from django.urls import reverse
from django.contrib.auth.models import User

from Todo.models import Todo
from Todo.serializers import TodoSerializer

from rest_framework import status


# --- Fixtures ---
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

    def make_auto_login(**kwargs):
        # set password
        password = 'johnnyappleseed'
        # create user
        user = User.objects.create_user(kwargs['username'], kwargs['email'], password)
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
        return user, response.json()['access'], response.json()['refresh']
    return make_auto_login


# --- Protected Actions (Authenticated) ---
class TestTodoAuthorized:
    def test_todo_list(self, db, client, create_todo, auto_login_user):
        """
        Test that a list of todos are returned when GET request is made to '/api/todos'
        - @param client is a built-in fixture from pytest-django based off of django.test.client /
                which can be used for making requests to the app
        """
        
        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create a Todo object in db
        todo = create_todo(title="Learn how to use pytest", memo="Use the book 'Python Testing with Pytest'", owner=user)
        # get the url to for getting the todo list
        url = reverse('todo-list')
        # add access token to request headers
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        # returns the response object from endpoint
        response = client.get(url, **headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['title'] == todo.title


    def test_todo_create(self, db, client, auto_login_user):
        """
        Test that a new object is successfully created when POST request is made to '/api/todos' successfully
        """
        
        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # should begin with zero Todo objects
        assert Todo.objects.count() == 0
        # define model values
        title = "Learn how to use pytest"
        memo = "Use the book 'Python Testing with Pytest'"
        # get the url to for creating the todo object
        url = reverse('todo-list')
        # add access token to request headers
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        # returns the response object from endpoint
        response = client.post(
                                url, 
                                {
                                    'title':title, 
                                    "memo":memo,
                                },
                                **headers
                            )
                                
        assert response.status_code == status.HTTP_201_CREATED
        assert Todo.objects.count() == 1


    def test_todo_detail(self, db, client, create_todo, auto_login_user):
        """
        Test that a get request can be made to '/api/todos/<id>' to obtain the detail page of a todo object successfully
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
        # get url for retrieving detail page for specific blog
        url = reverse('todo-detail', args=(todo.pk,))
        # add access token to request headers
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        response = client.get(url, **headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == todo.pk


    def test_todo_update(self, db, client, create_todo, auto_login_user):
        """
        Test that a PUT request can be made to '/api/todos/<id>' to update a todo object successfully
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
        # set values to be updated
        new_title = 'Learn how to use pytest with DjangoRestFramework'
        new_memo = "Use the book 'Python Testing with Pytest and other resources'"
        # get url for updating the todo object
        url = reverse('todo-detail', args=(todo.pk,))
        # add access token to request headers
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        response = client.put(
                            url, 
                            {
                                'title':new_title,
                                'memo':new_memo,
                            },
                            **headers,
                            content_type="application/json")
        assert response.status_code == status.HTTP_200_OK

        updated_todo = TodoSerializer(Todo.objects.get(pk=todo.pk)).data
        assert updated_todo['title'] == new_title
        assert updated_todo['memo'] == new_memo


    def test_todo_delete(self, db, client, create_todo, auto_login_user):
        """
        Test that a DELETE request can be made to '/api/todos/<id>' to destroy a todo object successfully
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
        # assert there are exactly 1 Todo objects
        assert Todo.objects.count() == 1

        # get url for updating the todo object
        url = reverse('todo-detail', args=(todo.pk,))
        # add access token to request headers
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        # make delete request to '/api/todos/<id>'
        response = client.delete(url, **headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Todo.objects.count() == 0


# --- Protected Actions (Not Authenticated) ---
class TestTodoUnauthorized:
    def test_todo_list_unauth(self, db, client, create_todo, auto_login_user):
        """
        Test that unauthorized users are rejected when GET request is made to '/api/todos'
        """
        
        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create a Todo object in db
        todo = create_todo(title="Learn how to use pytest", memo="Use the book 'Python Testing with Pytest'", owner=user)
        # get the url to for getting the todo list
        url = reverse('todo-list')
        # returns the response object from endpoint
        response = client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_todo_create_unauth(self, db, client, auto_login_user):
        """
        Test that unauthorized users are rejected when POST request is made to '/api/todos'
        """
        
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
                                })
                    
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_todo_detail_unauth(self, db, client, create_todo, auto_login_user):
        """
        Test that an unauthorized user is rejected when a get request is made to '/api/todos/<id>' to obtain the detail page of a todo object
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
        # get url for retrieving detail page for specific blog
        url = reverse('todo-detail', args=(todo.pk,))
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_todo_update_unauth(self, db, client, create_todo, auto_login_user):
        """
        Test that an authorized user is rejected when a PUT request is made to '/api/todos/<id>' to update a todo object
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
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
                            content_type="application/json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_todo_delete_unauth(self, db, client, create_todo, auto_login_user):
        """
        Test that an unauthorized user is rejected when a DELETE request is made to '/api/todos/<id>' to destroy a todo object
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
        # assert there are exactly 1 Todo objects
        assert Todo.objects.count() == 1

        # get url for updating the todo object
        url = reverse('todo-detail', args=(todo.pk,))
        # make delete request to '/api/todos/<id>'
        response = client.delete(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # --- Owner Checks ---
    def test_todo_list_owner(self, db, client, create_todo, auto_login_user):
        """
        Test that the list of todos returned when GET request is made to '/api/todos' contains only todos owned by current user
        """
        
        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create a Todo object in db made by current user
        todo = create_todo(title="Learn how to use pytest", memo="Use the book 'Python Testing with Pytest'", owner=user)
        # create second user
        user2, access_token2, refresh_token2 = auto_login_user(username='johndoe', email='johndoe@gmail.com')
        # create second Todo object made by user #2
        todo2 = create_todo(title="Learn how to use Ant.design", owner=user2)
        # get the url to for getting the todo list
        url = reverse('todo-list')
        # add access token to request headers
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token,
        }
        # returns the response object from endpoint
        response = client.get(url, **headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == todo.id


    def test_todo_update_owner(self, db, client, create_todo, auto_login_user):
        """
        Test that a PUT request made to '/api/todos/<id>' is rejected if it is not the owner
        """

        # login user
        user, access_token, refresh_token = auto_login_user(username='johnsmith', email='johnsmith@gmail.com')
        # create todo object in db
        todo = create_todo(title='Learn how to use pytest', memo="Use the book 'Python Testing with Pytest'", owner=user)
        # login second user
        user2, access_token2, refresh_token2 = auto_login_user(username='johndoe', email='johndoe@gmail.com')
        # set values to be updated
        new_title = 'Learn how to use pytest with DjangoRestFramework'
        new_memo = "Use the book 'Python Testing with Pytest and other resources'"
        # get url for updating the todo object
        url = reverse('todo-detail', args=(todo.pk,))
        # attempt to make update request using the token of second user (who isn't the owner)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token2,
        }
        response = client.put(
                            url, 
                            {
                                'title':new_title,
                                'memo':new_memo,
                            },
                            **headers,
                            content_type="application/json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

