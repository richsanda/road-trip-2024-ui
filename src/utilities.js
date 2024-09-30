export const formatISODateTime = (isoDateTime) => {
    const date = new Date(isoDateTime);

    // Define options for formatting
    const dateOptions = { month: 'short', day: 'numeric' };
    const timeOptions = { hour: 'numeric', minute: 'numeric', hour12: true };

    // Format date and time
    const formattedDate = date.toLocaleDateString('en-US', dateOptions);
    let formattedTime = date.toLocaleTimeString('en-US', timeOptions);

    // Remove leading zero from day
    const day = date.getDate();
    const month = date.toLocaleString('en-US', { month: 'short' });
    formattedTime = formattedTime.replace(' ', '').replace('M', '').toLowerCase(); // Remove space and convert to lowercase

    // Combine formatted date and time
    return `${month} ${day}, ${formattedTime}`;
};

export const formatTime = (time) => {
    if (!time || typeof time !== 'string' || !/^\d{2}:\d{2}$/.test(time)) {
        return '';
    }

    const [hours, minutes] = time.split(':').map(Number);

    if (isNaN(hours) || isNaN(minutes) || hours < 0 || hours >= 24 || minutes < 0 || minutes >= 60) {
        return '';
    }

    const suffix = hours >= 12 ? 'p' : 'a';
    const formattedHours = hours % 12 || 12; // Convert 0 hours to 12
    return `${formattedHours}:${minutes < 10 ? '0' : ''}${minutes}${suffix}`;
};

export const getDateFromISO = (isoDateTime) => {
    const date = new Date(isoDateTime);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

/**
 * Extracts the first line from the given text.
 * @param {string} text - The input text.
 * @returns {string} - The first line of the text.
 */
export function storyTitle(text) {
    // Split the text into lines and return the first line
    return text.split('\n')[0].trim();
}

/**
 * Extracts everything but the first line from the given text.
 * @param {string} text - The input text.
 * @returns {string} - The body text excluding the first line, with extra line breaks trimmed.
 */
export function storyBody(text) {
    // Split the text into lines, remove the first line, and join the remaining lines
    const lines = text.split('\n');
    const bodyLines = lines.slice(1).filter(line => line.trim() !== '');
    return bodyLines;
}

export function getImageUrl(record) {
    if (record.type === 'map') {
        return `http://localhost:8001/${record.filename}.jpg`;
    } else if (record.type === 'receipt') {
        return `http://localhost:8002/${record.filename}.jpg`;
    } else if (record.type === 'picture') {
        return `http://localhost:8000/${record.filename}.jpg`;
    }
    return null; // Return null if neither 'receipt' nor 'map'
}