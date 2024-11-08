import React, { useState, useEffect, useRef } from 'react';
import { Card as BootstrapCard, Button } from 'react-bootstrap';
import './Timeline.css'; // Custom CSS for the timeline layout
import { deleteNote, fetchTimeline, updateNote } from '../api';
import TimelineCard from './TimelineCard';
import dates from '../data/dates.json'; // Assuming your dates.json is located in the same directory
import { dayOfTrip } from '../utilities';
import DayIndex from './DayIndex';
import HighwaySign from './HighwaySign';
import { signOut } from 'firebase/auth';
import { auth } from '../firebase';

function DayNavCard({ onClick, dateIndex, prev }) {
    const linkText = prev ? `<— previous day: ${dates[dateIndex].label}` : `next day: ${dates[dateIndex].label} —>`;
    return (
        <BootstrapCard style={{ textAlign: 'center', alignItems: 'center', padding: '10px;' }} className="card mb-3 timeline-nav" onClick={onClick}>
            <BootstrapCard.Body style={{ textAlign: 'center', alignItems: 'center' }} className="card-body" >
                <div className="card-title">
                    <span style={{ color: 'darkolivegreen' }} className='modal-title'>{linkText}</span>
                </div>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

const Timeline = () => {
    const [currentDate, setCurrentDate] = useState(new Date(`${dates[0].value}T00:00:00`)); // Default to the first day
    const [records, setRecords] = useState([]);

    const [isEditMode, setIsEditMode] = useState(false);

    const timelineRef = useRef(null); // Ref for the timeline content

    const handleLogout = () => {
        signOut(auth);
    };

    const handleRemove = (record) => {
        deleteNote(record.id);
        setRecords((prevRecords) => prevRecords.filter(other => !other.is_note || (other.ref !== record.ref && other.ref_type !== record.ref_type)));
    };

    const handleSave = (record, text) => {
        record.description = text;
        updateNote(record.id, record.type, record.type_id, record.position, text)
            .then(result => {
                record.id = result.id;
                console.log(JSON.stringify(result));
            });
    }

    // Function to handle clicking on a card to add new cards with properties like type and position
    const handleNew = (clickedRecord, position) => {
        const newRecord = {
            type_id: clickedRecord.type_id,
            type: clickedRecord.type,
            position: position,
            is_note: true,
            description: ''
        };

        setRecords((prevRecords) => {
            const clickedIndex = prevRecords.findIndex((record) => record.id === clickedRecord.id);

            if (clickedIndex === -1) return prevRecords;

            const updatedRecords = [...prevRecords];

            // Insert above or below based on position
            if (position === 'above') {
                updatedRecords.splice(clickedIndex, 0, newRecord);
            } else if (position === 'below') {
                updatedRecords.splice(clickedIndex + 1, 0, newRecord);
            }

            return updatedRecords;
        });
    };

    const handleTimelineDateSelect = (date) => {
        setCurrentDate(date); // Only set the new date

        if (timelineRef.current) {
            const titleHeight = document.querySelector('.timeline-title').offsetHeight; // Dynamically calculate title height
            timelineRef.current.scrollTo({
                top: -titleHeight,  // Adjust by title height
                behavior: 'smooth'  // Smooth scrolling to the top
            });
        }
    };

    useEffect(() => {
        // Fetch the timeline whenever currentDate changes
        fetchTimeline(currentDate).then(response => setRecords(response));
    }, [currentDate]); // Dependency array watches currentDate    

    const renderRecord = (record) => {
        return (
            record.is_note && record?.description?.startsWith('signs') ? (
                <HighwaySign text={record.description} />
            ) : (
                <div key={record.id}>
                    <TimelineCard
                        record={record}
                        currentDate={currentDate}
                        onClickAbove={() => handleNew(record, 'above')}
                        onClickBelow={() => handleNew(record, 'below')}
                        onRemove={() => handleRemove(record)}
                        onSave={(description) => handleSave(record, description)}
                        defaultEditMode={isEditMode}
                    />
                </div>
            )
        );
    };

    const getCurrentDateIndex = () => {
        return dayOfTrip(currentDate) - 1;
    };

    const handlePreviousClick = () => {
        const currentIndex = getCurrentDateIndex();
        if (currentIndex > 0) {
            const previousDate = new Date(`${dates[currentIndex - 1].value}T00:00:00`);
            handleTimelineDateSelect(previousDate);
        }
    };

    const handleNextClick = () => {
        const currentIndex = getCurrentDateIndex();
        if (currentIndex < dates.length - 1) {
            const nextDate = new Date(`${dates[currentIndex + 1].value}T00:00:00`);
            handleTimelineDateSelect(nextDate);
        }
    };

    return (
        <>
            <div className="timeline-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>me and sydney's road trip jun / jul 2024</span>
                <Button style={{ backgroundColor: '#49b853', border: '2px solid #E5E5E5'}} onClick={handleLogout}>Logout</Button>
            </div>
            <div className="timeline-layout">
                {/* Left index (days of the road trip) */}
                <DayIndex currentDate={currentDate} onClick={handleTimelineDateSelect} />

                {/* Right section for the cards */}
                <div className="timeline-content" ref={timelineRef}>
                    {getCurrentDateIndex() > 0 && (
                        <DayNavCard onClick={handlePreviousClick} dateIndex={getCurrentDateIndex() - 1} prev={true} />
                    )}

                    {records.map(renderRecord)}

                    {getCurrentDateIndex() < dates.length - 1 && (
                        <DayNavCard onClick={handleNextClick} dateIndex={getCurrentDateIndex() + 1} />
                    )}
                </div>
            </div>
        </>
    );
};

export default Timeline;
