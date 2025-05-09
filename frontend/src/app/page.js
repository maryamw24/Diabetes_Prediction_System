"use client";
import { useState, useEffect } from 'react';


import Link from "next/link";

export default function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null);
  useEffect(() => {
          const token = localStorage.getItem('token');
          if (token) {
              setIsLoggedIn(true);
              try {
                  const payload = JSON.parse(atob(token.split('.')[1]));
                  setUserRole(payload.sub); // Assuming role is stored in token
              } catch (e) {
                  console.error('Error decoding token:', e);
                  setIsLoggedIn(false);
              }
          }
      }, []);
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-100 to-blue-300 p-6">
      <div className="bg-white p-8 rounded-2xl shadow-lg max-w-2xl text-center">
        <h1 className="text-4xl font-bold mb-4 text-blue-800">Early Stage Diabetes Prediction</h1>
        <p className="text-lg text-gray-700 mb-6">
          Welcome! Our system is designed to help predict the likelihood of early stage diabetes.
          We will ask you a few simple questions about your daily life and habits.
          After analyzing your responses, we will provide an accurate prediction based on your input.
        </p>
        <p className="text-md text-gray-600 mb-8">
          It only takes a few minutes, and your answers could help you take the first step toward a healthier future.
        </p>
        <Link href={isLoggedIn ? "/questionaire" : "/login"}>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-full text-lg transition">
            Get Started
          </button>
        </Link>
      </div>
    </main>
  );
}