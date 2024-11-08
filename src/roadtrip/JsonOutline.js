import React from 'react';

function JsonOutline({ data }) {
    const renderJson = (json) => {
        return Object.entries(json).map(([key, value]) => {
            // Handle arrays as bulleted lists
            if (Array.isArray(value)) {
                return (
                    <div key={key} style={{ marginLeft: '20px' }}>
                        <strong>{key}:</strong>
                        <ul>
                            {value.map((item, index) => (
                                <li key={index} style={{ marginLeft: '20px' }}>
                                    {typeof item === 'object' ? renderJson(item) : item}
                                </li>
                            ))}
                        </ul>
                    </div>
                );
            }
            // Recursively render objects
            else if (typeof value === 'object' && value !== null) {
                return (
                    <div key={key} style={{ marginLeft: '20px' }}>
                        <strong>{key}:</strong>
                        {renderJson(value)}
                    </div>
                );
            }
            // Render non-object values
            else {
                return (
                    <div key={key} style={{ marginLeft: '20px' }}>
                        <strong>{key}:</strong> {value}
                    </div>
                );
            }
        });
    };

    return <div>{renderJson(data)}</div>;
}

export default JsonOutline;
