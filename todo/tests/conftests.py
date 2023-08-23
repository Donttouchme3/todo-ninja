from rest_framework.test import APIClient
import requests
client = APIClient()


    
    
def user_register(payload): 
    return client.post('/auth/user/register', data=payload, format='multipart')


USER_REGISTER_PAYLOAD = {
    'user_success_register_payload': {
        "username": "asilbek",
        "email": "asilbek@icloud.com",
        "first_name": "asilbek",
        "last_name": "shavkatov",
        "password": "As031001"
    },
    'user_fail_register_payload': {
        "username": "asilbek_shavkatov",
        "email": "asil007bek@icloud.com",
        # "password": "As031001"
    },
    'user_register_required_field': ['first_name', 'last_name']
}