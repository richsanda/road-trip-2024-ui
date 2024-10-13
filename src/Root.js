import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { Tabs, Tab } from 'react-bootstrap';
import DateGrid from './components/DateGrid';
import Popup from './components/Popup';
import PictureCard from './components/PictureCard';
import MapCarousel from './components/MapCarousel';
import ReceiptCarousel from './components/ReceiptCarousel';
import 'bootstrap/dist/css/bootstrap.min.css';
import ShazamCard from './components/ShazamCard';
import SongCard from './components/SongCard';
import MessageCard from './components/MessageCard';
import TimelineCard from './components/TimelineCard';
import StoryCard from './components/StoryCard';
import { fetchMessages, fetchShazams, fetchSongs, fetchStories, fetchTimeline, fetchPictures } from './api';

function Root() {
  const [pictures, setPictures] = useState([]);
  const [shazams, setShazams] = useState([]);
  const [songs, setSongs] = useState([]);
  const [messages, setMessages] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [stories, setStories] = useState([]);
  const [selectedPicture, setSelectedPicture] = useState(null);

  const handleDateSelect = (date) => {
    fetchPictures(date).then(response => setPictures(response));
  };

  const handleTimelineDateSelect = (date) => {
    fetchTimeline(date).then(response => setTimeline(response));
  };

  const fetchMethods = {
    stories: () => fetchStories().then(response => setStories(response)),
    songs: () => fetchSongs().then(response => setSongs(response)),
    messages: () => fetchMessages().then(response => setMessages(response)),
    timeline: () => fetchTimeline().then(response => setTimeline(response)),
    shazams: () => fetchShazams().then(response => setShazams(response))
  };


  const handleCardClick = (record) => {
    setSelectedPicture(record);
  };

  const closePopup = () => {
    setSelectedPicture(null);
  };

  return (
    <div className="App">
      <h1>Me and Sydney's 2024 Road Trip</h1>
      <Tabs defaultActiveKey="pictures" id="uncontrolled-tab-example" onSelect={(key) => {
        if (fetchMethods[key]) {
          fetchMethods[key]();
        }
      }}>
        <Tab eventKey="pictures" title="Pictures">
          <DateGrid
            startDate={new Date(2024, 5, 27)} // June 27, 2024
            endDate={new Date(2024, 6, 15)}   // July 15, 2024
            onDateSelect={handleDateSelect}
          />
          <div className="records-list">
            {pictures.map((record, index) => (
              <PictureCard key={index} record={record} onClick={() => handleCardClick(record)} />
            ))}
          </div>
          {selectedPicture && <Popup record={selectedPicture} show={!!selectedPicture} handleClose={closePopup} />}
        </Tab>
        <Tab eventKey="maps" title="Maps">
          <MapCarousel />
        </Tab>
        <Tab eventKey="receipts" title="Receipts">
          <ReceiptCarousel />
        </Tab>
        <Tab eventKey="shazams" title="Shazams">
          <div className="records-list">
            {shazams.map((record, index) => (
              <ShazamCard key={index} record={record} />
            ))}
          </div>
        </Tab>
        <Tab eventKey="songs" title="Songs">
          <div className="records-list">
            {songs.map((record, index) => (
              <SongCard key={index} record={record} />
            ))}
          </div>
        </Tab>
        <Tab eventKey="messages" title="Messages">
          <div className="records-list">
            {messages.map((record, index) => (
              <MessageCard key={index} record={record} />
            ))}
          </div>
        </Tab>
        <Tab eventKey="timeline" title="Timeline">
          <DateGrid
            startDate={new Date(2024, 5, 27)} // June 27, 2024
            endDate={new Date(2024, 6, 15)}   // July 15, 2024
            onDateSelect={handleTimelineDateSelect}
          />
          <div className="records-list">
            {timeline.map((record, index) => (
              <TimelineCard key={index} record={record} />
            ))}
          </div>
          {selectedPicture && <Popup record={selectedPicture} show={!!selectedPicture} handleClose={closePopup} />}
        </Tab>
        <Tab eventKey="stories" title="Stories">
          <div className="records-list">
            {stories.map((record, index) => (
              <StoryCard key={index} record={record} />
            ))}
          </div>
        </Tab>
      </Tabs>
    </div >
  );
}

export default Root;
