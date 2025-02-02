require('dotenv').config();
const { createClient } = require('pexels');

const client = createClient(process.env.PEXELS_API_KEY);

async function searchPexels(query) {
    try {
        const response = await client.photos.search({ 
            query: query,
            per_page: 1,
            orientation: 'square'  // Better for recipe cards
        });
        
        return response.photos.length > 0 
            ? response.photos[0].src.medium
            : process.env.DEFAULT_IMAGE_URL;

    } catch (error) {
        console.error('Error fetching from Pexels:', error);
        return process.env.DEFAULT_IMAGE_URL;
    }
}

// Get query from command line arguments
const query = process.argv[2];
searchPexels(query)
    .then(url => console.log(url))
    .catch(() => console.log(process.env.DEFAULT_IMAGE_URL));