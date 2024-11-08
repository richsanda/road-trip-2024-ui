import React, { useState } from 'react';
import { format } from 'date-fns';
import DateGrid from './DateGrid';
import 'bootstrap/dist/css/bootstrap.min.css';
import TimelineCard from './TimelineCard';
import './Timeline.css'
import TimelineModal from './TimelineModal';

const apiUrl = process.env.REACT_APP_API_URL;

function Timeline() {

  const [timeline, setTimeline] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [showModal, setShowModal] = useState(false);

  const handleTimelineDateSelect = (date) => {
    fetchTimeline(date);
  };

  const fetchTimeline = async (date) => {
    try {
      const formattedDate = format(date, 'yyyy-MM-dd');
      const response = await fetch(`${apiUrl}/timeline?start=${formattedDate}T00:00:00&end=${formattedDate}T23:59:00`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setTimeline(data);
    } catch (error) {
      alert(apiUrl);
      console.error('Error fetching records:', error);
    }
  };

  const handleCardClick = (index) => {
    setSelectedIndex(index);
    setShowModal(true);
  };

  const closeModal = () => {
    setSelectedIndex(null);
    setShowModal(false);
  };

  return (
    <div className="App">
      <div className="header-container">
        <div className="date-grid-container">
          <DateGrid
            startDate={new Date(2024, 5, 27)} // June 27, 2024
            endDate={new Date(2024, 6, 15)}   // July 15, 2024
            onDateSelect={handleTimelineDateSelect}
          />
        </div>
        <h2>me and sydney's jun / jul 2024 road trip</h2>
      </div>

      <div className="records-list-container">
          <div className="records-list">
          {timeline.map((record, index) => (
            <div className="timeline-card" key={index} onClick={() => handleCardClick(index)}>
              <TimelineCard record={record} />
            </div>
          ))}
        </div>
      </div>

      {/* Modal */}
      {showModal && <TimelineModal records={timeline} initialIndex={selectedIndex} show={showModal} handleClose={closeModal} />}
    </div>
  );
}

export default Timeline;
