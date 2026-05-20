from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime

from api.database import get_db
from api.models.job import Job
from api.schemas.job import JobResponse, JobCreate, JobUpdate

router = APIRouter(prefix="/jobs", tags=["Bot Jobs"])

@router.get("/", response_model=List[JobResponse])
async def list_jobs(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Lista o histórico e os jobs atuais dos robôs"""
    query = select(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/trigger", response_model=JobResponse)
async def trigger_bot(job_in: JobCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Dispara um robô de scraping/RPA manualmente (roda em background)"""
    new_job = Job(
        bot_name=job_in.bot_name,
        parameters=job_in.parameters,
        status="pending"
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    
    # Aqui vamos chamar a função que inicia o robô em background
    # background_tasks.add_task(run_bot_task, new_job.id, job_in.bot_name, job_in.parameters)
    
    return new_job

@router.get("/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: int, db: AsyncSession = Depends(get_db)):
    """Consulta o status de um job específico"""
    query = select(Job).filter(Job.id == job_id)
    result = await db.execute(query)
    job = result.scalars().first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
        
    return job
