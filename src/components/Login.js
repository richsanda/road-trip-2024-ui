// src/components/Login.js

import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';  // Import the auth object from firebase.js
import './Login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await signInWithEmailAndPassword(auth, email, password);
            console.log('Login successful');
            // Redirect or display protected content
        } catch (err) {
            setError('Failed to log in: ' + err.message);
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f5f5f5' }}>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', width: '300px' }}>
                <h4 style={{ textAlign: 'center' }}>2024 road trip</h4>
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '10px', paddingTop: '10px' }}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{ padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc', width: '100%' }}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc', width: '100%' }}
                    />
                    <button type="submit" className='highway-sign' style={{ padding: '10px', fontSize: '16px', border: 'none', borderRadius: '4px', backgroundColor: '#4CAF50', color: 'white', cursor: 'pointer' }}>
                        Login
                    </button>
                </form>
                {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '10px' }}>{error}</p>}
            </div>
        </div>

    );
};

export default Login;
