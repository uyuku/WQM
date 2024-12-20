import axios from 'axios'

export const evaluateWaterQuality = async (data) => {
    try {
        const response = await axios.post(`/evaluate`, data);
        return response.data;
    } catch (error) {
        console.error("Error evaluating water quality:", error);
        if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            throw new Error(error.response.data.detail || "An error occurred while evaluating water quality.");
        } else if (error.request) {
            // The request was made but no response was received
            throw new Error("The server did not respond. Please check your connection.");
        } else {
            // Something happened in setting up the request that triggered an Error
            throw new Error("An error occurred while setting up the request.");
        }
    }
};
