import express from 'express';
import fetch from 'node-fetch';
import redis from 'redis';
import dotenv from 'dotenv';

dotenv.config();

const PORT = process.env.PORT || 4000;
const REDIS_PORT = process.env.REDIS_PORT || 6379;
const CACHE_DURATION = 7 * 24 * 60 * 60; // 7 days in seconds
const FASTAPI_URL = process.env.FASTAPI_URL;

const client = redis.createClient(REDIS_PORT);

const app = express();

// Helper function: Fetch data from FastAPI and cache in Redis
async function getAndCacheEvents(req, res, next) {
    try {
        const { location, event_preferences, date } = req.body;

        console.log('Fetching Data...');

        // Fetch data from FastAPI
        const response = await fetch(`${FASTAPI_URL}/get_event`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                event_preferences: event_preferences,
                date: date,
            })
        });
        const data = await response.json();

        // Save the data to Redis, set the expiration time for caching
        client.setex(`${location}:${category}:${date}`, CACHE_DURATION, JSON.stringify(data));

        res.send(data);

    } catch (err) {
        console.error(err);
        res.status(500);
    }
}

// Cache middleware
function cache(req, res, next) {
    const { location, event_preferences, date } = req.body;

    client.get(`${location}:${event_preferences}:${date}`, (err, data) => {
        if (err) throw err;

        if (data !== null) {
            res.send(JSON.parse(data));
        } else {
            next();
        }
    });
}

app.post('/event', cache, getAndCacheEvents);

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
