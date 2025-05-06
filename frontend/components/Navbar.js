'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Navbar() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userRole, setUserRole] = useState(null);
    const router = useRouter();

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

    const handleLogout = () => {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
        setUserRole(null);
        router.push('/login');
    };

    return (
        <nav className="bg-blue-600 p-4">
            <div className="container mx-auto flex justify-between items-center">
                <Link href="/getting-started" className="text-white text-lg font-bold">
                    Diabetes Prediction System
                </Link>
                <div className="space-x-4">
                    {isLoggedIn ? (
                        <button
                            onClick={handleLogout}
                            className="text-white hover:text-blue-200 focus:outline-none"
                        >
                            Logout
                        </button>
                    ) : (
                        <Link href="/login" className="text-white hover:text-blue-200">
                            Sign In
                        </Link>
                    )}
                </div>
            </div>
        </nav>
    );
}