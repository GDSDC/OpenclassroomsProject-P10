from django.test import TestCase
from rest_framework.test import APIClient

client = APIClient()


# Create your tests here.
def test_register():
    request = {
        'email': 'email@truc.fr',
        'password1': '11111',
        'password2': '11111',
        'first_name': 'First',
        'last_name': 'Last'
    }
    response = client.post('/signup', request, format='json')

    assert response.status_code == 201
    # TODO test the response
    print(response.data)

