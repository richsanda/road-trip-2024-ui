import { format } from "date-fns";

const apiUrl = process.env.REACT_APP_API_URL;

export async function fetchPictures(date) {
    try {
        const formattedDate = format(date, 'yyyy-MM-dd');
        const response = await fetch(`${apiUrl}/pictures?start=${formattedDate}T00:00:00&end=${formattedDate}T23:59:00`);
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function fetchShazams() {
    try {
        const response = await fetch(`${apiUrl}/shazams`);
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function fetchSongs() {
    try {
        const response = await fetch(`${apiUrl}/songs`);
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function fetchMessages() {
    try {
        const response = await fetch(`${apiUrl}/messages`, {
            method: 'GET',
            cache: 'no-store' // Ensure no caching
        });
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function fetchTimeline(date) {
    try {
        const formattedDate = format(date, 'yyyy-MM-dd');
        const response = await fetch(`${apiUrl}/timeline?start=${formattedDate}T00:00:00&end=${formattedDate}T23:59:00`);
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function fetchStories() {
    try {
        const response = await fetch(`${apiUrl}/stories`, {
            method: 'GET',
            cache: 'no-store' // Ensure no caching
        });
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function fetchNotes() {
    try {
        const response = await fetch(`${apiUrl}/notes`, {
            method: 'GET',
            cache: 'no-store' // Ensure no caching
        });
        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

export async function updateMapTimestamp(id, timestamp) {
    try {
        const response = await fetch(`${apiUrl}/maps/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                timestamp: timestamp,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        console.log('Timestamp updated successfully');
        return true; // Indicate success
    } catch (error) {
        console.error('Error updating timestamp:', error);
        return false; // Indicate failure
    }
}

export async function updateMapHide(id, hide) {
    try {
        const response = await fetch(`${apiUrl}/maps/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                hide: hide,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        console.log('Hide updated successfully');
        return true; // Indicate success
    } catch (error) {
        console.error('Error updating hide:', error);
        return false; // Indicate failure
    }
}

export async function updateTimelineKeep(type, type_id, keep) {
    try {
        const response = await fetch(`${apiUrl}/timeline/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: type,
                type_id: type_id,
                keep: keep
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        console.log('Hide updated successfully');
        return true; // Indicate success
    } catch (error) {
        console.error('Error updating hide:', error);
        return false; // Indicate failure
    }
}

export async function updateStory(id, date, text) {
    // Create the payload with the optional fields
    const payload = {
        id: id,
        date: date,
        text: text,
    };

    // Filter out fields with null or undefined values
    const filteredPayload = Object.fromEntries(
        Object.entries(payload).filter(([_, value]) => value != null)
    );

    try {
        const response = await fetch(`${apiUrl}/stories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filteredPayload), // Send the filtered payload
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        console.log('Updated successfully');
        return response.json(); // Indicate success
    } catch (error) {
        console.error('Error updating:', error);
        return false; // Indicate failure
    }
}

export async function updateNote(id, type, type_id, position, text, date) {
    // Create the payload with the optional fields
    const payload = {
        id: id,
        type: type,
        type_id: type_id,
        position: position,
        text: text,
        date: date
    };

    // Filter out fields with null or undefined values
    const filteredPayload = Object.fromEntries(
        Object.entries(payload).filter(([_, value]) => value != null)
    );

    try {
        const response = await fetch(`${apiUrl}/notes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filteredPayload), // Send the filtered payload
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        console.log('Updated successfully');
        return response.json(); // Indicate success
    } catch (error) {
        console.error('Error updating:', error);
        return false; // Indicate failure
    }
}

export async function deleteNote(id) {
    // Create the payload with the optional fields
    const payload = {
        id: id
    };

    // Filter out fields with null or undefined values
    const filteredPayload = Object.fromEntries(
        Object.entries(payload).filter(([_, value]) => value != null)
    );

    try {
        const response = await fetch(`${apiUrl}/notes`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filteredPayload), // Send the filtered payload
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        console.log('Updated successfully');
        return response.json(); // Indicate success
    } catch (error) {
        console.error('Error updating:', error);
        return false; // Indicate failure
    }
}