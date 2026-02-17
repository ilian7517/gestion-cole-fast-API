from pydantic import BaseModel, Field

class ClassCreate(BaseModel):
    name: str = Field(..., min_length=1)

class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
