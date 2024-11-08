import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import dates from '../data/dates.json'; // Assuming dates.json is in the same directory
import './DayIndex.css'; // Import your CSS file

function DayIndex({ currentDate, onClick }) {
    return (
        <div className="index-container">
            {dates.map((date, index) => {
                const isActive = new Date(`${date.value}T00:00:00`).toDateString() === currentDate.toDateString();

                return (
                    <div
                        key={index}
                        className={`index-item mb-2 ${isActive ? 'active' : ''}`}
                        onClick={() => onClick(new Date(`${date.value}T00:00:00`))}
                        style={{
                            cursor: 'pointer',
                            ...(isActive ? { fontWeight: 'bold' } : {})
                        }}
                    >
                        {date.label}
                    </div>
                );
            })}
        </div>
    );
}

export default DayIndex;
