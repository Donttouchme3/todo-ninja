import pytest
from ninja_extra import status
from todo_app import models as model
from . import conftests as confs

@pytest.fixture
@pytest.mark.django_db
def create_user():
    model.CustomUser.objects.create_user(**confs.USER_PAYLOAD['USER_REGISTER']['USER_SUCCESS_REGISTER_PAYLOAD'])

@pytest.fixture
@pytest.mark.django_db
def login_user(create_user):
    user_payload = confs.USER_PAYLOAD['USER_LOGIN']['USER_SUCCESS_LOGIN_PAYLOAD']
    login_response = confs.user_login(user_payload)
    access_token = login_response.json()['access_token']
    return access_token

@pytest.mark.django_db
class TestUserRegister:
    def test_success_user_register(self):
        user_payload = confs.USER_PAYLOAD['USER_REGISTER']['USER_SUCCESS_REGISTER_PAYLOAD']
        user_register_response = confs.user_register(user_payload)
        assert user_register_response.status_code == status.HTTP_201_CREATED
        
    def test_fail_user_register(self):
        user_payload = confs.USER_PAYLOAD['USER_REGISTER']['USER_FAIL_REGISTER_PAYLOAD']
        user_register_response = confs.user_register(user_payload)
        assert confs.check_required_fields(user_register_response.json()['detail'])
    
    def test_re_registration(self, create_user):
        user_payload = confs.USER_PAYLOAD['USER_REGISTER']['USER_SUCCESS_REGISTER_PAYLOAD']
        user_register_response = confs.user_register(user_payload)
        assert user_register_response.status_code == status.HTTP_200_OK
        assert user_register_response.json()['error'] == 'Это имя пользователя уже занято'
        

@pytest.mark.django_db
class TestUserLogin:
    def test_success_user_login(self, create_user):
        user_payload = confs.USER_PAYLOAD['USER_LOGIN']['USER_SUCCESS_LOGIN_PAYLOAD']
        user_login_response = confs.user_login(user_payload)
        assert user_login_response.status_code == status.HTTP_200_OK
        assert user_login_response.json()['access_token']
        
    def test_fail_user_login(self, create_user):
        user_payload = confs.USER_PAYLOAD['USER_LOGIN']['USER_FAIL_LOGIN_PAYLOAD']
        user_login_response = confs.user_login(user_payload)
        assert user_login_response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_login_response.json()['error']
        
        
@pytest.mark.django_db
class TestUserChangePassword:
    def test_success_user_change_password(self, create_user):
        user_payload = confs.USER_PAYLOAD['USER_CHANGE_PASSWORD']['USER_SUCCESS_CHANGE_PASSWORD_PAYLOAD']
        user_change_password_response = confs.user_change_password(user_payload)
        assert user_change_password_response.status_code == status.HTTP_202_ACCEPTED
    
    def test_fail_user_change_password(self, create_user):
        user_payload = confs.USER_PAYLOAD['USER_CHANGE_PASSWORD']['USER_FAIL_CHANGE_PASSWORD_PAYLOAD']
        user_change_password_response = confs.user_change_password(user_payload)
        assert user_change_password_response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_change_password_response.json()['error'] == 'Логин или пароль не верны'
        
    def test_nonexistent_user_change_password(self, create_user):
        user_payload = confs.USER_PAYLOAD['USER_CHANGE_PASSWORD']['USER_NONEXISTING_USER_PAYLOAD']
        user_change_password_response = confs.user_change_password(user_payload)
        assert user_change_password_response.status_code == status.HTTP_404_NOT_FOUND
        assert user_change_password_response.json()['error'] == 'Такого пользователя не существует'
