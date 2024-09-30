import React, { useState } from 'react';
import { Dropdown } from 'react-bootstrap';
import dates from '../data/dates.json'
import { updateMapTimestamp, updateStory } from '../api';
import './DateDropdown.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function DateDropdown({defaultDate, type, id}) {

    const getLabelForValue = (value, data) => {
        const entry = data.find(item => item.value === value);
        return entry ? entry.label : 'Select a date'; 
    };

    const [selectedValue, setSelectedValue] = useState(defaultDate);

    const handleDateChange = (eventKey) => {

        const selected = dates.find(date => date.value === eventKey);
        if (selected) {
            setSelectedValue(selected.value);
            if (type === 'map') {
                updateMapTimestamp(id, selected.value);
            } else if (type === 'story') {
                updateStory(id, selected.value);
            }
        }
    };

    return (
        <Dropdown onSelect={handleDateChange}>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                {selectedValue}
            </Dropdown.Toggle>

            <Dropdown.Menu className="custom-dropdown-menu">
                {dates.map(date => (
                    <Dropdown.Item key={date.value} eventKey={date.value}>
                        {date.label}
                    </Dropdown.Item>
                ))}
            </Dropdown.Menu>
        </Dropdown>
    );
}

export default DateDropdown;
