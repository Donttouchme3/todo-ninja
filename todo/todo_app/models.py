from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from .utils import get_status
from datetime import date

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username
    
    
class Task(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='user_task')
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    description = models.TextField(verbose_name='Описание')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    status = models.CharField(verbose_name='Статус', choices=get_status(), default='to-do', max_length=50)
    
    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        
        
class Notes(models.Model):
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.CASCADE, related_name='task_notes')
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='user_notes')
    text = models.TextField(verbose_name='Текст')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'Заметки пользователя {self.user}'
    
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'