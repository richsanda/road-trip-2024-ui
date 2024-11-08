// HighwaySign.js
import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';

function HighwaySign({ text, onClick }) {
    return (
        <BootstrapCard 
            className="card mb-3 highway-sign-card" 
            onClick={onClick}
            style={{
                backgroundColor: '#49b853', // Lighter, sunlit green
                color: '#FFFFFF', // White text color
                border: '2px solid #E5E5E5', // Light gray border for subtle contrast
                borderRadius: '5px', // Slight rounding
                boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' // Soft shadow for depth
            }}
        >
            <BootstrapCard.Body className="card-body" style={{ textAlign: 'center' }}>
                <h5 style={{ fontWeight: 'bold', margin: 0 }}>{text}</h5>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default HighwaySign;
