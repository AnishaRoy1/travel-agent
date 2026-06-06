type WeatherResult = {
  condition: string;
  average_temp_celsius: number;
  humidity_percent: number;
  travel_tip: string;
};

export default function WeatherCard({ weather }: { weather: WeatherResult }) {
  const icons: Record<string, string> = {
    Clear: "☀️",
    Clouds: "⛅",
    Rain: "🌧️",
    Drizzle: "🌦️",
    Thunderstorm: "⛈️",
    Snow: "❄️",
  };


  const icon = icons[weather.condition] || "🌤️";

  return (
    <div className="bg-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xl">🌍</span>
        <h3 className="font-semibold text-white">Weather</h3>
      </div>
      <p className="text-2xl mb-1">{icon}</p>
      <p className="text-blue-400 font-bold text-lg">{weather.condition}</p>
      <p className="text-slate-300 text-sm mt-1">
        {weather.average_temp_celsius}°C · {weather.humidity_percent}% humidity
      </p>
      <p className="text-slate-400 text-xs mt-2">{weather.travel_tip}</p>
    </div>
  );
}