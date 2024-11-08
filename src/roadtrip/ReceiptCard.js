import React from 'react';
import './ReceiptCard.css'; // Custom CSS for receipt styling
import { getImageUrl } from '../utilities';

const ReceiptCard = ({ record }) => {
    const imgSrc = getImageUrl(record);

    return (
        <div className="card receipt-card">
            <img src={imgSrc} alt={`Receipt from ${record.data.business}`} className="image" />
            <div className="details">
                <p><strong>Business:</strong> {record.data.business}</p>
                <p><strong>Address:</strong> {record.data.address}</p>
                <p><strong>Timestamp:</strong> {new Date(record.timestamp).toLocaleString()}</p>
            </div>
        </div>
    );
};

export default ReceiptCard;
