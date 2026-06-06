type HotelResult = {
  name: string;
  location: string;
  estimated_cost_per_night: number;
  total_cost: number;
  rating: number;
  notes: string;
};

export default function HotelCard({ hotel }: { hotel: HotelResult }) {  return (
    <div className="bg-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">🏨</span>
        <h3 className="font-semibold text-white">Hotel</h3>
      </div>
      <p className="text-blue-400 font-bold text-lg">{hotel.name}</p>
      <p className="text-slate-300 text-sm mt-1">{hotel.location}</p>
      <p className="text-slate-300 text-sm">
        ₹{hotel.estimated_cost_per_night.toLocaleString()}/night ·{" "}
        ⭐ {hotel.rating}
      </p>
      <p className="text-green-400 font-semibold mt-2">
        Total: ₹{hotel.total_cost.toLocaleString()}
      </p>
      <p className="text-slate-400 text-xs mt-2">{hotel.notes}</p>
    </div>
  );
}