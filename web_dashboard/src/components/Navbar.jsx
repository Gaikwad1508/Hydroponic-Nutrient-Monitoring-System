import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-green-700 p-4 text-white shadow-lg flex justify-between items-center">
      <h1 className="text-xl font-bold">🌿 Hydroponics Dashboard</h1>
      <div className="space-x-4">
        <Link to="/" className="hover:underline">
          Dashboard
        </Link>
      </div>
    </nav>
  );
}
