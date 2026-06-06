from models import FlightResult, HotelResult, ActivityResult, BudgetResult


def budget_agent(
    trip_budget: int,
    flight: FlightResult,
    hotel: HotelResult,
    activity: ActivityResult,
    days: int
) -> BudgetResult:
    food_estimate = days * 1500  # ₹1500/day is a reasonable estimate

    total = (
        flight.estimated_cost +
        hotel.total_cost +
        activity.estimated_activity_cost +
        food_estimate
    )

    remaining = trip_budget - total
    is_within_budget = total <= trip_budget

    if is_within_budget:
        recommendation = f"You're within budget with ₹{remaining:,} to spare. Consider upgrading your hotel or adding an extra activity."
    else:
        overage = total - trip_budget
        recommendation = f"You're over budget by ₹{overage:,}. Consider a cheaper hotel or reducing activity costs."

    return BudgetResult(
        flight_cost=flight.estimated_cost,
        hotel_cost=hotel.total_cost,
        activity_cost=activity.estimated_activity_cost,
        food_estimate=food_estimate,
        total_estimated=total,
        remaining_budget=remaining,
        is_within_budget=is_within_budget,
        recommendation=recommendation
    )