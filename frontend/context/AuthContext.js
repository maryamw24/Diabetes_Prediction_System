'use client';
import { createContext, useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userRole, setUserRole] = useState(null);
    const pathname = usePathname(); // Track route changes in Next.js

    useEffect(() => {
        const token = localStorage.getItem('token');
        console.log('Encoded Token:', token);

        if (token) {
            try {
                // Decode the JWT payload
                const payload = JSON.parse(atob(token.split('.')[1]));

                // Get current time in seconds
                const currentTime = Math.floor(Date.now() / 1000);

                // Check if token has exp claim and if it's expired
                if (!payload.exp) {
                    console.error('Token missing exp claim');
                    localStorage.removeItem('token');
                    setIsLoggedIn(false);
                    setUserRole(null);
                    return;
                }

                if (payload.exp < currentTime) {
                    localStorage.removeItem('token');
                    setIsLoggedIn(false);
                    setUserRole(null);
                } else {
                    setIsLoggedIn(true);
                    setUserRole(payload.sub); // Assuming 'sub' contains role or user ID
                }
            } catch (e) {
                console.error('Error decoding token:', e);
                localStorage.removeItem('token');
                setIsLoggedIn(false);
                setUserRole(null);
            }
        } else {
            console.log('No token found in localStorage');
            setIsLoggedIn(false);
            setUserRole(null);
        }
    }, [pathname]); // Re-run on route changes

    return (
        <AuthContext.Provider value={{ isLoggedIn, setIsLoggedIn, userRole, setUserRole }}>
            {children}
        </AuthContext.Provider>
    );
};