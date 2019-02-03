var express = require('express');
var router = express.Router();

router.get('/api/', function (req, res, next) {
	res.render('index', { title: 'Mobile Libraries' });
});

module.exports = router;