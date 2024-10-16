from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app import crud, models
from app.database import engine, get_db
from app.dtos.tasks import TaskCreateDTO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

@app.post("/task")
async def create_task(task: TaskCreateDTO, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_task(db, task.title, task.description, task.deadline_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks")
async def read_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks(db)
    return tasks

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreateDTO, db: AsyncSession = Depends(get_db)):
    try:
       return await crud.update_task(db, task_id, task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


