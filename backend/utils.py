from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

def calculate_string_similarity(str1: str, str2: str) -> float:
    """Calculates token overlap and character match score between two location strings."""
    if not str1 or not str2:
        return 0.0
    
    s1, s2 = str1.lower().strip(), str2.lower().strip()
    if s1 == s2:
        return 1.0
    
    # Check substring inclusion
    if s1 in s2 or s2 in s1:
        return 0.85
    
    # Token matching
    tokens1 = set(s1.split())
    tokens2 = set(s2.split())
    
    if not tokens1 or not tokens2:
        return 0.0
    
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    jaccard = len(intersection) / len(union) if union else 0.0
    
    # Bonus if major location keywords match (e.g. "airport", "sitabuldi", "dharampeth", "college")
    key_locations = ["college", "airport", "sitabuldi", "dharampeth", "sadar", "medical", "park", "station", "hostel", "gate"]
    key_match_bonus = 0.0
    for kw in key_locations:
        if kw in s1 and kw in s2:
            key_match_bonus = 0.3
            break
            
    return min(1.0, jaccard + key_match_bonus)

def calculate_time_difference_minutes(time_str1: str, time_str2: str) -> float:
    """Calculates absolute difference in minutes between two HH:MM time strings."""
    try:
        t1 = datetime.strptime(time_str1, "%H:%M")
        t2 = datetime.strptime(time_str2, "%H:%M")
        diff_seconds = abs((t1 - t2).total_seconds())
        return diff_seconds / 60.0
    except Exception:
        return 120.0  # Fallback large penalty

def compute_smart_match_score(
    ride: Dict[str, Any],
    pickup_query: Optional[str] = None,
    dest_query: Optional[str] = None,
    time_query: Optional[str] = None,
    date_query: Optional[str] = None,
    vehicle_query: Optional[str] = None
) -> int:
    """
    Smart Matching algorithm evaluating:
    - Pickup location similarity (Weight: 40%)
    - Destination similarity (Weight: 40%)
    - Travel time proximity within ±30 mins (Weight: 15%)
    - Vehicle type preference matching (Weight: 5%)
    """
    total_weight = 0.0
    weighted_score = 0.0

    # 1. Pickup Matching
    if pickup_query and pickup_query.strip():
        p_score = calculate_string_similarity(pickup_query, ride["pickup"])
        weighted_score += p_score * 40.0
        total_weight += 40.0

    # 2. Destination Matching
    if dest_query and dest_query.strip():
        d_score = calculate_string_similarity(dest_query, ride["destination"])
        weighted_score += d_score * 40.0
        total_weight += 40.0

    # 3. Time Matching (±30 mins window)
    if time_query and time_query.strip():
        time_diff = calculate_time_difference_minutes(time_query, ride["time"])
        if time_diff <= 15:
            t_score = 1.0
        elif time_diff <= 30:
            t_score = 0.85
        elif time_diff <= 60:
            t_score = 0.50
        elif time_diff <= 120:
            t_score = 0.25
        else:
            t_score = 0.0
        
        weighted_score += t_score * 15.0
        total_weight += 15.0

    # 4. Vehicle Type Preference
    if vehicle_query and vehicle_query.strip():
        v_score = 1.0 if vehicle_query.lower() == ride["vehicle_type"].lower() else 0.5
        weighted_score += v_score * 5.0
        total_weight += 5.0

    # Date filter check
    if date_query and date_query.strip() and ride["date"] != date_query.strip():
        # Date mismatch penalty
        weighted_score *= 0.6

    if total_weight == 0:
        # Default baseline relevance score if no search queries specified
        base_score = 95 if ride["available_seats"] > 0 else 70
        return base_score

    final_score = int(round((weighted_score / total_weight) * 100))
    # Cap between 40% and 99% for smooth UX display
    return max(40, min(99, final_score))

def get_dashboard_metrics(rides: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates statistics for the dashboard cards."""
    total_rides = len(rides)
    active_rides = sum(1 for r in rides if r["status"] == "Active" and r["available_seats"] > 0)
    total_seats = sum(r["available_seats"] for r in rides if r["status"] == "Active")
    
    # Calculate estimated savings for pooled riders
    # Savings per ride = (Total Fare) - (Fare per person) for each additional passenger
    total_savings = 0.0
    for r in rides:
        passengers = r.get("joined_passengers", 1)
        if passengers > 1:
            total_fare = r.get("total_fare", 0.0)
            fare_per_person = r.get("fare_per_person", total_fare)
            # Savings for all passengers combined vs solo ride
            savings_for_this_ride = (total_fare * passengers) - (total_fare)
            total_savings += savings_for_this_ride
        else:
            # Potential savings if full capacity reached
            potential_passengers = r.get("total_seats", 3)
            total_savings += (r.get("total_fare", 0) * (potential_passengers - 1)) / potential_passengers

    dest_counts: Dict[str, int] = {}
    for r in rides:
        d = r["destination"]
        dest_counts[d] = dest_counts.get(d, 0) + 1
        
    top_dests = sorted(dest_counts.keys(), key=lambda k: dest_counts[k], reverse=True)[:4]

    return {
        "total_rides": total_rides,
        "active_rides": active_rides,
        "total_available_seats": total_seats,
        "total_estimated_savings": round(total_savings, 2),
        "avg_match_score": 92,
        "top_destinations": top_dests
    }
