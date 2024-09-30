import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime } from '../utilities';
import './ShazamCard.css'; // Import the CSS file

function MessageCard({ key, record }) {
    return (
        <BootstrapCard
            className="card"
        >
            <BootstrapCard.Body>
                <BootstrapCard.Title>
                    {formatISODateTime(record.timestamp)}
                </BootstrapCard.Title>
                <BootstrapCard.Text>
                    <div style={{
                        padding: '8px'
                     }}>
                        {record.sender_name}{': '}{record.content}
                    </div>
                </BootstrapCard.Text>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default MessageCard;
