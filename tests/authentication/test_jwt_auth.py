import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status


def test_jwt_login_authorized(db, client):
    """
    Tests if both an access token and refresh token are generated when a user logs in successfully
    """
    
    # create password value (stored in variable because user.password is encrypted)
    password = 'johnnyappleseed'
    # create a new user
    user = User.objects.create_user('johnsmith', 'jsmith@gmail.com', password)
    # assert that only one user exists currently
    assert User.objects.count() == 1
    
    # get url for issuing new token
    url = reverse('token-obtain-pair')
    # make POST request to 'api/token' with username and password
    response = client.post(
                            url,
                            {
                                'username':user.username,
                                'password':password
                            },
                            content_type='application/json'
                        )
    assert response.status_code == status.HTTP_200_OK


def test_jwt_login_unauthorized(db, client):
    """
    Tests that no tokens are generated when a users credentials are incorrect
    """

     # create password value (stored in variable because user.password is encrypted)
    password = 'johnnyappleseed'
    wrong_password = 'Johnnyappleseed'
    # create a new user
    user = User.objects.create_user('johnsmith', 'jsmith@gmail.com', password)
    # assert that only one user exists currently
    assert User.objects.count() == 1
    
    # get url for issuing new token
    url = reverse('token-obtain-pair')
    # make POST request to 'api/token' with username and password
    response = client.post(
                            url,
                            {
                                'username':user.username,
                                'password':wrong_password
                            },
                            content_type='application/json'
                        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED