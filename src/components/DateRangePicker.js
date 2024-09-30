// src/components/DateRangePicker.js
import React, { useState } from 'react';
import { DateRange } from 'react-date-range';
import { format } from 'date-fns';
import 'react-date-range/dist/styles.css'; // main css file
import 'react-date-range/dist/theme/default.css'; // theme css file

function DateRangePicker({ onDateChange }) {
    // Default to June 27, 2024
    const defaultDate = new Date(2024, 5, 27); // Month is 0-indexed

    const [state, setState] = useState([
        {
            startDate: defaultDate,
            endDate: defaultDate,
            key: 'selection'
        }
    ]);

    // Function to handle date selection with double click
    const handleSelect = (ranges) => {
        const { startDate, endDate } = ranges.selection;
        setState([ranges.selection]);
        onDateChange(startDate, endDate);
    };

    const handleDateClick = (date) => {
        // Handle single date selection (double-click or similar action)
        setState([
            {
                startDate: date,
                endDate: date,
                key: 'selection'
            }
        ]);
        onDateChange(date, date);
    };

    return (
        <div>
            <DateRange
                editableDateInputs={true}
                onChange={handleSelect}
                moveRangeOnFirstSelection={false}
                ranges={state}
                dateDisplayFormat="yyyy-MM-dd"
                // This is a workaround: the date click event needs to be manually handled
                onDayClick={(date) => handleDateClick(date)}
            />
        </div>
    );
}

export default DateRangePicker;
