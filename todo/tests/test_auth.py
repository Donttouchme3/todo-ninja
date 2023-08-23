import pytest
from rest_framework import status
from todo_app import models as model
from . import conftests as confs

@pytest.fixture
@pytest.mark.django_db
def create_user():
    user = model.CustomUser.objects.create_user(**confs.USER_REGISTER_PAYLOAD['user_success_register_payload'])
    return user


@pytest.mark.django_db
class TestUserRegister:
    def test_success_user_register(self):
        user_payload = confs.USER_REGISTER_PAYLOAD['user_success_register_payload']
        user_register_response = confs.user_register(user_payload)
        assert user_register_response.status_code == status.HTTP_201_CREATED
        
    def test_fail_user_register(self):
        user_payload = confs.USER_REGISTER_PAYLOAD['user_fail_register_payload']
        user_register_response = confs.user_register(user_payload)
        data = user_register_response.json()
        print(model.CustomUser._meta.get_fields().field)
        
        for i in data['detail']:
            print(f'todo_app.CustomerUser.{i["loc"][1]}')
           
        assert 0 == 0
        


