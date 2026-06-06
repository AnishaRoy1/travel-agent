type BudgetResult = {
  flight_cost: number;
  hotel_cost: number;
  activity_cost: number;
  food_estimate: number;
  total_estimated: number;
  remaining_budget: number;
  is_within_budget: boolean;
  recommendation: string;
};

export default function BudgetCard({ budget }: { budget: BudgetResult }) {  const items = [
    { label: "Flight", value: budget.flight_cost },
    { label: "Hotel", value: budget.hotel_cost },
    { label: "Activities", value: budget.activity_cost },
    { label: "Food", value: budget.food_estimate },
  ];

  return (
    <div className="bg-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">💰</span>
        <h3 className="font-semibold text-white">Budget Breakdown</h3>
      </div>

      <div className="flex flex-col gap-2 mb-3">
        {items.map((item) => (
          <div key={item.label} className="flex justify-between text-sm">
            <span className="text-slate-400">{item.label}</span>
            <span className="text-slate-200">
              ₹{item.value.toLocaleString()}
            </span>
          </div>
        ))}
        <div className="border-t border-slate-600 pt-2 flex justify-between text-sm font-semibold">
          <span className="text-slate-300">Total</span>
          <span className="text-white">
            ₹{budget.total_estimated.toLocaleString()}
          </span>
        </div>
      </div>

      <div
        className={`text-xs px-3 py-2 rounded-lg ${
          budget.is_within_budget
            ? "bg-green-900 text-green-300"
            : "bg-red-900 text-red-300"
        }`}
      >
        {budget.recommendation}
      </div>
    </div>
  );
}