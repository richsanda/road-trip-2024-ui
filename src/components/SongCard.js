import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime } from '../utilities';
import './SongCard.css'; // Import the CSS file

function SongCard({ key, record }) {
    return (
        <BootstrapCard className="card">
            <BootstrapCard.Body className="card-body">
                <div className="card-content">
                    <div className="card-text">
                        <BootstrapCard.Text>
                            <a href={record.link} target="_blank" rel="noopener noreferrer">
                                {record.song_name}
                            </a>
                            {'  -  '}
                            {record.artist_name}
                        </BootstrapCard.Text>
                    </div>
                    <div className="card-image">
                        <img
                            src={record.image_link}
                            alt={record.song_name}
                            className="card-img"
                        />
                    </div>
                </div>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default SongCard;
