import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import './Popup.css';
import { formatISODateTime, getDateFromISO } from '../utilities';
import DateDropdown from './DateDropdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import { updateStory } from '../api';

function StoryModal({ record, show, handleClose }) {
    const [editedText, setEditedText] = useState(record ? record.text : '');

    useEffect(() => {
        if (record) {
            setEditedText(record.text);
        }
    }, [record]);

    const handlePopupClick = (event) => {
        // Prevent click event from propagating to the overlay
        event.stopPropagation();
    };

    const handleUpdate = () => {
        // Call the updateStory function with record.id, passing null for date, and the edited text
        updateStory(record.id, null, editedText)
            .then((response) => {
                record.text = editedText
                record.time = response.time
                handleClose();  // Close the modal after the update is successful
            })
            .catch(error => {
                console.error('Error updating story:', error);
                // Optionally, you can add error handling here
            });
    };    

    const dateTime = record.time ? `${record.date}T${record.time}` : record.date;

    return (
        <Modal
            show={show}
            onHide={handleClose}
            dialogClassName="popup-dialog"
            onClick={handlePopupClick} // Prevent click event propagation
        >
            <Modal.Header closeButton>
                <Modal.Title>{formatISODateTime(dateTime)}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group controlId="storyText">
                        <Form.Label>Story Text</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={10}
                            value={editedText}
                            onChange={(e) => setEditedText(e.target.value)}
                        />
                    </Form.Group>
                    <DateDropdown defaultDate={getDateFromISO(record.date)} />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleUpdate}>
                    Save Changes
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default StoryModal;
