import pytest
from ninja_extra import status
from todo_app import models as model
from . import conftests as confs
from jwt.exceptions import InvalidSignatureError, DecodeError


@pytest.fixture
@pytest.mark.django_db
def create_user():
    model.CustomUser.objects.create_user(**confs.USER_PAYLOAD['USER_REGISTER']['USER_SUCCESS_REGISTER_PAYLOAD'])

@pytest.fixture
@pytest.mark.django_db
def auth_token(create_user):
    user_payload = confs.USER_PAYLOAD['USER_LOGIN']['USER_SUCCESS_LOGIN_PAYLOAD']
    login_response = confs.user_login(user_payload)
    access_token = login_response.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}

@pytest.mark.django_db
class TestUserRegister:
    def test_success(self):
        user_payload = confs.USER_PAYLOAD['USER_REGISTER']['USER_SUCCESS_REGISTER_PAYLOAD']
        user_register_response = confs.user_register(user_payload)
        assert user_register_response.status_code == status.HTTP_201_CREATED
        
    def test_fail(self):
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
    def test_success(self, create_user):
        """Тестирование успешного логина"""
        user_payload = confs.USER_PAYLOAD['USER_LOGIN']['USER_SUCCESS_LOGIN_PAYLOAD']
        user_login_response = confs.user_login(user_payload)
        assert user_login_response.status_code == status.HTTP_200_OK
        assert user_login_response.json()['access_token']
        
    def test_fail(self, create_user):
        """Тестирование при не правильном вводе логина или пароля"""
        user_payload = confs.USER_PAYLOAD['USER_LOGIN']['USER_FAIL_LOGIN_PAYLOAD']
        user_login_response = confs.user_login(user_payload)
        assert user_login_response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_login_response.json()['error']
        
    def test_required_fields(self, create_user): 
        """Тестирование для случая где пользователь не ввел какие либо поля"""
        user_payload = {'username': 'asilbek'}
        user_login_response = confs.user_login(user_payload)
        assert confs.check_required_fields(user_login_response.json()['detail'])
        assert user_login_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        
@pytest.mark.django_db
class TestUserChangePassword:
    def test_success(self, create_user):
        """Тестирование успешного изменения пароля"""
        user_payload = confs.USER_PAYLOAD['USER_CHANGE_PASSWORD']['USER_SUCCESS_CHANGE_PASSWORD_PAYLOAD']
        user_change_password_response = confs.user_change_password(user_payload)
        assert user_change_password_response.status_code == status.HTTP_202_ACCEPTED
    
    def test_fail(self, create_user):
        """Тестирование для случая при неправильном логине или пароле"""
        user_payload = confs.USER_PAYLOAD['USER_CHANGE_PASSWORD']['USER_FAIL_CHANGE_PASSWORD_PAYLOAD']
        user_change_password_response = confs.user_change_password(user_payload)
        assert user_change_password_response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_change_password_response.json()['error'] == 'Логин или пароль не верны'
        
    def test_nonexistent_user(self, create_user):
        """Тестирование для случая где пользователя не существует"""
        user_payload = confs.USER_PAYLOAD['USER_CHANGE_PASSWORD']['USER_NONEXISTING_USER_PAYLOAD']
        user_change_password_response = confs.user_change_password(user_payload)
        assert user_change_password_response.status_code == status.HTTP_404_NOT_FOUND
        assert user_change_password_response.json()['error'] == 'Такого пользователя не существует'
    
    def test_required_fields(self, create_user):
        """Тестирование для случая где пользователь не ввел какие либо поля"""
        user_payload = {'username': 'asilbek'}
        user_change_password_response = confs.user_change_password(user_payload)
        for i in user_change_password_response.json()['detail']:
            assert i['loc'][2] in ['username', 'password', 'new_password']
        assert user_change_password_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        
@pytest.mark.django_db
class TestUserDelete:
    def test_success(self, auth_token):
        user_delete_response = confs.user_delete(auth_token)
        assert user_delete_response.status_code == status.HTTP_204_NO_CONTENT
        
    def test_invalid_token(self, auth_token):
        invalid_auth_token = confs.INVALID_TOKEN
        try:
            user_delete_response = confs.user_delete(invalid_auth_token)
        except Exception as _e:
            assert _e.__class__.__name__ == DecodeError or InvalidSignatureError
            

@pytest.mark.django_db
class TestUpdate:
    def test_success(self, auth_token):
        user_payload = confs.USER_PAYLOAD['USER_UPDATE']['USER_SUCCESS_UPDATE_PAYLOAD']
        user_update_response = confs.user_update(auth_token, user_payload)
        assert user_update_response.status_code == status.HTTP_202_ACCEPTED         
            
            
    
    
    

