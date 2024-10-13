import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Root from './Root';
import Timeline from './components/Timeline';
import SortableStories from './components/SortableCards';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';  // Import auth from your Firebase config
import Login from './components/Login';
import ProtectedContent from './components/ProtectedContent';

const App = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setUser(user);
      } else {
        setUser(null);
      }
    });
    return () => unsubscribe();
  }, []);

  return (
    <div>
      {user ? (
        <Router>
          <Routes>
            <Route path="/" element={<Root />} />
            <Route path="/categories" element={<SortableStories />} />
            <Route path="/timeline" element={<Timeline />} />
          </Routes>
        </Router>
      ) : (
        <Login />
      )}
    </div>
  );
};

export default App;
