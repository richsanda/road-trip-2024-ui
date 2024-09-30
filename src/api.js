export async function updateMapTimestamp(id, timestamp) {
    try {
        const response = await fetch('http://localhost:5000/maps/update', {
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
        const response = await fetch('http://localhost:5000/maps/update', {
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
        const response = await fetch('http://localhost:5000/stories', {
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

