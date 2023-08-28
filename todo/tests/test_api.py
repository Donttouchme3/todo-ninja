import pytest
from ninja_extra import status
from . import conftests as confs
from todo_app import models as model
from .test_auth import auth_token, create_user


@pytest.fixture
@pytest.mark.django_db
def create_task(create_user):
    user = create_user
    task_payload = confs.TASK_PAYLOAD['TASK_CREATE_PAYLOAD']
    task_payload['user'] = user
    task = model.Task.objects.create(**task_payload)
    return task

class TestToken:
    @classmethod
    def setup_class(cls):
        cls.task_payload = confs.TASK_PAYLOAD['TASK_CREATE_PAYLOAD']
        cls.invalid_token = confs.INVALID_TOKEN
        
    @pytest.mark.django_db
    def test_invalid_auth_token(self, auth_token):
        task_create_response  = confs.task_create(self.task_payload, None)
        assert task_create_response.json()['detail'] == 'Unauthorized'
        assert task_create_response.status_code == status.HTTP_401_UNAUTHORIZED
        
        task_create_response = confs.task_create(self.task_payload, self.invalid_token)
        assert task_create_response.json()['detail'] == 'Unauthorized'
        assert task_create_response.status_code == status.HTTP_401_UNAUTHORIZED

class TestTaskCreate:
    @classmethod
    def setup_class(cls):
        cls.task_payload = confs.TASK_PAYLOAD['TASK_CREATE_PAYLOAD']
        cls.invalid_token = confs.INVALID_TOKEN
        
    @pytest.mark.django_db
    def test_task_create(self, auth_token):
        task_create_response = confs.task_create(self.task_payload, auth_token)
        for i in self.task_payload.values():
            assert i in task_create_response.json().values()
        assert task_create_response.status_code == status.HTTP_200_OK
        
    @pytest.mark.django_db
    def test_task_create_required_fields(self, auth_token):
        task_create_response = confs.task_create({"status": 'to-do'}, auth_token)
        assert confs.check_tasK_required_fields(task_create_response.json()['detail'])
        assert task_create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        

class TestGetTask:
    @pytest.mark.django_db
    def test_get_tasks(self, create_task, auth_token):
        get_tasks_response = confs.get_tasks(auth_token)
        for field in get_tasks_response.json()[0]:
            assert field in [field.name for field in model.Task._meta.get_fields()]
        assert get_tasks_response.status_code == status.HTTP_200_OK
    
    @pytest.mark.django_db
    def test_get_task(self, create_task, auth_token):
        get_task_response = confs.get_task(auth_token)
        
        assert 'id' in get_task_response.json()
        assert get_task_response.status_code == status.HTTP_200_OK


        



        
        
    