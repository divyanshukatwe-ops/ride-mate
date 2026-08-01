from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class RideBase(BaseModel):
    pickup: str = Field(..., description="Pickup location", min_length=2)
    destination: str = Field(..., description="Destination location", min_length=2)
    date: str = Field(..., description="Date of travel (YYYY-MM-DD)")
    time: str = Field(..., description="Time of travel (HH:MM)")
    vehicle_type: str = Field(..., description="Vehicle type (Auto or Cab)")
    total_fare: float = Field(..., description="Total fare amount in INR", gt=0)
    available_seats: int = Field(..., description="Available seats left for pooling", ge=0)
    notes: Optional[str] = Field(default="", description="Additional instructions or preferences")
    creator_name: Optional[str] = Field(default="Student Rider", description="Name of ride host")

    @field_validator('vehicle_type')
    def validate_vehicle(cls, v):
        allowed = ['Auto', 'Cab']
        if v.title() not in allowed:
            raise ValueError("Vehicle type must be either 'Auto' or 'Cab'")
        return v.title()

class RideCreate(RideBase):
    pass

class RideUpdate(BaseModel):
    pickup: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    vehicle_type: Optional[str] = None
    total_fare: Optional[float] = None
    available_seats: Optional[int] = None
    notes: Optional[str] = None

class Ride(RideBase):
    id: str
    total_seats: int
    joined_passengers: int = 1
    fare_per_person: float
    created_at: str
    match_score: Optional[int] = None
    status: str = "Active" # Active, Full, Completed

class JoinRideRequest(BaseModel):
    passenger_name: Optional[str] = "Student Companion"

class JoinRideResponse(BaseModel):
    success: bool
    message: str
    ride: Ride

class DashboardStats(BaseModel):
    total_rides: int
    active_rides: int
    total_available_seats: int
    total_estimated_savings: float
    avg_match_score: int
    top_destinations: List[str]
