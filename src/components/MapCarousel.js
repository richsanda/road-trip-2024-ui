import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import DateDropdown from './DateDropdown';
import { formatTime } from '../utilities';
import './MapCarousel.css';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { updateMapHide } from '../api';

const apiUrl = process.env.REACT_APP_API_URL;
const imageUrl = process.env.REACT_APP_IMAGES_URL

function MapCarousel() {
    const [maps, setMaps] = useState([]);

    const fetchMaps = async () => {
        try {
            const response = await fetch(`${apiUrl}/maps`);
            if (!response.ok) {
                throw new Error('Failed to fetch maps');
            }
            const data = await response.json();
            setMaps(data);
        } catch (error) {
            console.error('Error fetching maps:', error);
        }
    };

    useEffect(() => {
        fetchMaps();
    }, []);

    function HideCheckbox({ defaultValue, handleCheckboxChange }) {
        const [checked, setChecked] = useState(defaultValue);
    
        const onCheckboxChange = (event) => {
            const isChecked = event.target.checked;
            setChecked(isChecked); // Update the state
            handleCheckboxChange(isChecked); // Pass the value to your function
        };
    
        return (
            <div className="form-check">
                <input 
                    className="form-check-input" 
                    type="checkbox" 
                    id="flexCheckDefault" 
                    checked={checked} 
                    onChange={onCheckboxChange} 
                />
                <label className="form-check-label" htmlFor="flexCheckDefault">
                    Hide
                </label>
            </div>
        );
    }

    const settings = {
        dots: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
    };

    return (
        <div className="carousel-container">
            <Slider {...settings}>
                {maps.map(map => {
                    const startTimeFormatted = formatTime(map.start_time);
                    const endTimeFormatted = formatTime(map.end_time);
                    const timeDisplay = startTimeFormatted && endTimeFormatted && startTimeFormatted !== endTimeFormatted
                        ? `${startTimeFormatted} - ${endTimeFormatted}`
                        : startTimeFormatted;

                    return (
                        <div key={map.id} className="carousel-slide">
                            <div className="carousel-content">
                                <img src={imageUrl + "/" + map.img_location} alt={`Map from ${map.start_place} to ${map.end_place}`} className="carousel-image" />
                                <div>
                                    <p style={{'display': 'flex', 'alignItems':'center','gap':'10px'}}>
                                        <strong>Date:</strong> 
                                        <DateDropdown defaultDate={map.timestamp} type={'map'} id={map.id}/>
                                    </p>
                                    <p><strong>Time:</strong> {timeDisplay}</p>
                                    <p><strong>From:</strong> {map.start_place}</p>
                                    <p><strong>To:</strong> {map.end_place}</p>
                                    <p><strong>Places:</strong> {map.map_places && map.map_places.join(', ')}</p>
                                    <p>
                                        <HideCheckbox defaultValue={map.hide} handleCheckboxChange={(val) => updateMapHide(map.id, val)}/>
                                    </p>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </Slider>
        </div>
    );
}

export default MapCarousel;
