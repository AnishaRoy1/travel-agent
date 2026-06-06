type FlightResult = {
  airline: string;
  estimated_cost: number;
  duration_hours: number;
  stops: number;
  notes: string;
};

export default function FlightCard({ flight }: { flight: FlightResult }) {  return (
    <div className="bg-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">✈️</span>
        <h3 className="font-semibold text-white">Flight</h3>
      </div>
      <p className="text-blue-400 font-bold text-lg">{flight.airline}</p>
      <p className="text-slate-300 text-sm mt-1">
        {flight.duration_hours} hrs · {flight.stops} stop(s)
      </p>
      <p className="text-green-400 font-semibold mt-2">
        ₹{flight.estimated_cost.toLocaleString()}
      </p>
      <p className="text-slate-400 text-xs mt-2">{flight.notes}</p>
    </div>
  );
}