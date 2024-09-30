import React, { useState } from 'react';
import './PopupImage.css'

function PopupImage({ src }) {
    const [magnifierStyle, setMagnifierStyle] = useState({
        visibility: 'hidden',
        top: '0px',
        left: '0px',
        backgroundPosition: '0% 0%',
    });

    const handleMouseMove = (e) => {
        const { top, left, width, height } = e.target.getBoundingClientRect();
        const x = e.clientX - left;
        const y = e.clientY - top;

        // Calculate background position relative to the image
        const bgPosX = ((x / width) * 100);
        const bgPosY = ((y / height) * 100);

        // Adjust position and visibility of magnifier
        setMagnifierStyle({
            visibility: 'visible',
            top: `${y - 50}px`, // Center magnifier on the mouse Y position
            left: `${x - 50}px`, // Center magnifier on the mouse X position
            backgroundPosition: `${bgPosX}% ${bgPosY}%`,
        });
    };

    const handleMouseLeave = () => {
        setMagnifierStyle({ visibility: 'hidden' });
    };

    return (
        <div 
            className="popup-image-wrapper"
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
        >
            <img 
                src={src} 
                alt="Record" 
                className="popup-image"
            />
            <div 
                className="magnifier" 
                style={{
                    ...magnifierStyle,
                    backgroundImage: `url(${src})`,
                }}
            />
        </div>
    );
}

export default PopupImage;
