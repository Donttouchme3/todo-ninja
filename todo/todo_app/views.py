from ninja import Router, Form
from django.http import HttpRequest, HttpResponse
from auth.jwt import AuthBearer
from . import models, schemas
from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from datetime import date
from ninja import Query

router = Router()

@router.post('/tasks', response=schemas.TaskSchemaOut,auth=AuthBearer())
def create_tasks(request: HttpRequest, payload: schemas.TaskSchemaIn):
    create_task = models.Task.objects.create(**payload.dict(), user=request.auth)
    return create_task

@router.get('/tasks', response=List[schemas.TasksSchemaOut], auth=AuthBearer())
def get_tasks(request: HttpRequest, filters: schemas.TaskFIlterSchema = Query(...)):
    tasks = models.Task.objects.filter(user=request.auth)
    if filters.start_date:
        tasks = tasks.filter(start_date__gte=filters.start_date)
    if filters.end_date:
        tasks = tasks.filter(end_date__lte=filters.end_date)
    return tasks

@router.get('/tasks/{int:task_id}', response=schemas.TaskSchemaOut, auth=AuthBearer())
def get_task(request: HttpRequest, task_id: int):
    task = get_object_or_404(models.Task, user=request.auth, id=task_id)
    return task
            
@router.api_operation(['PUT', 'PATCH'],'/tasks/{int:task_id}', response=schemas.TaskSchemaOut, auth=AuthBearer())
def update_task(request:HttpRequest, payload: schemas.TaskPatchSchemaIn, task_id: int):
    task = get_object_or_404(models.Task, id=task_id, user=request.auth)
    if request.method == 'PUT': payload_schema = schemas.TaskSchemaIn
    else: payload_schema = schemas.TaskPatchSchemaIn
    payload_instance = payload_schema(**payload.dict())
    for attr, value in payload_instance.dict().items():
        if value is not None:
            setattr(task, attr, value)
    task.save()
    return task

@router.delete('/tasks/{int:task_id}', response={status.HTTP_204_NO_CONTENT: None}, auth=AuthBearer())
def delete_task(request: HttpRequest, task_id: int):
    task = get_object_or_404(models.Task, id=task_id, user=request.auth)
    task.delete()
    return None
    
@router.get('/tasks/{str:status}', response=List[schemas.TasksSchemaOut], auth=AuthBearer())
def get_task_by_status(request: HttpRequest, status: str):
    if status == 'expired': task = get_list_or_404(models.Task, user=request.auth, end_date__lt=date.today())
    else: task = get_list_or_404(models.Task, user=request.auth, status=status)
    return task

@router.get('/user', auth=AuthBearer(), response=schemas.UserSchemaOut)
def user_data(request: HttpRequest):
    user = get_object_or_404(models.CustomUser, username=request.auth)
    return user

@router.post('/notes', auth=AuthBearer(), response=schemas.NotesSchemaOut)
def create_notes(request: HttpRequest, data: schemas.NotesSchemaIn = Form(...)):
    note = models.Notes.objects.create(user=request.auth, task_id=data.task, text=data.text, parent_id=data.parent)
    return note

@router.put('/notes/{int:note_id}', auth=AuthBearer(), response=schemas.NotesSchemaOut)
def update_notes(request: HttpRequest, note_id: int, data: schemas.NotesUpdateSchemaIn ):
    note = models.Notes.objects.filter(user=request.auth, pk=note_id).first()
    note.text = data.text
    note.save()
    return note

@router.delete('/notes/{int:note_id}', auth=AuthBearer(), response={status.HTTP_204_NO_CONTENT: None})
def delete_note(request: HttpRequest, note_id: int):
    note = get_object_or_404(models.Notes, user=request.auth, pk=note_id).delete()
    return None    

