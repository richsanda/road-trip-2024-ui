import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import DateDropdown from './DateDropdown';
import { formatTime } from '../utilities';
import './ReceiptCarousel.css';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const apiUrl = process.env.REACT_APP_API_URL;
const imageUrl = process.env.REACT_APP_IMAGES_URL

function ReceiptCarousel() {
    const [receipts, setReceipts] = useState([]);

    const fetchReceipts = async () => {
        try {
            const response = await fetch(`${apiUrl}/receipts`);
            if (!response.ok) {
                throw new Error('Failed to fetch maps');
            }
            const data = await response.json();
            setReceipts(data);
        } catch (error) {
            console.error('Error fetching receipts:', error);
        }
    };

    useEffect(() => {
        fetchReceipts();
    }, []);

    const settings = {
        dots: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1
    };

    const ItemsList = ({ items }) => {
        // Function to get the description or name
        const getItemText = (item) => item.description || item.name;
    
        // Generate the comma-separated list
        const itemList = items
            .map(getItemText)
            .filter(Boolean) // Remove any undefined or null values
            .join(', ');
    
        return (
            <div>
                <p>{itemList}</p>
            </div>
        );
    };

    return (
        <div className="carousel-container">
            <Slider {...settings}>
                {receipts.map(receipt => (
                    <div key={receipt.id} className="carousel-slide">
                        <div className="carousel-content">
                            <img src={imageUrl + "/" + receipt.img_location} alt={`Receipt from ${receipt.place}`} className="carousel-image" />
                            <div>
                                <p style={{ 'display': 'flex', 'alignItems': 'center', 'gap': '10px' }}>
                                    <strong>Date:</strong>
                                    <DateDropdown defaultDate={receipt.timestamp} type={'receipt'} id={receipt.id} />
                                </p>
                                <p><strong>Time:</strong> {formatTime(receipt.time)}</p>
                                <p><strong>Place:</strong> {receipt.place}</p>
                                <p style={{ userSelect: 'text' }}><strong>Items:</strong> <ItemsList items={receipt.record.items} /></p>
                                {/* {<p>
                                    <strong>Text:</strong>
                                    <pre style={{
                                        backgroundColor: '#f5f5f5',
                                        padding: '10px',
                                        borderRadius: '4px',
                                        overflowX: 'auto'
                                    }}>
                                        {receipt.text}
                                    </pre>
                                </p> } */}
                            </div>
                        </div>
                    </div>
                ))
                }
            </Slider>
        </div>
    );
}

export default ReceiptCarousel;
