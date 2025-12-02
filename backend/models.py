"""
Pydantic Models
Data validation schemas for API requests and responses
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# Animal Models
class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: int = Field(..., gt=0)
    gender: str
    status: str = "Available"
    intake_date: Optional[str] = None  # YYYY-MM-DD format
    behavioral_notes: Optional[str] = None


class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[str] = None
    status: Optional[str] = None
    intake_date: Optional[str] = None
    behavioral_notes: Optional[str] = None


class AnimalResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='_id', serialization_alias='_id')
    name: str
    species: str
    breed: Optional[str] = None
    age: int
    gender: str
    status: str
    intake_date: Optional[str] = None
    behavioral_notes: Optional[str] = None
    assigned_volunteers: Optional[List[str]] = None


# Adopter Models
class AdopterCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    address: str


class AdopterUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class AdopterResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='_id', serialization_alias='_id')
    name: str
    phone: str
    email: str
    address: str


# Adoption Models
class AdoptionCreate(BaseModel):
    animal_id: str
    adopter_id: str
    adoption_date: Optional[str] = None
    notes: Optional[str] = None


class AdoptionUpdate(BaseModel):
    animal_id: Optional[str] = None
    adopter_id: Optional[str] = None
    adoption_date: Optional[str] = None
    notes: Optional[str] = None


class AdoptionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='_id', serialization_alias='_id')
    animal_id: str
    adopter_id: str
    adoption_date: str
    notes: Optional[str] = None


# Medical Record Models
class MedicalRecordCreate(BaseModel):
    animal_id: str
    vet_name: str
    visit_date: str
    diagnosis: str
    treatment: str
    notes: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    animal_id: Optional[str] = None
    vet_name: Optional[str] = None
    visit_date: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='_id', serialization_alias='_id')
    animal_id: str
    vet_name: str
    visit_date: str
    diagnosis: str
    treatment: str
    notes: Optional[str] = None


# Volunteer Models
class VolunteerCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    skills: List[str]  # Changed to list for multiple skills
    availability: str


class VolunteerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    skills: Optional[List[str]] = None  # Changed to list
    availability: Optional[str] = None


# Volunteer Activity Models
class VolunteerActivityCreate(BaseModel):
    volunteer_id: str
    animal_id: str
    activity_type: str
    activity_date: str  # YYYY-MM-DD format
    duration_minutes: int = Field(..., gt=0)
    notes: Optional[str] = None


class VolunteerActivityUpdate(BaseModel):
    volunteer_id: Optional[str] = None
    animal_id: Optional[str] = None
    activity_type: Optional[str] = None
    activity_date: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None


class VolunteerActivityResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='_id', serialization_alias='_id')
    volunteer_id: str
    animal_id: str
    activity_type: str
    activity_date: str
    duration_minutes: int
    notes: Optional[str] = None


# Volunteer Assignment Models
class VolunteerAssignmentCreate(BaseModel):
    animal_id: str
    volunteer_id: str


class VolunteerAssignmentResponse(BaseModel):
    success: bool
    message: str
    animal_id: str
    volunteer_id: str


class VolunteerResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias='_id', serialization_alias='_id')
    name: str
    phone: str
    email: str
    skills: List[str]  # Changed to list for multiple skills
    availability: str


# Common Response Models
class SuccessResponse(BaseModel):
    success: bool
    message: str

