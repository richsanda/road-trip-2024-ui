import React from 'react';
import StoryDisplay from '../components/StoryDisplay';
import JsonOutline from './JsonOutline';

const MessageDisplay = ({ record }) => {
    return (
        <div className="message-display" style={{ maxWidth: '90%', width: '100%', margin: '0 auto' }}>
            <div style={{ maxHeight: '70vh', overflowY: 'auto', marginBottom: '8px' }}>
                {record.is_note ? (
                    record.description && <StoryDisplay text={`${record.description}`} />
                ) : record.type === 'shazam' ? (
                    (() => {
                        try {
                            return (
                                <p>
                                    {/* Entire div (title and artist) is clickable */}
                                    <div
                                        onClick={() => window.open(record.data.link, '_blank', 'noopener,noreferrer')}
                                        className='timeline-nav-card'
                                    >
                                        <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>{record.data.title}</span>
                                        <span style={{ marginLeft: '8px' }}>&mdash; {record.data.artist}</span>
                                    </div>
                                </p>

                            );
                        } catch (e) {
                            // If JSON parsing fails, show the raw description
                            return <p>{record.description}</p>;
                        }
                    })()
                ) : (record.type === 'story' && record?.data?.category === 'songs') ? (
                    (() => {
                        try {
                            return (
                                <>
                                    <p>
                                        {/* Entire div (title and artist) is clickable */}
                                        <div
                                            onClick={() => window.open(record.data.song_link, '_blank', 'noopener,noreferrer')}
                                            className='timeline-nav-card'
                                        >
                                            <span style={{ fontWeight: 'bold', marginLeft: '8px', color: 'olive' }}>{record.data.song_name}</span>
                                            <span style={{ marginLeft: '8px' }}>&mdash; {record.data.artist_name}</span>
                                        </div>
                                    </p>
                                    {record.data?.dada_rank && record.data?.dada_rank <= 10 &&
                                        <div style={{ fontStyle: 'italic', color: 'darkblue', fontSize: '1.2em', marginTop: '8px', marginBottom: '16px' }}>
                                            rich's #{record.data.dada_rank}
                                        </div>}
                                    {record.data?.sydney_rank && record.data?.sydney_rank <= 10 &&
                                        <div style={{ fontStyle: 'italic', color: 'darkgreen', fontSize: '1.2em', marginTop: '8px', marginBottom: '16px' }}>
                                            sydney's #{record.data.sydney_rank}
                                        </div>
                                    }
                                </>

                            );
                        } catch (e) {
                            // If JSON parsing fails, show the raw description
                            return <p>{record.description}</p>;
                        }
                    })()
                ) : record.type === 'picture' ? (
                    (() => {
                        const dashText = record.data && record.data.miles || record.data.temp || record.data.mpg
                        try {
                            return (
                                record?.data?.signs ?
                                    <div className='highway-sign'>
                                        <StoryDisplay text={`\n${record.data.signs}`} />
                                    </div>
                                    : record?.data?.sign ?
                                        <>
                                            <div className='sign'>
                                                <StoryDisplay text={`\n${record.data.sign}`} />
                                            </div>
                                            <div style={{ paddingTop: '16px' }}>{record.data.note}</div>
                                        </>
                                        : dashText ?
                                            <>
                                                <div className='dashboard'>
                                                    <StoryDisplay text={`\n${dashText}`} />
                                                </div>
                                                <div style={{ paddingTop: '16px' }}>{record.data.note && record.data.note}</div>
                                            </>
                                            : record?.data?.caption &&
                                            <div style={{ paddingTop: '16px', fontSize: '.9em', color: 'darkbrown' }}>{record.data.caption}</div>
                            );
                        } catch (e) {
                            // If JSON parsing fails, show the raw description
                            return <p>{record.description}</p>;
                        }
                    })()
                ) : record.type === 'message' ? (
                    (() => {
                        try {
                            const messages = record.data;

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
                ) : record.type === 'receipt' || record.type === 'map' ? (
                    <div>{
                        record.data?.category &&
                        <div style={{ fontWeight: 'bold', color: 'olive', fontSize: '1.2em', marginTop: '8px', marginBottom: '16px' }}>
                            {record.data?.category}
                        </div>
                    }
                        {record.data && <div style={{ color: 'darkolivegreen' }}>
                            <JsonOutline data={record.data?.info ? record.data.info : record.data} />
                        </div>}
                    </div>
                ) : record.type === 'story' ? (
                    <>
                        {record.data?.dada_rank && record.data?.dada_rank <= 10 &&
                            <div style={{ fontStyle: 'italic', color: 'darkblue', fontSize: '1.2em', marginTop: '8px', marginBottom: '16px' }}>
                                rich's #{record.data.dada_rank}
                            </div>}
                        {record.data?.sydney_rank && record.data?.sydney_rank <= 10 &&
                            <div style={{ fontStyle: 'italic', color: 'darkgreen', fontSize: '1.2em', marginTop: '8px', marginBottom: '16px' }}>
                                sydney's #{record.data.sydney_rank}
                            </div>
                        }
                    </>
                ) : (
                    record.description && <p>{record.description}</p>
                )}
            </div>
            {/* {record.place && <p>{record.place}</p>} */}
        </div>
    );
};




export default MessageDisplay;
