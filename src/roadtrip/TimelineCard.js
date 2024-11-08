import React, { useEffect, useState } from 'react';
import { Card as BootstrapCard, Button, Form } from 'react-bootstrap';
import { formatISODateTime, getImageUrl, storyTitle } from '../utilities';
import './TimelineCard.css'; // Import the CSS file
import MessageDisplay from './MessageDisplay';

function TimelineCard({ record, onClick, onClickAbove, onClickBelow, onRemove, onSave, defaultEditMode }) {
    const [description, setDescription] = useState(record.description);
    const imageUrl = getImageUrl(record); // Get the correct image URL
    const data = record.data;
    const place = record.type === 'receipt' || record.type === 'map' || record.type === 'picture' ? data?.place || data?.end_place : data;
    const title = record.type === 'story' || record.type === 'note' ? storyTitle(record.description) : null;
    const category = title ? title.includes(':') ? title?.split(":")[0].trim() : null : null;
    const trimmedTitle = title ? title.includes(':') ? title?.split(":")[1].trim() : title.trim() : null;
    const parensTitle = trimmedTitle && trimmedTitle.includes('(') && trimmedTitle.includes(')')
        ? trimmedTitle.substring(
            trimmedTitle.indexOf('(') + 1,
            trimmedTitle.indexOf(')')
        )
        : '';

    const [isEditMode, setEditMode] = useState(defaultEditMode);

    // Determine the width ratio based on record type
    const isPicture = record.type === 'picture';
    const isSigns = isPicture && record?.data?.signs
    const isSign = isPicture && record?.data?.sign
    const isDash = isPicture && record?.data?.miles || record?.data?.temp || record?.data?.mpg
    const isNote = record.is_note;
    const imageWidthClass = isPicture && (isSigns || isSign || isDash) ? 'image-normal' : 
    isPicture ? 'image-wide' : 'image-narrow'; 

    // Effect to sync the textarea with the record description
    useEffect(() => {
        setDescription(record.description);
    }, [record.description]);

    return (
        <BootstrapCard className="card mb-3" onClick={onClick}>
            <BootstrapCard.Body className="card-body">
                {/* Title displayed above the image and text */}
                <div className="card-title">
                    {!isNote && formatISODateTime(record.timestamp, !category || category != 'days')}
                    {' '}
                    <span className='modal-title'>
                        {record.is_note ? (
                            <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>{storyTitle(record.description)}</span>
                        ) : record.type === 'shazam' ? (
                            <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>shazam</span>
                        ) : record.type === 'story' && record.data?.spotify_add ? (
                            <>
                                <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>
                                    {record.data.playlist_owner === 'Sydney' ? 'sydney' : 'rich'}'s playlist add
                                </span>
                                {data.category === 'songs' && (data.dada_rank <= 10 || data.sydney_rank <= 10) &&
                                    <span style={{ fontSize: '.9em', fontWeight: 'normal', marginLeft: '8px' }}>
                                        &nbsp;&nbsp;&nbsp;&nbsp;top 10 songs
                                    </span>
                                }
                            </>
                        ) : record.type === 'picture' || record.type === 'receipt' ? (
                            <span>
                                <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>
                                    {place?.city || place?.county}
                                    {(place?.city || place?.county) && place?.state && ', '}
                                    {place?.state}
                                </span>
                                <span style={{ fontSize: '.9em', fontWeight: 'normal', marginLeft: '8px' }}>
                                   {data?.business} {place?.address}
                                </span>
                            </span>
                        ) : record.type === 'map' ? (
                            <span>
                                <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>
                                    {place?.city}
                                    {place?.state && place?.city && ', '}
                                    {place?.state}
                                </span>
                                <span style={{ fontSize: '.9em', fontWeight: 'normal', marginLeft: '8px' }}>
                                    {place?.address}
                                </span>
                            </span>
                        ) : record.type === 'story' ? (
                            <span>
                                <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>
                                    {category && category === 'days' ? parensTitle : category != 'songs' && trimmedTitle}
                                </span>
                                <span style={{ fontSize: '.9em', fontWeight: 'normal', marginLeft: '8px' }}>
                                    &nbsp;&nbsp;&nbsp;&nbsp;top 10 {category}
                                </span>
                            </span>
                        ) : record.place}
                    </span>
                    {!isNote && (
                        <>
                            {/* <div className="button-container">
                                <Button onClick={onClickAbove}>above</Button>
                                <Button onClick={onClickBelow}>below</Button>
                            </div> */}
                        </>
                    )}
                </div>

                <div className="card-content">
                    {/* Image */}
                    {imageUrl && !isNote && (
                        <img
                            src={imageUrl}
                            alt={imageUrl}
                            className={`card-img ${imageWidthClass}`} // Use the conditional class
                        />
                    )}
                    {!imageUrl && (
                        <div className="card-img-placeholder"></div>
                    )}

                    {/* Text Content or Textarea depending on edit mode */}
                    <div className={`card-text-content ${isPicture ? 'text-normal' : 'text-receipt-map'}`}>
                        {isEditMode && isNote ? (
                            <Form>
                                <Form.Group controlId="storyText">
                                    <Form.Control
                                        as="textarea"
                                        rows={10}
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                    />
                                </Form.Group>
                            </Form>
                        ) : (
                            <div className="card-text">
                                <MessageDisplay record={record} />
                            </div>
                        )}
                    </div>

                    {!isNote ? (
                        <>
                        </>
                    ) : isEditMode ? (
                        <>
                            <div>
                                <Button onClick={() => {
                                    onSave(description);
                                    setEditMode(false);
                                }}>Save</Button>
                            </div>
                            <div>
                                <Button onClick={() => {
                                    setEditMode(false);
                                }}>Cancel</Button>
                            </div>
                        </>
                    ) : (
                        <>
                            {/* <div><Button onClick={() => setEditMode(true)}>Edit</Button></div>
                            <div><Button onClick={onRemove}>Remove</Button></div> */}
                        </>
                    )}
                </div>
            </BootstrapCard.Body>
        </BootstrapCard>
    );
}

export default TimelineCard;
