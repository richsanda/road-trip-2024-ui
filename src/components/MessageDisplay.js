import React from 'react';

const MessageDisplay = ({ record }) => {
    return (
        <div className="message-display" style={{ maxWidth: '80%', width: '100%', margin: '0 auto' }}>
            <div style={{ maxHeight: '70vh', overflowY: 'auto', marginBottom: '8px' }}>
                {record.type === 'shazam' ? (
                    (() => {
                        try {
                            // Parse the description JSON for shazam records
                            const { title, artist, link } = JSON.parse(record.description);

                            return (
                                <p>
                                    {/* Song title as a clickable link */}
                                    <a href={link} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: '#007bff' }}>
                                        {title}
                                    </a>
                                    {/* Separator and artist name in a span */}
                                    <span style={{ fontWeight: 'bold', marginLeft: '8px' }}> &mdash; {artist}</span>
                                </p>
                            );
                        } catch (e) {
                            // If JSON parsing fails, show the raw description
                            return <p>{record.description}</p>;
                        }
                    })()
                ) : record.type === 'message' ? (
                    (() => {
                        try {
                            const messages = JSON.parse(record.description);

                            if (Array.isArray(messages)) {
                                return messages.map((message, index) => (
                                    <div
                                        key={index}
                                        style={{
                                            display: 'flex',
                                            justifyContent: message.sender_name.toLowerCase() === 'rich' ? 'flex-end' : 'flex-start',
                                            marginBottom: '8px'
                                        }}
                                    >
                                        <div
                                            style={{
                                                backgroundColor: message.sender_name.toLowerCase() === 'rich' ? '#007bff' : '#e1e1e1',
                                                color: message.sender_name.toLowerCase() === 'rich' ? '#fff' : '#000',
                                                borderRadius: '10px',
                                                padding: '10px',
                                                maxWidth: '80%',
                                                width: 'auto',
                                                wordWrap: 'break-word',
                                                display: 'flex',
                                                alignItems: 'center',
                                                flexDirection: message.sender_name.toLowerCase() === 'rich' ? 'row' : 'row-reverse',
                                            }}
                                        >
                                            <span style={{ marginLeft: '8px', marginRight: '8px' }}>{message.message}</span>
                                            <span
                                                style={{
                                                    fontSize: '0.75em',
                                                    color: message.sender_name.toLowerCase() === 'rich' ? '#ddd' : '#888',
                                                    padding: '5px',
                                                    order: message.sender_name.toLowerCase() === 'rich' ? 1 : 0,
                                                    whiteSpace: 'nowrap',
                                                }}
                                            >
                                                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </span>
                                        </div>
                                    </div>
                                ));
                            } else {
                                return <p>{record.description}</p>;
                            }
                        } catch (e) {
                            return <p>{record.description}</p>;
                        }
                    })()
                ) : (
                    record.description && <p>{record.description}</p>
                )}
            </div>
            {record.place && <p>{record.place}</p>}
        </div>
    );
};




export default MessageDisplay;
