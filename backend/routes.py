from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from models import Ride, RideCreate, RideUpdate, JoinRideRequest, JoinRideResponse, DashboardStats
import data
import utils

router = APIRouter(prefix="/rides", tags=["Rides"])

def _to_str(val) -> Optional[str]:
    """Helper to safely extract string value when called directly or via FastAPI."""
    if val is None:
        return None
    if isinstance(val, str):
        return val
    if hasattr(val, "default") and isinstance(val.default, str):
        return val.default
    return None

@router.get("", response_model=List[Ride])
def list_rides(
    pickup: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    vehicle_type: Optional[str] = None
):
    """Retrieve all rides with optional filtering and smart match score calculation."""
    p_str = _to_str(pickup)
    d_str = _to_str(destination)
    dt_str = _to_str(date)
    tm_str = _to_str(time)
    v_str = _to_str(vehicle_type)

    all_rides = data.get_all_rides()
    filtered_rides = []

    for r in all_rides:
        if v_str and v_str.strip() and v_str.lower() != "all":
            if r["vehicle_type"].lower() != v_str.strip().lower():
                continue
                
        if dt_str and dt_str.strip():
            if r["date"] != dt_str.strip():
                continue

        score = utils.compute_smart_match_score(
            ride=r,
            pickup_query=p_str,
            dest_query=d_str,
            time_query=tm_str,
            date_query=dt_str,
            vehicle_query=v_str
        )
        
        ride_copy = dict(r)
        ride_copy["match_score"] = score
        filtered_rides.append(ride_copy)

    filtered_rides.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return filtered_rides

@router.get("/search", response_model=List[Ride])
def search_rides(
    pickup: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    vehicle_type: Optional[str] = None
):
    """Advanced Smart Match Search API endpoint."""
    return list_rides(pickup=pickup, destination=destination, date=date, time=time, vehicle_type=vehicle_type)

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats():
    """Retrieve aggregate metric statistics for the RideMate Dashboard."""
    all_rides = data.get_all_rides()
    stats = utils.get_dashboard_metrics(all_rides)
    return stats

@router.get("/{ride_id}", response_model=Ride)
def get_ride(ride_id: str):
    """Fetch details for a specific ride by ID."""
    ride = data.get_ride_by_id(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail=f"Ride '{ride_id}' not found.")
    return ride

@router.post("", response_model=Ride, status_code=status.HTTP_201_CREATED)
def create_ride(ride_in: RideCreate):
    """Create a new ride post."""
    if not ride_in.pickup.strip():
        raise HTTPException(status_code=400, detail="Pickup location is required.")
    if not ride_in.destination.strip():
        raise HTTPException(status_code=400, detail="Destination location is required.")
    if ride_in.total_fare <= 0:
        raise HTTPException(status_code=400, detail="Total fare must be greater than 0.")
    if ride_in.available_seats <= 0:
        raise HTTPException(status_code=400, detail="Available seats must be greater than 0.")

    created_ride = data.add_ride(ride_in.dict())
    created_ride["match_score"] = 99
    return created_ride

@router.put("/{ride_id}", response_model=Ride)
def update_ride(ride_id: str, ride_update: RideUpdate):
    """Update ride details."""
    existing = data.get_ride_by_id(ride_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Ride '{ride_id}' not found.")
        
    if ride_update.total_fare is not None and ride_update.total_fare <= 0:
        raise HTTPException(status_code=400, detail="Total fare must be greater than 0.")
    if ride_update.available_seats is not None and ride_update.available_seats < 0:
        raise HTTPException(status_code=400, detail="Available seats cannot be negative.")

    updated = data.update_ride(ride_id, ride_update.dict(exclude_unset=True))
    return updated

@router.delete("/{ride_id}", status_code=status.HTTP_200_OK)
def delete_ride(ride_id: str):
    """Cancel / delete a ride post."""
    success = data.delete_ride(ride_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Ride '{ride_id}' not found.")
    return {"success": True, "message": f"Ride '{ride_id}' successfully removed."}

@router.post("/{ride_id}/join", response_model=JoinRideResponse)
def join_ride(ride_id: str, req: Optional[JoinRideRequest] = None):
    """Join an existing ride."""
    ride = data.get_ride_by_id(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail=f"Ride '{ride_id}' not found.")

    if ride["available_seats"] <= 0:
        raise HTTPException(status_code=400, detail="No Seats Available for this ride.")

    updated_ride = data.join_ride(ride_id)
    if not updated_ride:
        raise HTTPException(status_code=400, detail="Unable to join ride. No Seats Available.")

    return JoinRideResponse(
        success=True,
        message=f"Successfully joined ride {ride_id}! Fare per person updated to ₹{updated_ride['fare_per_person']}.",
        ride=updated_ride
    )

@router.post("/{ride_id}/leave", response_model=JoinRideResponse)
def leave_ride(ride_id: str):
    """Leave a joined ride. Increments seat count and recalculates fare split."""
    ride = data.get_ride_by_id(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail=f"Ride '{ride_id}' not found.")

    updated_ride = data.leave_ride(ride_id)
    if not updated_ride:
        raise HTTPException(status_code=400, detail="Unable to leave ride.")

    return JoinRideResponse(
        success=True,
        message=f"Successfully left ride {ride_id}. Seat freed up for other students.",
        ride=updated_ride
    )
