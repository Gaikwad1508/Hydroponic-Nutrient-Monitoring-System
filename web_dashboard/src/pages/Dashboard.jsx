import React, { useEffect, useState } from "react";
import axios from "axios";
import SensorCard from "../components/SensorCard";
import NutrientCard from "../components/NutrientCard";

export default function Dashboard() {
  const [sensorData, setSensorData] = useState(null);
  const [nutrients, setNutrients] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get("http://localhost:5000/latest-data");
      setSensorData(res.data.sensor);
      setNutrients(res.data.nutrients);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // auto-refresh every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h2 className="text-xl font-semibold mb-2">📟 Latest Sensor Readings</h2>
        {sensorData ? (
          <SensorCard data={sensorData} />
        ) : (
          <p className="text-gray-500">Loading sensor data...</p>
        )}
      </div>
      <div>
        <h2 className="text-xl font-semibold mb-2">🧪 Predicted Nutrient Levels</h2>
        {nutrients ? (
          <NutrientCard data={nutrients} />
        ) : (
          <p className="text-gray-500">Loading predictions...</p>
        )}
      </div>
    </div>
  );
}
