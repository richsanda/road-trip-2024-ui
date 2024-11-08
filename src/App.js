import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Root from './Root';
import Timeline from './roadtrip/Timeline';
import SortableStories from './components/SortableCards';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';  // Import auth from your Firebase config
import Login from './components/Login';

const App = () => {

  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setUser(user);
        setLoading(false);
      } else {
        setUser(null);
        setLoading(false);
      }
    });
    return () => unsubscribe();
  }, []);
  
  return (
    <div>
      {loading ? (
        <div className="spinner"></div>
      ) : user ? (
        <Router>
          <Routes>
            <Route path="/admin" element={<Root />} />
            <Route path="/categories" element={<SortableStories />} />
            <Route path="/" element={<Timeline />} />
          </Routes>
        </Router>
      ) : (
        <Login />
      )}
    </div>
  );
};

export default App;
