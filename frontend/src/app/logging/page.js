'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Logging() {
    const [logs, setLogs] = useState([]);
    const [newUsers, setNewUsers] = useState([]);
    const [allUsers, setAllUsers] = useState([]);
    const [error, setError] = useState('');
    const router = useRouter();

    const fetchData = async (endpoint, setData) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000/admin${endpoint}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error(`Failed to fetch ${endpoint}`);
            }
            const data = await response.json();
            setData(data);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleBan = async (userId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000/admin/users/ban/${userId}`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error('Failed to ban user');
            }
            setAllUsers(allUsers.map(user => user.id === userId ? { ...user, is_banned: true } : user));
        } catch (err) {
            setError('Failed to ban user');
        }
    };

    useEffect(() => {
        fetchData('/logs/today', setLogs);
        fetchData('/users/new', setNewUsers);
        fetchData('/users', setAllUsers);
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-3xl font-bold mb-6 text-black">Admin Dashboard - Logs & Users</h1>
                {error && <p className="text-red-500 mb-4">{error}</p>}

                <div className="mb-8">
                    <h2 className="text-2xl font-semibold mb-4 text-black">Today’s Prediction Logs</h2>
                    {logs.length === 0 ? (
                        <p className="text-black">No logs for today.</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse">
                                <thead>
                                    <tr className="bg-gray-200">
                                        <th className="border px-4 py-2 text-black">User ID</th>
                                        <th className="border px-4 py-2 text-black">Input Data</th>
                                        <th className="border px-4 py-2 text-black">Prediction</th>
                                        <th className="border px-4 py-2 text-black">Probability</th>
                                        <th className="border px-4 py-2 text-black">Timestamp</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {logs.map(log => (
                                        <tr key={log.id}>
                                            <td className="border px-4 py-2 text-black">{log.user_id}</td>
                                            <td className="border px-4 py-2 text-black">{log.input_data}</td>
                                            <td className="border px-4 py-2 text-black">{log.prediction}</td>
                                            <td className="border px-4 py-2 text-black">{log.probability}</td>
                                            <td className="border px-4 py-2 text-black">{log.timestamp}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                <div className="mb-8">
                    <h2 className="text-2xl font-semibold mb-4 text-black">New Users (Today)</h2>
                    {newUsers.length === 0 ? (
                        <p className="text-black">No new users today.</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse">
                                <thead>
                                    <tr className="bg-gray-200">
                                        <th className="border px-4 py-2 text-black">ID</th>
                                        <th className="border px-4 py-2 text-black">Email</th>
                                        <th className="border px-4 py-2 text-black">Role</th>
                                        <th className="border px-4 py-2 text-black">Verified</th>
                                        <th className="border px-4 py-2 text-black">Banned</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {newUsers.map(user => (
                                        <tr key={user.id}>
                                            <td className="border px-4 py-2 text-black">{user.id}</td>
                                            <td className="border px-4 py-2 text-black">{user.email}</td>
                                            <td className="border px-4 py-2 text-black">{user.role}</td>
                                            <td className="border px-4 py-2 text-black">{user.is_verified ? 'Yes' : 'No'}</td>
                                            <td className="border px-4 py-2 text-black">{user.is_banned ? 'Yes' : 'No'}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                <div>
                    <h2 className="text-2xl font-semibold mb-4 text-black">All Users</h2>
                    {allUsers.length === 0 ? (
                        <p className="text-black">No users found.</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse">
                                <thead>
                                    <tr className="bg-gray-200">
                                        <th className="border px-4 py-2 text-black">ID</th>
                                        <th className="border px-4 py-2 text-black">Email</th>
                                        <th className="border px-4 py-2 text-black">Role</th>
                                        <th className="border px-4 py-2 text-black">Verified</th>
                                        <th className="border px-4 py-2 text-black">Banned</th>
                                        <th className="border px-4 py-2 text-black">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {allUsers.map(user => (
                                        <tr key={user.id}>
                                            <td className="border px-4 py-2 text-black">{user.id}</td>
                                            <td className="border px-4 py-2 text-black">{user.email}</td>
                                            <td className="border px-4 py-2 text-black">{user.role}</td>
                                            <td className="border px-4 py-2 text-black">{user.is_verified ? 'Yes' : 'No'}</td>
                                            <td className="border px-4 py-2 text-black">{user.is_banned ? 'Yes' : 'No'}</td>
                                            <td className="border px-4 py-2">
                                                {!user.is_banned && user.role !== 'admin' && (
                                                    <button
                                                        onClick={() => handleBan(user.id)}
                                                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                                                    >
                                                        Ban
                                                    </button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                <button
                    onClick={() => router.push('/')}
                    className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                    Return Home
                </button>
            </div>
        </div>
    );
}