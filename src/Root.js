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

function Root() {
  const [pictures, setPictures] = useState([]);
  const [shazams, setShazams] = useState([]);
  const [songs, setSongs] = useState([]);
  const [messages, setMessages] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [stories, setStories] = useState([]);
  const [selectedPicture, setSelectedPicture] = useState(null);

  const handleDateSelect = (date) => {
    fetchPictures(date);
  };

  const handleTimelineDateSelect = (date) => {
    fetchTimeline(date);
  };

  const fetchPictures = async (date) => {
    try {
      const formattedDate = format(date, 'yyyy-MM-dd');
      const response = await fetch(`http://localhost:5000/pictures?start=${formattedDate}T00:00:00&end=${formattedDate}T23:59:00`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setPictures(data);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  const fetchShazams = async () => {
    try {
      const response = await fetch(`http://localhost:5000/shazams`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setShazams(data);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  const fetchSongs = async () => {
    try {
      const response = await fetch(`http://localhost:5000/songs`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setSongs(data);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await fetch('http://localhost:5000/messages', {
        method: 'GET',
        cache: 'no-store' // Ensure no caching
      });
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  const fetchTimeline = async (date) => {
    try {
      const formattedDate = format(date, 'yyyy-MM-dd');
      const response = await fetch(`http://localhost:5000/timeline?start=${formattedDate}T00:00:00&end=${formattedDate}T23:59:00`);
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setTimeline(data);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  const fetchStories = async () => {
    try {
      const response = await fetch('http://localhost:5000/stories', {
        method: 'GET',
        cache: 'no-store' // Ensure no caching
      });
      if (!response.ok) {
        throw new Error('Failed to fetch');
      }
      const data = await response.json();
      setStories(data);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  useEffect(() => {
    // fetchShazams();
    // fetchSongs();
    // fetchMessages();
    // fetchTimeline();
    // fetchStories();
  }, []);

  const fetchMethods = {
    stories: fetchStories,
    songs: fetchSongs,
    messages: fetchMessages,
    timeline: fetchTimeline,
    shazams: fetchShazams
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
