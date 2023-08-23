from django.contrib import admin
from .models import CustomUser, Task, Notes

@admin.register(CustomUser)
class AdminCustomUserView(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')


@admin.register(Task)
class AdminTasksView(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'start_date', 'end_date', 'status')
    

@admin.register(Notes)
class AdminNotesView(admin.ModelAdmin):
    list_display = ('id', 'user', 'task')
    list_filter = ('user', 'task')