from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel


app = FastAPI()


class Task(BaseModel):
    title: str
    description: Optional[str]
    is_completed: bool


tasks: List[Task] = []


@app.get("/tasks")
async def read_tasks():
    if tasks:
        return tasks
    return {'message': 'sorry, empty'}


@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    return tasks[task_id]


@app.post("/tasks/")
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.put('/tasks/{task_id}')
async def update_task(task_id: int, task: Task):
    tasks[task_id] = task
    return {'task_id': task_id, 'task': task}


@app.delete('/tasks/{task_id}')
async def delete_task(item_id: int):
    tasks.pop(item_id)
    return {'item_id': item_id}
