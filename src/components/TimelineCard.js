import React, { useEffect, useState } from 'react';
import { Card as BootstrapCard, Button } from 'react-bootstrap';
import { formatISODateTime, getImageUrl } from '../utilities';
import './TimelineCard.css'; // Import the CSS file
import { updateTimelineKeep } from '../api';
import MessageDisplay from './MessageDisplay';



function TimelineCard({ key, record, onClick }) {
    const imageUrl = getImageUrl(record); // Get the correct image URL

    const [keep, setKeep] = useState(record.keep); // Assuming record.keep is the boolean value
    useEffect(() => {
        setKeep(record.keep);
    }, [record]);

    // Function to handle the button click event
    const handleToggle = async (e) => {
        // Prevent the card's onClick from firing
        e.stopPropagation();

        // Toggle the keep state
        try {
            await updateTimelineKeep(record.type, record.type_id, !record.keep)
                .then((response) => {
                    record.keep = !record.keep;
                    setKeep(record.keep);
                }); // Toggle keep value
            console.log('Toggle success'); // Optional: log success
        } catch (error) {
            console.error('Error toggling keep:', error); // Handle errors
        }
    };

    // Determine button text and styles based on the 'keep' value
    const buttonText = keep ? 'Keep !' : 'Keep ?';
    const buttonVariant = keep ? 'primary' : 'outline-primary';
    const buttonStyle = keep ? { color: 'white', backgroundColor: '#007bff' } : {};

    return (
        <BootstrapCard className="card mb-3" onClick={onClick}>
            <BootstrapCard.Body className="card-body">
                <div className="card-content">
                    {/* Image on the left */}
                    {imageUrl && (
                        <img
                            src={imageUrl}
                            alt="Card image"
                            className="card-img"
                        />
                    )}
                    {!imageUrl && (
                        <div className="card-img-placeholder"></div>
                    )}

                    {/* Text Content */}
                    <div className="card-text-content">
                        <div className="card-title">
                            {formatISODateTime(record.timestamp)}
                            <span className="card-type">
                                {record.type}
                            </span>

                            {/* Toggle Button in the top-right corner */}
                            <Button
                                variant={buttonVariant}
                                className="toggle-btn"
                                onClick={handleToggle}
                                style={{
                                    position: 'absolute',
                                    top: '10px',
                                    right: '10px',
                                    ...buttonStyle // Apply additional styles conditionally
                                }}
                            >
                                {buttonText}
                            </Button>
                        </div>
                        <div className="card-text">
                            <MessageDisplay record={record} />
                        </div>

                    </div>
                </div>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default TimelineCard;
