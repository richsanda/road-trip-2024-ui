import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime } from '../utilities';
import './PictureCard.css'; // Import the CSS file

function PictureCard({ record, onClick }) {
    return (
        <BootstrapCard 
            className="card" 
            onClick={onClick}
            style={{
                width: '100%', 
                margin: '0 auto',
                display: 'flex', // Keep the image and text side by side
                alignItems: 'center',
            }}
        >
            {/* Image on the left */}
            {record.img_location && (
                <BootstrapCard.Img 
                    variant="top" 
                    src={record.img_location} 
                    alt="Record" 
                    style={{
                        height: '50vh', // Image height is 80% of the viewport height
                        width: 'auto', // Maintain the aspect ratio
                        marginRight: '20px' // Space between image and text block
                    }}
                />
            )}
            {/* Title block (timestamp above the address) on the right */}
            <BootstrapCard.Body>
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <BootstrapCard.Title>
                        <strong>{formatISODateTime(record.timestamp)}</strong>
                    </BootstrapCard.Title>
                    <BootstrapCard.Text>
                        {record.address}
                    </BootstrapCard.Text>
                </div>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default PictureCard;
