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
        get_tasks_response = confs.tasks_get(auth_token)
        for field in get_tasks_response.json()[0]:
            assert field in [field.name for field in model.Task._meta.get_fields()]
            
        get_tasks_by_filter_response = confs.tasks_get_by_filter(auth_token=auth_token)
        assert len(get_tasks_by_filter_response.json()) == 0
        assert get_tasks_by_filter_response.status_code == status.HTTP_200_OK
        
        get_tasks_by_status_response = confs.tasks_get_by_status(auth_token, 'to-do')
        try:
            assert 'id' in get_tasks_by_status_response.json()[0]
            assert get_tasks_by_status_response.status_code == status.HTTP_200_OK
        except:
            assert get_tasks_by_status_response.json()['detail'] == 'Not Found'
            assert get_tasks_by_status_response.status_code == status.HTTP_404_NOT_FOUND
            
    
    @pytest.mark.django_db
    def test_get_task(self, create_task, auth_token):
        get_task_response = confs.task_get(auth_token)
        assert 'id' in get_task_response.json() or get_task_response.json()['detail'] == 'Not Found'
        assert get_task_response.status_code == status.HTTP_200_OK or get_task_response.status_code == status.HTTP_404_NOT_FOUND

        
class TestUpdateDeleteTask:
    @pytest.mark.django_db
    def test_update_task(self, auth_token, create_task):
        task_update_payload = confs.TASK_PAYLOAD['TASK_UPDATE_PAYLOAD']
        task_update_response = confs.task_update(auth_token, task_update_payload, 1)
        
        try:
            for i in task_update_payload.values():
                assert i in task_update_response.json().values()
            assert task_update_response.status_code == status.HTTP_200_OK
        except:
            assert task_update_response.json()['detail'] == 'Not Found'
            assert task_update_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_task(self, auth_token, create_task):
        task_delete_response = confs.task_delete(auth_token, 2)
        try:
            assert task_delete_response.status_code == status.HTTP_204_NO_CONTENT
        except:
            assert task_delete_response.json()['detail'] == 'Not Found'
            assert task_delete_response.status_code == status.HTTP_404_NOT_FOUND

        
        
    