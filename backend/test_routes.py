import data
import utils
import routes
from models import RideCreate, JoinRideRequest

def run_direct_tests():
    print("Testing data.seed_sample_data()...")
    data.seed_sample_data()
    all_rides = data.get_all_rides()
    assert len(all_rides) == 10, f"Expected 10 sample rides, got {len(all_rides)}"
    print("[SUCCESS] Initial 10 sample rides verified in memory!")

    print("\nTesting routes.list_rides()...")
    list_res = routes.list_rides()
    assert len(list_res) == 10
    print(f"[SUCCESS] list_rides() returned {len(list_res)} rides.")

    print("\nTesting routes.get_dashboard_stats()...")
    stats = routes.get_dashboard_stats()
    assert stats["total_rides"] == 10
    assert stats["active_rides"] > 0
    assert stats["total_available_seats"] > 0
    print(f"[SUCCESS] Dashboard stats verified: {stats}")

    print("\nTesting routes.create_ride()...")
    new_ride_in = RideCreate(
        pickup="College Hostel Block C",
        destination="Airport Terminal 1",
        date="2026-08-01",
        time="19:30",
        vehicle_type="Cab",
        total_fare=360.0,
        available_seats=3,
        notes="Direct route to airport",
        creator_name="Aarav"
    )
    created = routes.create_ride(new_ride_in)
    ride_id = created["id"]
    assert created["pickup"] == "College Hostel Block C"
    print(f"[SUCCESS] Ride created: {ride_id} - {created['pickup']} -> {created['destination']}")

    print(f"\nTesting routes.join_ride('{ride_id}')...")
    join_res = routes.join_ride(ride_id, JoinRideRequest(passenger_name="Rahul"))
    assert join_res.success == True
    assert join_res.ride.available_seats == 2
    assert join_res.ride.joined_passengers == 2
    assert join_res.ride.fare_per_person == 180.0  # 360 / 2 = 180
    print(f"[SUCCESS] Join Ride verified! Seats left: 2, Fare share: Rs. 180 / person.")

    print("\nTesting Smart Match search...")
    search_res = routes.search_rides(pickup="College", destination="Airport")
    assert len(search_res) > 0
    top_score = search_res[0]["match_score"]
    assert top_score >= 80
    print(f"[SUCCESS] Smart Match search verified! Top match score: {top_score}%")

    print(f"\nTesting delete_ride('{ride_id}')...")
    del_res = routes.delete_ride(ride_id)
    assert del_res["success"] == True
    print(f"[SUCCESS] Delete ride verified!")

    print("\n*** ALL BACKEND LOGIC & ROUTES PASSED EMPIRICAL VERIFICATION! ***")

if __name__ == "__main__":
    run_direct_tests()
