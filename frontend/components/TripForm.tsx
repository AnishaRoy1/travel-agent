"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function TripForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    source: "",
    destination: "",
    days: "",
    budget: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit() {
    setError("");

    if (!form.source || !form.destination || !form.days || !form.budget) {
      setError("Please fill in all fields.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/plan-trip`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source: form.source,
          destination: form.destination,
          days: parseInt(form.days),
          budget: parseInt(form.budget),
        }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Something went wrong");
      }

      const data = await response.json();

      sessionStorage.setItem("tripResult", JSON.stringify(data));
      router.push("/results");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-slate-800 rounded-2xl p-8 w-full max-w-md shadow-xl">
      <h1 className="text-2xl font-bold text-white mb-2">
        AI Travel Planner ✈️
      </h1>
      <p className="text-slate-400 text-sm mb-6">
        Plan your perfect trip in seconds
      </p>

      <div className="flex flex-col gap-4">
        <div>
          <label className="text-slate-300 text-sm mb-1 block">From</label>
          <input
            name="source"
            value={form.source}
            onChange={handleChange}
            placeholder="e.g. Bangalore"
            className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="text-slate-300 text-sm mb-1 block">To</label>
          <input
            name="destination"
            value={form.destination}
            onChange={handleChange}
            placeholder="e.g. Bali"
            className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex gap-3">
          <div className="flex-1">
            <label className="text-slate-300 text-sm mb-1 block">Days</label>
            <input
              name="days"
              type="number"
              value={form.days}
              onChange={handleChange}
              placeholder="5"
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex-1">
            <label className="text-slate-300 text-sm mb-1 block">
              Budget (₹)
            </label>
            <input
              name="budget"
              type="number"
              value={form.budget}
              onChange={handleChange}
              placeholder="80000"
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-semibold py-3 rounded-lg transition-colors"
        >
          {loading ? "Planning your trip..." : "Plan My Trip →"}
        </button>
      </div>
    </div>
  );
}