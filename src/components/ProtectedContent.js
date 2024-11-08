// src/components/ProtectedContent.js

import React from 'react';
import { signOut } from 'firebase/auth';
import { auth } from '../firebase';  // Import auth from your Firebase config

const ProtectedContent = () => {
  const handleLogout = () => {
    signOut(auth);
  };

  return (
    <div>
      <h2>Protected Content</h2>
      <p>This content is only visible to logged-in users.</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default ProtectedContent;
