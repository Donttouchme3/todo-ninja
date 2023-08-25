from rest_framework.test import APIClient
from todo_app import models as model

client = APIClient()


    
    
def user_register(payload): return client.post('/auth/user/register', data=payload, format='multipart')
def user_login(payload): return client.post('/auth/user/login', data=payload, format='multipart')
def user_change_password(payload): return client.post('/auth/user/change-password', data=payload, format='json')
def user_delete(auth_token): return client.delete('/auth/user/delete', headers=auth_token)
def user_update(auth_token, payload): return client.post('/auth/user/update', headers=auth_token, data=payload)


def task_create(payload, auth_token): return client.post('/api/tasks', data=payload, headers=auth_token, format='json')


def check_required_fields(detail):
    fields = [field.name for field in model.CustomUser._meta.get_fields()]
    checking = []
    for i in detail:      
        checking.append(i["loc"][1] in fields)
    return True if False not in checking else False 

USER_PAYLOAD = {
    'USER_REGISTER': {
        'USER_SUCCESS_REGISTER_PAYLOAD': {"username": "asilbek", "email": "asilbek@icloud.com",
                                          "first_name": "asilbek", "last_name": "shavkatov", "password": "As031001"},
        'USER_FAIL_REGISTER_PAYLOAD': {"username": "asilbek_shavkatov", "email": "asil007bek@icloud.com",}
    },
    'USER_LOGIN': {
        'USER_SUCCESS_LOGIN_PAYLOAD': {'username': 'asilbek', 'password': 'As031001'},
        'USER_FAIL_LOGIN_PAYLOAD': {'username': 'asilbek', 'password': '123'},
    },
    'USER_CHANGE_PASSWORD': {
        'USER_SUCCESS_CHANGE_PASSWORD_PAYLOAD': {'username': 'asilbek', 'password': 'As031001', 'new_password': 'Ma240302'},
        'USER_FAIL_CHANGE_PASSWORD_PAYLOAD': {'username': 'asilbek', 'password': '031001', 'new_password': '12345'},
        'USER_NONEXISTING_USER_PAYLOAD': {'username': 'shavkatov', 'password': '031001', 'new_password': '12345'}
    },
    'USER_UPDATE': {
        'USER_SUCCESS_UPDATE_PAYLOAD': {'first_name': 'Asilbek', 'last_name': 'Shavkatov', 'email': 'asilbek6921@gmail.com', 'avatar': ('1.jpg', open('C:/Users/asil0/OneDrive/Изображения/1.jpg', 'rb'))},
    }
}

TASK_PAYLOAD = {
    'TASK_CREATE_PAYLOAD': {
        "title": "Я добавил таск",
        "description": "test description",
        "end_date": "2023-08-25",
        "status": 'to-do'
    },
}

INVALID_TOKEN = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTI3OTg2MjAsInN1YiI6ImFjY2VzcyJ9.Q6V9xNe5v9ucXD9n4V7ogLszTX0zqOizWPX1WaFYFAd'}