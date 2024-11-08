import React from 'react';
import './MapCard.css'; // Custom CSS for map styling
import { getImageUrl } from '../utilities';

const MapCard = ({ record }) => {
    const imgSrc = getImageUrl(record);

    return (
        <div className="card map-card">
            <img src={imgSrc} alt={`Map from ${record.data.place.address} to ${record.data.end_place.address}`} className="image" />
            <div className="details">
                <p><strong>From:</strong> {record.data.place.address || 'Unknown'}</p>
                <p><strong>To:</strong> {record.data.end_place.address || 'Unknown'}</p>
                <p><strong>Timestamp:</strong> {new Date(record.timestamp).toLocaleString()}</p>
            </div>
        </div>
    );
};

export default MapCard;
