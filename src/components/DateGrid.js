// src/components/DateGrid.js
import './DateGrid.css'; // Add your own styles for the grid

import React, { useState } from 'react';
import { eachDayOfInterval, startOfWeek, endOfWeek, format, isSameDay } from 'date-fns';

function DateGrid({ startDate, endDate, onDateSelect }) {
    const [selectedDate, setSelectedDate] = useState(null);

    // Generate an array of dates within the range
    const allDates = eachDayOfInterval({ start: startDate, end: endDate });

    // Determine the start and end of the week for calendar view
    const firstDate = startOfWeek(startDate, { weekStartsOn: 0 }); // Sunday
    const lastDate = endOfWeek(endDate, { weekStartsOn: 0 }); // Saturday

    // Generate an array of all dates to display in the calendar view
    const calendarDates = eachDayOfInterval({ start: firstDate, end: lastDate });

    const handleDateClick = (date) => {
        if (allDates.some(d => d.toDateString() === date.toDateString())) {
            setSelectedDate(date);
            onDateSelect(date);
        }
    };

    return (
        <div className="date-grid">
            <div className="calendar-header">
                <div className="calendar-header-item">s</div>
                <div className="calendar-header-item">m</div>
                <div className="calendar-header-item">t</div>
                <div className="calendar-header-item">w</div>
                <div className="calendar-header-item">t</div>
                <div className="calendar-header-item">f</div>
                <div className="calendar-header-item">s</div>
            </div>
            {calendarDates.map(date => {
                const isActive = allDates.some(d => d.toDateString() === date.toDateString());
                const isSelected = selectedDate && isSameDay(selectedDate, date);
                
                return (
                    <div
                        key={date}
                        className={`date-tile ${isActive ? 'active' : 'inactive'} ${isSelected ? 'selected' : ''}`}
                        onClick={() => handleDateClick(date)}
                        style={{ cursor: isActive ? 'pointer' : 'not-allowed' }}
                    >
                        {format(date, 'd')}
                    </div>
                );
            })}
        </div>
    );
}

export default DateGrid;
