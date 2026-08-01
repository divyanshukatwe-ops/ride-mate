import datetime
from typing import List, Dict, Any, Optional

# In-memory storage for ride data
rides_db: List[Dict[str, Any]] = []

def calculate_fare_per_person(total_fare: float, joined_passengers: int) -> float:
    """Helper to calculate per-person fare split accurately rounded to nearest rupee."""
    if joined_passengers <= 0:
        return total_fare
    return round(total_fare / joined_passengers, 1)

def seed_sample_data():
    """Seed 10 initial sample rides as required by hackathon spec."""
    global rides_db
    if len(rides_db) > 0:
        return  # Already seeded

    sample_rides = [
        {
            "id": "RIDE-101",
            "pickup": "College Main Gate",
            "destination": "Sitabuldi Metro Station",
            "date": "2026-08-01",
            "time": "14:30",
            "vehicle_type": "Auto",
            "total_fare": 180.0,
            "available_seats": 2,
            "total_seats": 3,
            "joined_passengers": 1,
            "fare_per_person": 180.0,
            "notes": "Leaving right after CS lecture. Quick drop near Metro Gate 2.",
            "creator_name": "Aarav Sharma",
            "created_at": "2026-08-01T09:00:00",
            "status": "Active"
        },
        {
            "id": "RIDE-102",
            "pickup": "College Hostel Block B",
            "destination": "Nagpur Airport (NAG)",
            "date": "2026-08-01",
            "time": "16:00",
            "vehicle_type": "Cab",
            "total_fare": 400.0,
            "available_seats": 3,
            "total_seats": 4,
            "joined_passengers": 1,
            "fare_per_person": 400.0,
            "notes": "AC Sedan cab. Traveling home for weekend. Room for 2 large luggage bags.",
            "creator_name": "Priya Patel",
            "created_at": "2026-08-01T09:30:00",
            "status": "Active"
        },
        {
            "id": "RIDE-103",
            "pickup": "College Admin Building",
            "destination": "Dharampeth Food Street",
            "date": "2026-08-01",
            "time": "18:15",
            "vehicle_type": "Auto",
            "total_fare": 120.0,
            "available_seats": 1,
            "total_seats": 3,
            "joined_passengers": 2,
            "fare_per_person": 60.0,
            "notes": "Evening snacks run! 2 of us already going, need 1 more to fill the auto.",
            "creator_name": "Rohan Gupta",
            "created_at": "2026-08-01T10:00:00",
            "status": "Active"
        },
        {
            "id": "RIDE-104",
            "pickup": "College Library",
            "destination": "Sadar Bazaar",
            "date": "2026-08-01",
            "time": "17:00",
            "vehicle_type": "Cab",
            "total_fare": 250.0,
            "available_seats": 2,
            "total_seats": 4,
            "joined_passengers": 2,
            "fare_per_person": 125.0,
            "notes": "Shopping and dinner at Sadar. Comfortable Uber Go.",
            "creator_name": "Ananya Roy",
            "created_at": "2026-08-01T10:15:00",
            "status": "Active"
        },
        {
            "id": "RIDE-105",
            "pickup": "College Mechanical Block",
            "destination": "Medical Square",
            "date": "2026-08-01",
            "time": "15:45",
            "vehicle_type": "Auto",
            "total_fare": 150.0,
            "available_seats": 2,
            "total_seats": 3,
            "joined_passengers": 1,
            "fare_per_person": 150.0,
            "notes": "Going for lab report printing & medical supplies.",
            "creator_name": "Vikram Singh",
            "created_at": "2026-08-01T10:30:00",
            "status": "Active"
        },
        {
            "id": "RIDE-106",
            "pickup": "College Gate 2",
            "destination": "IT Park / Gayatri Nagar",
            "date": "2026-08-02",
            "time": "09:00",
            "vehicle_type": "Cab",
            "total_fare": 200.0,
            "available_seats": 3,
            "total_seats": 4,
            "joined_passengers": 1,
            "fare_per_person": 200.0,
            "notes": "Morning internship commuter ride. On time departure.",
            "creator_name": "Sneha Kulkarni",
            "created_at": "2026-08-01T10:45:00",
            "status": "Active"
        },
        {
            "id": "RIDE-107",
            "pickup": "College Sports Complex",
            "destination": "VR Mall / Trillium",
            "date": "2026-08-02",
            "time": "13:30",
            "vehicle_type": "Auto",
            "total_fare": 160.0,
            "available_seats": 2,
            "total_seats": 3,
            "joined_passengers": 1,
            "fare_per_person": 160.0,
            "notes": "Weekend movie trip! Catching 2:15 PM show.",
            "creator_name": "Devansh Mehta",
            "created_at": "2026-08-01T11:00:00",
            "status": "Active"
        },
        {
            "id": "RIDE-108",
            "pickup": "College Main Campus",
            "destination": "Nagpur Railway Station",
            "date": "2026-08-02",
            "time": "19:00",
            "vehicle_type": "Cab",
            "total_fare": 320.0,
            "available_seats": 2,
            "total_seats": 4,
            "joined_passengers": 2,
            "fare_per_person": 160.0,
            "notes": "Catching 8:30 PM train. Plenty of boot space for luggage.",
            "creator_name": "Kabir Verma",
            "created_at": "2026-08-01T11:15:00",
            "status": "Active"
        },
        {
            "id": "RIDE-109",
            "pickup": "College Girls Hostel",
            "destination": "Futala Lake",
            "date": "2026-08-02",
            "time": "17:30",
            "vehicle_type": "Auto",
            "total_fare": 140.0,
            "available_seats": 1,
            "total_seats": 3,
            "joined_passengers": 2,
            "fare_per_person": 70.0,
            "notes": "Sunset breeze drive. Great street food hangout spot.",
            "creator_name": "Diya Nair",
            "created_at": "2026-08-01T11:30:00",
            "status": "Active"
        },
        {
            "id": "RIDE-110",
            "pickup": "College Canteen",
            "destination": "Wardha Road Square",
            "date": "2026-08-03",
            "time": "11:00",
            "vehicle_type": "Auto",
            "total_fare": 100.0,
            "available_seats": 2,
            "total_seats": 3,
            "joined_passengers": 1,
            "fare_per_person": 100.0,
            "notes": "Quick drop near metro connectivity.",
            "creator_name": "Aditya Joshi",
            "created_at": "2026-08-01T11:45:00",
            "status": "Active"
        }
    ]

    rides_db.extend(sample_rides)

