type DayPlan = {
  day: number;
  morning: string;
  afternoon: string;
  evening: string;
};

type ActivityResult = {
  day_wise_plan: DayPlan[];
  must_see: string[];
  estimated_activity_cost: number;
};

export default function ActivityCard({ activities }: { activities: ActivityResult }) {  return (
    <div className="bg-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">🗺️</span>
        <h3 className="font-semibold text-white">Activities</h3>
      </div>

      <div className="mb-4">
        <p className="text-slate-400 text-xs uppercase tracking-wide mb-2">
          Must See
        </p>
        <div className="flex flex-wrap gap-2">
          {activities.must_see.map((place, i) => (
            <span
              key={i}
              className="bg-blue-900 text-blue-300 text-xs px-2 py-1 rounded-full"
            >
              {place}
            </span>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        {activities.day_wise_plan.map((day) => (
          <div key={day.day} className="border-l-2 border-blue-600 pl-3">
            <p className="text-white text-sm font-semibold mb-1">
              Day {day.day}
            </p>
            <p className="text-slate-400 text-xs">🌅 {day.morning}</p>
            <p className="text-slate-400 text-xs">☀️ {day.afternoon}</p>
            <p className="text-slate-400 text-xs">🌙 {day.evening}</p>
          </div>
        ))}
      </div>
    </div>
  );
}