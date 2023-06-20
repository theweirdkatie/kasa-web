import express from 'express';
import * as Db from '$lib/server/db';

const app = express();
app.use(express.json());

app.get('/db/devices', async (req, res) => {
    try {
        const devices = await Db.getInitialDevices();
        res.json(devices);
    } catch (error) {
        console.error('Error fetching devices:', error);
        res.status(500).json({ error: 'Failed to fetch devices' });
    }
});

app.post('/db/devices', async (req,res) => {
    const devices = req.body();

    try {
        await Db.insertNewDevices(devices);
        res.json({ message: 'Devices inserted successfully' });
    } catch (error) {
        console.error('Error inserting devices:', error);
        res.status(500).json({ error: 'Failed to insert devices' });
    }
});