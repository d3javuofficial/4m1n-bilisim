from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RequirementCreate(BaseModel):
    field: str
    operator: str
    value: str
    unit: Optional[str] = None
    mandatory: bool = True

class TenderItemCreate(BaseModel):
    item_no: int
    description: str
    quantity: float
    unit: str = "adet"
    requirements: List[RequirementCreate] = []

class TenderCreate(BaseModel):
    tender_number: str
    title: str
    institution: str
    submission_deadline: Optional[datetime] = None
    items: List[TenderItemCreate] = []