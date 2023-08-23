from ninja import Schema, FilterSchema
from datetime import date
from typing import Optional, List

class NotesSchemaIn(Schema):
    task: int
    text: str
    parent: Optional[int]
    
class NotesUpdateSchemaIn(Schema):
    text: str
    
class NotesBaseSchemaOut(Schema):
    pk: int
    task_id: int
    text: str

    
class NotesSchemaOut(NotesBaseSchemaOut):
    parent: NotesBaseSchemaOut = None
    
class TaskSchemaIn(Schema):
    title: str
    description: str
    start_date: date = date.today()
    end_date: date = date.today()
    status: str

class TaskSchemaOut(Schema):
    pk: int
    title: str
    description: str
    start_date: date
    end_date: date
    status: str
    notes: List[NotesSchemaOut] = None
    
    @staticmethod
    def resolve_notes(obj):
        return obj.task_notes
    

class TasksSchemaOut(Schema):
    pk: int
    title: str
    start_date: date
    end_date: date
    status: str
    
class TaskFIlterSchema(FilterSchema):
    start_date: Optional[date]
    end_date: Optional[date]

class TaskPatchSchemaIn(Schema):
    title: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    status: Optional[str]
    
class UserSchemaOut(Schema):
    avatar: str
    first_name: str
    last_name: str
    email: str
    username: str
    
    @staticmethod
    def resolve_avatar(obj):
        if not obj.avatar:
            return 'https://img.freepik.com/premium-vector/photo-coming-soon_77760-116.jpg?w=2000'
        else: return obj.avatar
        

