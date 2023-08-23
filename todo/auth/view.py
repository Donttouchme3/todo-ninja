from ninja import Form, Router, File
from ninja.responses import Response
from ninja_extra import status
from ninja.files import UploadedFile
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.db import IntegrityError
from typing import Optional
from .schemas import UserRegistrationSchema, UserPasswordUpdateSchema, UserUpdateSchema
from .jwt import AuthBearer, create_token
from todo_app.models import CustomUser



router = Router()

@router.post('user/register')
def user_register(request: HttpRequest, data: UserRegistrationSchema = Form(...)):
    try:
        CustomUser.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name
        )
        return Response({"message": "Вы успешно зарегистрировались"}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return {'error': 'Это имя пользователя уже занято'}

@router.post('user/login')
def user_login(request: HttpRequest, username: str = Form(...), password: str = Form(...)):
    user = get_object_or_404(CustomUser, username=username)
    if check_password(password, user.password):
        return create_token(user.id)

@router.post('user/change-password')
def user_change_password(request, data: UserPasswordUpdateSchema):
    user = CustomUser.objects.filter(username=data.username).first()
    try:
        if user.check_password(data.password):
            user.set_password(data.new_password)
            user.save()
            return {'message': 'Пароль успешно изменен'}
        else: return {'error': 'Логин или пароль не верны'}
    except AttributeError:
        return {'error': 'Такого пользователя не существует'}
    
@router.delete('user/delete', auth=AuthBearer(), response={204: None})
def user_delete(request: HttpRequest, ):
    user = get_object_or_404(CustomUser, username=request.auth)
    user.delete()
    return None


@router.post('user/update', auth=AuthBearer(),)
def user_data_update(request: HttpRequest, data: UserUpdateSchema = Form(...), avatar: Optional[UploadedFile] = File(None)):
    user = get_object_or_404(CustomUser, username=request.auth)
    for attr, value in data.dict().items():
        if value is not None:
            setattr(user, attr, value)  
    if avatar:
        user.avatar = avatar
    user.save()
    return {'message': 'Данные успешно обновлены'}



    