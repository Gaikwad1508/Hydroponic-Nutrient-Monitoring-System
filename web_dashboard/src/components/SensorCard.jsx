import React from "react";

export default function SensorCard({ data }) {
  return (
    <div className="bg-white p-4 shadow-md rounded-2xl">
      {Object.entries(data).map(([key, value]) => (
        <p key={key} className="text-sm">
          <strong>{key}:</strong> {value}
        </p>
      ))}
    </div>
  );
}
