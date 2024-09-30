import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime, getImageUrl } from '../utilities';
import './TimelineCard.css'; // Import the CSS file

function TimelineCard({ key, record, onClick }) {

    const imageUrl = getImageUrl(record); // Get the correct image URL

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
                </div>
                <div className="card-text">
                    {record.description && <p>{record.description}</p>}
                    {record.place && <p>{record.place}</p>}
                </div>
            </div>
        </div>
    </BootstrapCard.Body>
</BootstrapCard>

    );
}

export default TimelineCard;
