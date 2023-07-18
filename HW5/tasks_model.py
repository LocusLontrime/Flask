from typing import List
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class TaskModel(BaseModel):
    id: int
    name: str
    description: str = None
    status: str


class Task(BaseModel):
    name: str
    description: str = None
    status: str


tasks: list[TaskModel] = []


@app.get('/tasks', response_model=List[Task])
async def get_tasks():
    if tasks:
        return tasks
    return {'message': 'Tasks are not found'}


@app.get('/tasks/{id_task}', response_model=Task)
async def get_task(id_task: int):
    res = [t for t in tasks if t.id == id_task][0]
    if res:
        return res


@app.post('/new_task')
async def set_task(task: Task):
    if tasks:
        new_id = max(tasks, key=lambda x: x.id).id + 1
    else:
        new_id = 1
    new_task = TaskModel(id=new_id, name=task.name, description=task.description, status=task.status)
    tasks.append(new_task)


@app.delete('/del_task/{id_task}')
async def del_task(id_task: int):
    task_ = [t for t in tasks if t.id == id_task][0]
    tasks.remove(task_)
