import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime, storyBody, storyTitle } from '../utilities';
import './StoryCard.css'; // Import the CSS file
import DateDropdown from './DateDropdown';
import StoryModal from './StoryModal';
import { useState } from 'react';

// Utility function to extract lines from the story body
const storyLines = (text) => {
    return storyBody(text).map(line => line.trim()).filter(line => line !== '');
};

// Utility function to determine if a line should be bolded and split it
const splitLine = (line) => {
    const match = /^([^\s]+:)(.*)$/.exec(line);
    if (match) {
        return {
            propertyName: match[1], // Text including the colon
            restOfLine: match[2].trim() // Remaining part of the line
        };
    }
    return {
        propertyName: '',
        restOfLine: line
    };
};

function StoryDisplay({ text }) {
    // Get the array of lines
    const lines = storyLines(text);

    return (
        <div className='story-container'>
            {lines.map((line, index) => {
                const { propertyName, restOfLine } = splitLine(line);
                return (
                    <div key={index} className='story-line'>
                        {propertyName && (
                            <span style={{ fontWeight: 'bold' }}>
                                {propertyName}{'  '}
                            </span>
                        )}
                        {restOfLine}
                    </div>
                );
            })}
        </div>
    );
}

function StoryCard({ record }) {
    const [selectedStory, setSelectedStory] = useState(null);

    const handleCardClick = () => {
        setSelectedStory(record);
    };

    const handleClose = () => {
        setSelectedStory(null);
    };

    const handleDropdownClick = (e) => {
        e.stopPropagation(); // Prevent the dropdown click from propagating to the card click handler
    };

    return (
        <>
            <BootstrapCard className="card mb-3" style={{ cursor: 'pointer' }} onClick={handleCardClick}>
                <BootstrapCard.Body className="card-body">
                    <div className="card-header">
                        <div className="card-title-container">
                            <div className="card-title">
                                {storyTitle(record.text)}
                                <span className="card-type">
                                {'   '}{record.category}{'   '}
                                </span>
                                <span className="card-time">
                                    {record.date && record.time && formatISODateTime(record.date + 'T' + record.time)}
                                </span>
                            </div>
                        </div>
                        <div className="date-dropdown-container" onClick={handleDropdownClick}>
                            <DateDropdown defaultDate={record.date} type={'story'} id={record.id} />
                        </div>
                    </div>
                    <div className="card-body-content">
                        <StoryDisplay text={record.text} />
                    </div>
                </BootstrapCard.Body>
            </BootstrapCard>
            {selectedStory && (
                <StoryModal
                    record={selectedStory}
                    show={!!selectedStory}
                    handleClose={handleClose}
                />
            )}
        </>
    );
}


export default StoryCard;
