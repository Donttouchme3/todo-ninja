from rest_framework.test import APIClient
from todo_app import models as model

client = APIClient()


def user_register(payload): return client.post(
    '/auth/user/register', data=payload, format='multipart')


def user_login(payload): return client.post(
    '/auth/user/login', data=payload, format='multipart')


def user_change_password(payload): return client.post(
    '/auth/user/change-password', data=payload, format='json')


def user_delete(auth_token): return client.delete(
    '/auth/user/delete', headers=auth_token)
def user_update(auth_token, payload): return client.post(
    '/auth/user/update', headers=auth_token, data=payload)


def user_data(auth_token): return client.get('/api/user', headers=auth_token)
def task_create(payload, auth_token): return client.post(
    '/api/tasks', data=payload, headers=auth_token, format='json')


def tasks_get(auth_token): return client.get('/api/tasks', headers=auth_token)


def tasks_get_by_filter(auth_token): return client.get(
    '/api/tasks?end_date=2023-08-01', headers=auth_token)


def tasks_get_by_status(auth_token, status): return client.get(
    f'/api/tasks/{status}', headers=auth_token)


def task_get(auth_token, task_id=1): return client.get(
    f'/api/tasks/{task_id}', headers=auth_token)


def task_update(auth_token, payload, task_id=1): return client.patch(
    f'/api/tasks/{task_id}', headers=auth_token, data=payload, format='json')


def task_delete(auth_token, task_id=1): return client.delete(
    f'/api/tasks/{task_id}', headers=auth_token)


def note_create(auth_token, payload): return client.post(
    '/api/notes', headers=auth_token, data=payload, format='multipart')


def note_update(auth_token, payload, note_id): return client.put(
    f'/api/notes/{note_id}', headers=auth_token, data=payload, format='json')


def note_delete(auth_token, note_id): return client.delete(
    f'/api/notes/{note_id}', headers=auth_token)


def check_required_fields(detail):
    fields = [field.name for field in model.CustomUser._meta.get_fields()]
    checking = []
    for i in detail:
        checking.append(i["loc"][1] in fields)
    return True if False not in checking else False


def check_tasK_required_fields(detail):
    fields = [field.name for field in model.Task._meta.get_fields()]
    checking = []
    for i in detail:
        checking.append(i["loc"][2] in fields)
    return True if False not in checking else False


USER_PAYLOAD = {
    'USER_REGISTER': {
        'USER_SUCCESS_REGISTER_PAYLOAD': {"username": "asilbek", "email": "asilbek@icloud.com",
                                          "first_name": "asilbek", "last_name": "shavkatov", "password": "As031001"},
        'USER_FAIL_REGISTER_PAYLOAD': {"username": "asilbek_shavkatov", "email": "asil007bek@icloud.com", }
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
    'TASK_CREATE_PAYLOAD': {"title": "Я добавил таск", "description": "test description", "end_date": "2023-08-25", "status": 'to-do', 'start_date': '2023-08-05'},
    'TASK_UPDATE_PAYLOAD': {'title': 'Я обновил таск', 'description': 'Я обновил description таска ', 'status': 'done'}
}

NOTE_PAYLOAD = {
    'NOTE_CREATE_PAYLOAD': {'task': 1, 'text': 'Я добавил заметку'},
    'NOTE_UPDATE_PAYLOAD': {'text': 'Я обновил заметку'}
}

INVALID_TOKEN = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTI3OTg2MjAsInN1YiI6ImFjY2VzcyJ9.Q6V9xNe5v9ucXD9n4V7ogLszTX0zqOizWPX1WaFYFAd'}
