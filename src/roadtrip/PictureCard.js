import React from 'react';
import './PictureCard.css'; // Custom CSS for picture styling
import { getImageUrl } from '../utilities';

const PictureCard = ({ record }) => {
    const imgSrc = getImageUrl(record); // Derive image URL from filename

    return (
        <div className="card picture-card">
            <img src={imgSrc} alt={`Picture from ${record.place}`} className="image" />
            <div className="details">
                <p><strong>Place:</strong> {record.place}</p>
                <p><strong>Timestamp:</strong> {new Date(record.timestamp).toLocaleString()}</p>
            </div>
        </div>
    );
};

export default PictureCard;
