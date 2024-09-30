// src/components/DateGrid.js
import React from 'react';
import { format, eachDayOfInterval, startOfWeek, endOfWeek } from 'date-fns';
import './DateGrid.css'; // Add your own styles for the grid

function DateGrid({ startDate, endDate, onDateSelect }) {
    // Generate an array of dates within the range
    const allDates = eachDayOfInterval({ start: startDate, end: endDate });

    // Determine the start and end of the week for calendar view
    const firstDate = startOfWeek(startDate, { weekStartsOn: 0 }); // Sunday
    const lastDate = endOfWeek(endDate, { weekStartsOn: 0 }); // Saturday

    // Generate an array of all dates to display in the calendar view
    const calendarDates = eachDayOfInterval({ start: firstDate, end: lastDate });

    const handleDateClick = (date) => {
        onDateSelect(date);
    };

    return (
        <div className="date-grid">
            <div className="calendar-header">
                <div className="calendar-header-item">Sun</div>
                <div className="calendar-header-item">Mon</div>
                <div className="calendar-header-item">Tue</div>
                <div className="calendar-header-item">Wed</div>
                <div className="calendar-header-item">Thu</div>
                <div className="calendar-header-item">Fri</div>
                <div className="calendar-header-item">Sat</div>
            </div>
            {calendarDates.map(date => (
                <div
                    key={date}
                    className={`date-tile ${allDates.some(d => d.toDateString() === date.toDateString()) ? 'active' : ''}`}
                    onClick={() => handleDateClick(date)}
                >
                    {format(date, 'd')}
                </div>
            ))}
        </div>
    );
}

export default DateGrid;