def get_all_rides() -> List[Dict[str, Any]]:
    seed_sample_data()
    return rides_db

def get_ride_by_id(ride_id: str) -> Optional[Dict[str, Any]]:
    seed_sample_data()
    for ride in rides_db:
        if ride["id"] == ride_id:
            return ride
    return None

def add_ride(ride_data: Dict[str, Any]) -> Dict[str, Any]:
    seed_sample_data()
    new_id = f"RIDE-{100 + len(rides_db) + 1}"
    now_str = datetime.datetime.now().isoformat()
    
    available_seats = ride_data["available_seats"]
    total_seats = available_seats + 1  # Creator is 1st seat
    total_fare = ride_data["total_fare"]
    
    new_ride = {
        "id": new_id,
        "pickup": ride_data["pickup"].strip(),
        "destination": ride_data["destination"].strip(),
        "date": ride_data["date"],
        "time": ride_data["time"],
        "vehicle_type": ride_data["vehicle_type"],
        "total_fare": float(total_fare),
        "available_seats": available_seats,
        "total_seats": total_seats,
        "joined_passengers": 1,
        "fare_per_person": float(total_fare),
        "notes": ride_data.get("notes", "").strip(),
        "creator_name": ride_data.get("creator_name", "Student Host"),
        "created_at": now_str,
        "status": "Active" if available_seats > 0 else "Full"
    }
    
    rides_db.insert(0, new_ride) # Insert at front so new rides appear top
    return new_ride

def update_ride(ride_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    seed_sample_data()
    for ride in rides_db:
        if ride["id"] == ride_id:
            for key, value in update_data.items():
                if value is not None:
                    ride[key] = value
            # Recalculate fare per person
            ride["fare_per_person"] = calculate_fare_per_person(ride["total_fare"], ride["joined_passengers"])
            if ride["available_seats"] <= 0:
                ride["status"] = "Full"
            else:
                ride["status"] = "Active"
            return ride
    return None

def delete_ride(ride_id: str) -> bool:
    seed_sample_data()
    global rides_db
    initial_len = len(rides_db)
    rides_db = [r for r in rides_db if r["id"] != ride_id]
    return len(rides_db) < initial_len

def join_ride(ride_id: str) -> Optional[Dict[str, Any]]:
    seed_sample_data()
    for ride in rides_db:
        if ride["id"] == ride_id:
            if ride["available_seats"] <= 0:
                return None  # No seats available
            
            ride["available_seats"] -= 1
            ride["joined_passengers"] += 1
            ride["fare_per_person"] = calculate_fare_per_person(ride["total_fare"], ride["joined_passengers"])
            
            if ride["available_seats"] == 0:
                ride["status"] = "Full"
            
            return ride
    return None

def leave_ride(ride_id: str) -> Optional[Dict[str, Any]]:
    seed_sample_data()
    for ride in rides_db:
        if ride["id"] == ride_id:
            if ride["joined_passengers"] <= 1:
                return None  # Cannot leave if host is the only person
            
            ride["available_seats"] += 1
            ride["joined_passengers"] -= 1
            ride["fare_per_person"] = calculate_fare_per_person(ride["total_fare"], ride["joined_passengers"])
            ride["status"] = "Active"
            return ride
    return None
