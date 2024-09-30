import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime } from '../utilities';
import './ShazamCard.css'; // Import the CSS file

function ShazamCard({ key, record }) {
    return (
        <BootstrapCard
            className="card"
        >
            <BootstrapCard.Body>
                <BootstrapCard.Title>
                    {formatISODateTime(record.date + 'T' + record.time)}
                </BootstrapCard.Title>
                <BootstrapCard.Text>
                        <a href={record.link} target="_blank" rel="noopener noreferrer">
                            {record.title}
                        </a>
                        {'  -  '}
                        {record.artist}
                </BootstrapCard.Text>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default ShazamCard;
