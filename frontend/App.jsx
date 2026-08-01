import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react.router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Toast from './components/Toast';
import JoinRideModal from './components/JoinRideModal';
import LiveMapModal from './components/LiveMapModal';
import SafetyModal from './components/SafetyModal';
import LoginModal from './components/LoginModal';

import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';
import BrowseRidesPage from './pages/BrowseRidesPage';
import CreateRidePage from './pages/CreateRidePage';
import MyRidesPage from './pages/MyRidesPage';
import ProfilePage from './pages/ProfilePage';

import { useRides } from './hooks/useRides';
import { rideService } from './services/api';

export default function App() {
  const {
    rides,
    stats,
    loading,
    filters,
    setFilters,
    fetchRides,
    handleJoinRide,
    handleCreateRide,
    resetFilters,
    toast,
    showToast,
    hideToast
  } = useRides();

  const [selectedRideToJoin, setSelectedRideToJoin] = useState(null);
  const [selectedTrackingRide, setSelectedTrackingRide] = useState(null);
  const [showSafetyModal, setShowSafetyModal] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  // User session state
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const stored = localStorage.getItem('ridemate_logged_user');
      return stored ? JSON.parse(stored) : {
        name: "Aarav Sharma",
        email: "aarav.sharma@college.edu",
        department: "Computer Science & Eng. (4th Year)",
        rollNo: "STU-2026-8842",
        phone: "+91 98230 44921",
        preferredGate: "College Gate 1 (Main Gate)"
      };
    } catch {
      return null;
    }
  });

  const handleLoginSuccess = (user) => {
    localStorage.setItem('ridemate_logged_user', JSON.stringify(user));
    setCurrentUser(user);
    setShowLoginModal(false);
    showToast(`Welcome back, ${user.name}! Logged in successfully.`, 'success');
  };

  const handleProfileUpdate = (updatedProfile) => {
    localStorage.setItem('ridemate_logged_user', JSON.stringify(updatedProfile));
    setCurrentUser(updatedProfile);
    showToast('Profile & Settings saved successfully!', 'success');
  };

  const handleLogout = () => {
    localStorage.removeItem('ridemate_logged_user');
    setCurrentUser(null);
    showToast('Logged out successfully.', 'info');
  };

  // My Rides persistence
  const [joinedRideIds, setJoinedRideIds] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('ridemate_joined_rides') || '[]');
    } catch {
      return [];
    }
  });

  const [offeredRideIds, setOfferedRideIds] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('ridemate_offered_rides') || '[]');
    } catch {
      return [];
    }
  });

  const saveJoinedRide = (id) => {
    setJoinedRideIds(prev => {
      if (prev.includes(id)) return prev;
      const next = [...prev, id];
      localStorage.setItem('ridemate_joined_rides', JSON.stringify(next));
      return next;
    });
  };

  const removeJoinedRide = (id) => {
    setJoinedRideIds(prev => {
      const next = prev.filter(rId => rId !== id);
      localStorage.setItem('ridemate_joined_rides', JSON.stringify(next));
      return next;
    });
  };

  const saveOfferedRide = (id) => {
    setOfferedRideIds(prev => {
      if (prev.includes(id)) return prev;
      const next = [...prev, id];
      localStorage.setItem('ridemate_offered_rides', JSON.stringify(next));
      return next;
    });
  };

  const openJoinModal = (ride) => {
    setSelectedRideToJoin(ride);
  };

  const closeJoinModal = () => {
    setSelectedRideToJoin(null);
  };

  const confirmJoinRide = async (rideId, passengerName) => {
    await handleJoinRide(rideId);
    saveJoinedRide(rideId);
  };

  const handleLeaveRide = async (rideId) => {
    try {
      if (rideService.leaveRide) {
        await rideService.leaveRide(rideId);
      }
      removeJoinedRide(rideId);
      showToast('Left ride successfully.', 'info');
      fetchRides();
    } catch (err) {
      removeJoinedRide(rideId);
      showToast('Booking removed.', 'info');
      fetchRides();
    }
  };

  const handleCreateRideWrapper = async (payload) => {
    const created = await handleCreateRide(payload);
    if (created && created.id) {
      saveOfferedRide(created.id);
    }
    return created;
  };

  const myTotalCount = joinedRideIds.length + offeredRideIds.length;

  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        {/* Navigation bar */}
        <Navbar
          myRidesCount={myTotalCount}
          onSafetyClick={() => setShowSafetyModal(true)}
          onLoginClick={() => setShowLoginModal(true)}
          currentUser={currentUser}
          onLogout={handleLogout}
        />

        {/* Main Content Body */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-12">
          <Routes>
            <Route
              path="/"
              element={
                <LandingPage
                  rides={rides}
                  onJoinClick={openJoinModal}
                />
              }
            />
            <Route
              path="/dashboard"
              element={
                <DashboardPage
                  stats={stats}
                  rides={rides}
                  loading={loading}
                  onJoinClick={openJoinModal}
                />
              }
            />
            <Route
              path="/browse"
              element={
                <BrowseRidesPage
                  rides={rides}
                  loading={loading}
                  filters={filters}
                  setFilters={setFilters}
                  onSearch={() => fetchRides()}
                  onReset={resetFilters}
                  onJoinClick={openJoinModal}
                />
              }
            />
            <Route
              path="/my-rides"
              element={
                <MyRidesPage
                  rides={rides}
                  joinedRideIds={joinedRideIds}
                  offeredRideIds={offeredRideIds}
                  onLeaveRide={handleLeaveRide}
                  onTrackClick={setSelectedTrackingRide}
                />
              }
            />
            <Route
              path="/profile"
              element={
                <ProfilePage
                  user={currentUser}
                  onUpdateProfile={handleProfileUpdate}
                  showToast={showToast}
                />
              }
            />
            <Route
              path="/create"
              element={
                <CreateRidePage
                  onCreateRide={handleCreateRideWrapper}
                  showToast={showToast}
                />
              }
            />
          </Routes>
        </main>

        {/* Footer */}
        <Footer />

        {/* Global Toast Alerts */}
        <Toast toast={toast} onClose={hideToast} />

        {/* Join Confirmation Modal */}
        {selectedRideToJoin && (
          <JoinRideModal
            ride={selectedRideToJoin}
            onClose={closeJoinModal}
            onConfirm={confirmJoinRide}
          />
        )}

        {/* Live GPS Driver Tracking Modal */}
        {selectedTrackingRide && (
          <LiveMapModal
            ride={selectedTrackingRide}
            onClose={() => setSelectedTrackingRide(null)}
          />
        )}

        {/* Emergency Contacts & 24/7 Customer Care Modal */}
        {showSafetyModal && (
          <SafetyModal
            onClose={() => setShowSafetyModal(false)}
            showToast={showToast}
          />
        )}

        {/* Student Login & Registration Modal */}
        {showLoginModal && (
          <LoginModal
            onClose={() => setShowLoginModal(false)}
            onLoginSuccess={handleLoginSuccess}
            showToast={showToast}
          />
        )}
      </div>
    </Router>
  );
}
