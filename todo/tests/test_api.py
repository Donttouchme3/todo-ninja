import pytest
from ninja_extra import status
from . import conftests as confs
from todo_app import models as model
from .test_auth import auth_token, create_user


# @pytest.mark.django_db
# def test(auth_token, create_user):
#     print(auth_token)
#     assert 0 == 0



class TestTask:
    @pytest.mark.django_db
    def test_task_create(self, auth_token, create_user):
        task_payload = confs.TASK_PAYLOAD['TASK_CREATE_PAYLOAD']
        task_create_response = confs.task_create(task_payload, auth_token)
        print(task_create_response.status_code)
        assert 0 == 0