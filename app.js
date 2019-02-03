const express = require('express');
const path = require('path');

const services = require('./routes/services')
const mobiles = require('./routes/mobiles')
const routes = require('./routes/routes')
const stops = require('./routes/stops')

var app = express();

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

app.use('/api/services', services);
app.use('/api/mobiles', mobiles)
app.use('/api/routes', routes)
app.use('/api/stops', stops)


app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname + '/client/build/index.html'));
});

module.exports = app;