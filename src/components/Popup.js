import React, { useState } from 'react';
import { Modal, Button, Dropdown } from 'react-bootstrap';
import './Popup.css'
import { formatISODateTime, getDateFromISO } from '../utilities';
import DateDropdown from './DateDropdown';
import 'bootstrap/dist/css/bootstrap.min.css';

const imageUrl = process.env.REACT_APP_IMAGES_URL

function Popup({ record, show, handleClose }) {

    const handlePopupClick = (event) => {
        // Prevent click event from propagating to the overlay
        event.stopPropagation();
    };

    return (
        <Modal
            show={show}
            onHide={handleClose}
            dialogClassName="popup-dialog"
            onClick={handlePopupClick} // Prevent click event propagation
        >
            <Modal.Header closeButton>
                <Modal.Title>{formatISODateTime(record.timestamp)} -- {record.address}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {/* <DateDropdown defaultDate={getDateFromISO(record.timestamp)}/> */}
                {record.img_location && <img 
                    src={imageUrl + "/" + record.img_location} 
                    alt="Record" 
                    className="popup-image"
            />}
            </Modal.Body>
        </Modal>
    );
}

export default Popup;