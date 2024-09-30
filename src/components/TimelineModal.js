import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import { formatISODateTime, getImageUrl } from '../utilities';
import 'bootstrap/dist/css/bootstrap.min.css';
import './TimelineModal.css';

function TimelineModal({ records, initialIndex, show, handleClose }) {
    const [currentIndex, setCurrentIndex] = useState(initialIndex);

    // Get the current record based on currentIndex
    const currentRecord = records[currentIndex];
    const imageUrl = getImageUrl(currentRecord);

    const handlePrevious = () => {
        setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : prevIndex));
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex < records.length - 1 ? prevIndex + 1 : prevIndex));
    };

    const handlePopupClick = (event) => {
        event.stopPropagation();
    };

    return (
        <Modal
            show={show}
            onHide={handleClose}
            dialogClassName="popup-dialog"
            contentClassName="modal-height"
            onClick={handlePopupClick}
        >
            <Modal.Header closeButton>
                <Modal.Title>
                    {formatISODateTime(currentRecord.timestamp)}
                    <span className='modal-title'>
                        {currentRecord.place || currentRecord.description}
                    </span>
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {imageUrl && (
                    <img
                        src={imageUrl}
                        alt="Record"
                        className="popup-image"
                    />
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
        </Modal>
    );
}

export default TimelineModal;

