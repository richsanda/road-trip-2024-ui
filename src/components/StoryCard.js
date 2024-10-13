import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime, storyBody, storyTitle } from '../utilities';
import './StoryCard.css'; // Import the CSS file
import DateDropdown from './DateDropdown';
import StoryModal from './StoryModal';
import { useState } from 'react';
import StoryDisplay from './StoryDisplay';

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
