import React from 'react';
import { Card as BootstrapCard } from 'react-bootstrap';
import { formatISODateTime, storyBody, storyTitle } from '../utilities';
import './StoryCard.css'; // Import the CSS file
import DateDropdown from './DateDropdown';
import StoryModal from './StoryModal';
import { useState } from 'react';

// Utility function to extract lines from the story body
const storyLines = (text) => {
    return storyBody(text).map(line => line.trim()).filter(line => line !== '');
};

// Utility function to determine if a line should be bolded and split it
const splitLine = (line) => {
    const match = /^([^\s]+:)(.*)$/.exec(line);
    if (match) {
        return {
            propertyName: match[1], // Text including the colon
            restOfLine: match[2].trim() // Remaining part of the line
        };
    }
    return {
        propertyName: '',
        restOfLine: line
    };
};

function StoryDisplay({ text }) {
    // Get the array of lines
    const lines = storyLines(text);

    return (
        <div className='story-container'>
            {lines.map((line, index) => {
                const { propertyName, restOfLine } = splitLine(line);
                return (
                    <div key={index} className='story-line'>
                        {/* {propertyName && (
                            <span style={{ fontWeight: 'bold' }}>
                                {propertyName}{'  '}
                            </span>
                        )} */}
                        {!propertyName && restOfLine}
                    </div>
                );
            })}
        </div>
    );
}

export default StoryDisplay;
