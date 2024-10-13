import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import { formatISODateTime, getImageUrl } from '../utilities';
import 'bootstrap/dist/css/bootstrap.min.css';
import './TimelineModal.css';
import { updateTimelineKeep } from '../api';
import MessageDisplay from './MessageDisplay';

function TimelineModal({ records, initialIndex, show, handleClose }) {
    const [currentIndex, setCurrentIndex] = useState(initialIndex);
    const [keep, setKeep] = useState(records[initialIndex]?.keep || false); // Initialize keep state

    // Get the current record based on currentIndex
    const currentRecord = records[currentIndex];
    const imageUrl = getImageUrl(currentRecord);

    const handlePrevious = () => {
        setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : prevIndex));
        setKeep(records[currentIndex - 1]?.keep || false); // Update keep state for the new record
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex < records.length - 1 ? prevIndex + 1 : prevIndex));
        setKeep(records[currentIndex + 1]?.keep || false); // Update keep state for the new record
    };

    const handleToggle = async () => {
        try {
            await updateTimelineKeep(currentRecord.type, currentRecord.type_id, !currentRecord.keep);
            setKeep((prevKeep) => !prevKeep); // Toggle keep value
            currentRecord.keep = !currentRecord.keep; // Update the current record's keep state
            console.log('Toggle success');
        } catch (error) {
            console.error('Error toggling keep:', error);
        }
    };

    const handlePopupClick = (event) => {
        event.stopPropagation();
    };

    const description = JSON.parse(currentRecord.description);

    return (
        <Modal
            show={show}
            onHide={handleClose}
            dialogClassName="popup-dialog"
            contentClassName="modal-height"
            onClick={handlePopupClick}
        >
            <Modal.Header closeButton style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ flex: 1 }}>
                    <Modal.Title>
                        {formatISODateTime(currentRecord.timestamp)}
                        <span className='modal-title'>
                            {currentRecord.type === 'shazam' ? (
                                <span>
                                    <a href={description.link} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: '#007bff' }}>
                                        {description.title}
                                    </a>
                                    <span style={{ fontWeight: 'bold', marginLeft: '8px' }}> &mdash; {description.artist}</span>
                                </span>
                            )
                                : currentRecord.type === 'picture' || currentRecord.type === 'receipt' ? (
                                    <span>
                                        <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>
                                            {description?.city || description?.county}
                                            {(description?.city || description?.county) && description?.state && ', '}
                                            {description?.state}
                                        </span>
                                        <span style={{ fontWeight: 'normal', marginLeft: '8px' }}>  {description?.business} {description?.address}</span>
                                    </span>
                                )
                                    : currentRecord.type === 'map' ? (
                                        <span>
                                            <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>
                                                {description?.place?.city}
                                                {description?.place?.state && description?.place?.city && ', '}
                                                {description?.place.state}
                                            </span>
                                            <span style={{ fontWeight: 'normal', marginLeft: '8px' }}>  {description.place.address}</span>
                                        </span>
                                    )
                                        : currentRecord.place}
                        </span>
                    </Modal.Title>
                </div>
                {/* Toggle Button in the Title Box */}
                <Button
                    variant={keep ? 'primary' : 'outline-primary'}
                    onClick={handleToggle}
                    style={{
                        marginRight: '16px', // Increased margin to 26px
                        ...(keep ? { color: 'white', backgroundColor: '#007bff' } : {})
                    }}
                >
                    {keep ? 'Keep !' : 'Keep ?'}
                </Button>
            </Modal.Header>
            <Modal.Body style={{ display: 'flex', justifyContent: 'center' }}>
                {imageUrl ? (
                    <img
                        src={imageUrl}
                        alt="Record"
                        className="popup-image"
                    />
                ) : (
                    <div style={{ width: '60%' }}>
                        <MessageDisplay record={currentRecord} />
                    </div>
                )}
            </Modal.Body>
            <button
                className="carousel-control-prev"
                onClick={handlePrevious}
                disabled={currentIndex === 0}
            >
                &#10094; {/* Left Arrow */}
            </button>
            <button
                className="carousel-control-next"
                onClick={handleNext}
                disabled={currentIndex === records.length - 1}
            >
                &#10095; {/* Right Arrow */}
            </button>
        </Modal >
    );
}


export default TimelineModal;

