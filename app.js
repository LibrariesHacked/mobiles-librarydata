// Require Express
const express = require('express');
const path = require('path');
const services = require('./routes/services')
const mobiles = require('./routes/mobiles')
const routes = require('./routes/routes')
const stops = require('./routes/stops')
const timetables = require('./routes/timetables')

//
var app = express();

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

// API

// Services
app.use('/api/services', services);

// Mobiles
app.use('/api/mobiles', mobiles)

// Routes
app.use('/api/routes', routes)

// Stops
app.use('/api/stops', stops)

// Timetables
app.use('/api/stops', timetables)

// Use React for other requests.
//app.get('*', (req, res) => {
//	res.sendFile(path.join(__dirname + '/client/build/index.html'));
//});

// 
module.exports = app;
