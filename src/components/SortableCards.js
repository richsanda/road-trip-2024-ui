import React, { useState, useEffect } from 'react';
import { Dropdown, DropdownButton } from 'react-bootstrap';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { formatISODateTime, formatTime, storyTitle } from '../utilities';
import StoryDisplay from './StoryDisplay';
import dates from '../data/dates.json'

const apiUrl = process.env.REACT_APP_API_URL;

const getLabelForValue = (value, data) => {
    const entry = data.find(item => item.value === value);
    return entry ? entry.label : 'Select a date';
};

// Helper function to fetch categories from the updated endpoint
async function fetchCategories() {
    const response = await fetch(`${apiUrl}/stories/categories`);
    if (!response.ok) throw new Error('Failed to fetch categories');
    return response.json();
}

// Helper function to fetch stories by category and ranker
async function fetchStories(category, ranker) {
    const response = await fetch(`${apiUrl}/stories?category=${category}&ranker=${ranker}`);
    if (!response.ok) throw new Error('Failed to fetch stories');
    return response.json();
}

// Helper function to save reordered story ranks
async function saveRanks(category, ranker, rankedStories) {
    const rankedData = rankedStories.map((story, index) => ({
        id: story.id,
        rank: index + 1 // rank starts from 1
    }));

    try {
        const response = await fetch(`${apiUrl}/stories/ranks?ranker=${ranker}&category=${category}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(rankedData),
        });

        if (!response.ok) {
            throw new Error('Failed to save story ranks');
        }

        console.log('Story ranks saved successfully');
    } catch (error) {
        console.error('Error saving story ranks:', error);
    }
}

function SortableStories() {
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [stories, setStories] = useState([]);
    const [ranker, setRanker] = useState('dada'); // Hard-coded ranker dropdown

    // Fetch categories on component mount
    useEffect(() => {
        const getCategories = async () => {
            try {
                const categories = await fetchCategories();
                setCategories(categories);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };

        getCategories();
    }, []);

    // Fetch stories when a category or ranker is selected
    useEffect(() => {
        if (selectedCategory && ranker) {
            const getStories = async () => {
                try {
                    const fetchedStories = await fetchStories(selectedCategory, ranker);
                    setStories(fetchedStories);
                } catch (error) {
                    console.error('Error fetching stories:', error);
                }
            };

            getStories();
        }
    }, [selectedCategory, ranker]);

    // Handle drag end (reordering)
    const handleOnDragEnd = (result) => {
        if (!result.destination) return;

        const reorderedStories = Array.from(stories);
        const [movedStory] = reorderedStories.splice(result.source.index, 1);
        reorderedStories.splice(result.destination.index, 0, movedStory);

        setStories(reorderedStories);

        // Save the new order via POST to the endpoint
        saveRanks(selectedCategory, ranker, reorderedStories);
    };

    return (
        <div style={{ padding: '20px' }}>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
                {/* Ranker Dropdown */}
                <DropdownButton id="ranker-dropdown" title={`Ranker: ${ranker}`}>
                    <Dropdown.Item onClick={() => setRanker('dada')}>dada</Dropdown.Item>
                    <Dropdown.Item onClick={() => setRanker('sydney')}>sydney</Dropdown.Item>
                </DropdownButton>

                {/* Category Dropdown */}
                <DropdownButton id="dropdown-basic-button" title="Select Category">
                    {categories.map(category => (
                        <Dropdown.Item
                            key={category}
                            onClick={() => setSelectedCategory(category)}
                        >
                            {category}
                        </Dropdown.Item>
                    ))}
                </DropdownButton>
            </div>

            {selectedCategory && (
                <>
                    <h2>Stories in "{selectedCategory}" (Ranker: {ranker})</h2>

                    {/* Sortable stories */}
                    <DragDropContext onDragEnd={handleOnDragEnd}>
                        <Droppable droppableId="stories">
                            {(provided) => (
                                <div
                                    {...provided.droppableProps}
                                    ref={provided.innerRef}
                                    style={{ padding: 16, backgroundColor: '#f0f0f0', borderRadius: 4 }}
                                >
                                    {stories.map((story, index) => (
                                        <Draggable key={story.id} draggableId={String(story.id)} index={index}>
                                            {(provided, snapshot) => (
                                                <div
                                                    ref={provided.innerRef}
                                                    {...provided.draggableProps}
                                                    {...provided.dragHandleProps}
                                                    style={{
                                                        userSelect: 'none',
                                                        padding: 8,
                                                        marginBottom: 4,
                                                        backgroundColor: snapshot.isDragging ? '#d3d3d3' : '#ffffff',
                                                        border: '1px solid #ddd',
                                                        borderRadius: 4,
                                                        ...provided.draggableProps.style,
                                                    }}
                                                >
                                                    <p><strong>{index + 1}. {storyTitle(story.text)}</strong>{' ~'}{story.time && formatTime(story.time)}, {story.date && getLabelForValue(story.date, dates)}
                                                    <StoryDisplay text={story.text} /></p>
                                                </div>
                                            )}
                                        </Draggable>
                                    ))}
                                    {provided.placeholder}
                                </div>
                            )}
                        </Droppable>
                    </DragDropContext>
                </>
            )}
        </div>
    );
}

export default SortableStories;
