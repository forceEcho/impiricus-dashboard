from typing import Any
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import  select

from app.api.deps import SessionDep
from app.models import Physician, PhysicianCreate, PhysicianPublic, PhysiciansPublic

router = APIRouter(prefix="/physicians")


@router.get("/", response_model=PhysiciansPublic)
async def read_physicians(
    session: SessionDep,
    state: Annotated[str | None, Query(max_length=2)] = None, 
    specialty: Annotated[str | None, Query(max_length=50)] = None
) -> Any:
    """
    Retrieve physicians.
    """
    statement = select(Physician)
    if state:
        statement=statement.where(Physician.state==state)
    if specialty:
        statement=statement.where(Physician.specialty==specialty)
    physicians = session.exec(statement).all()
    
    physicians_public = [PhysicianPublic.model_validate(p) for p in physicians]

    return PhysiciansPublic(data=physicians_public, count=len(physicians))


@router.get("/{id}", response_model=Physician)
async def read_physician(session: SessionDep, id: int) -> Any:
    """
    Get physician by ID.
    """
    physician = session.get(Physician, Physician.physician_id)
    if not physician:
        raise HTTPException(status_code=404, detail="Physician not found")
    return physician

#not needed but wanted to test

@router.post("/", response_model=PhysicianPublic)
def create_physician(
    *, session: SessionDep, phys_in: PhysicianCreate
) -> Any:
    
    physician = Physician.model_validate(phys_in)
    session.add(physician)
    session.commit()
    session.refresh(physician)
    return physician