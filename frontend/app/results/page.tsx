"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import FlightCard from "@/components/FlightCard";
import HotelCard from "@/components/HotelCard";
import WeatherCard from "@/components/WeatherCard";
import ActivityCard from "@/components/ActivityCard";
import BudgetCard from "@/components/BudgetCard";

type TripResult = {
  destination: string;
  days: number;
  budget: number;
  flight: {
    airline: string;
    estimated_cost: number;
    duration_hours: number;
    stops: number;
    notes: string;
  };
  hotel: {
    name: string;
    location: string;
    estimated_cost_per_night: number;
    total_cost: number;
    rating: number;
    notes: string;
  };
  weather: {
    condition: string;
    average_temp_celsius: number;
    humidity_percent: number;
    travel_tip: string;
  };
  activities: {
    day_wise_plan: {
      day: number;
      morning: string;
      afternoon: string;
      evening: string;
    }[];
    must_see: string[];
    estimated_activity_cost: number;
  };
  budget_breakdown: {
    flight_cost: number;
    hotel_cost: number;
    activity_cost: number;
    food_estimate: number;
    total_estimated: number;
    remaining_budget: number;
    is_within_budget: boolean;
    recommendation: string;
  };
  itinerary: string;
  recommendation: string;
};

export default function ResultsPage() {
  const router = useRouter();
  const [trip, setTrip] = useState<TripResult | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("tripResult");
    if (!stored) {
      router.push("/");
      return;
    }
    setTrip(JSON.parse(stored));
  }, []);

  if (!trip) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-slate-400">Loading...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen px-4 py-10 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">
            {trip.destination} Trip 🌏
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            {trip.days} days · Budget ₹{trip.budget.toLocaleString()}
          </p>
        </div>
        <button
          onClick={() => router.push("/")}
          className="text-sm text-blue-400 hover:text-blue-300"
        >
          ← Plan another
        </button>
      </div>

      <div className="bg-slate-800 rounded-xl p-5 mb-6">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xl">📋</span>
          <h3 className="font-semibold text-white">Itinerary Summary</h3>
        </div>
        <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-line">
          {trip.itinerary}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <FlightCard flight={trip.flight} />
        <HotelCard hotel={trip.hotel} />
        <WeatherCard weather={trip.weather} />
        <BudgetCard budget={trip.budget_breakdown} />
      </div>

      <ActivityCard activities={trip.activities} />
    </main>
  );
}