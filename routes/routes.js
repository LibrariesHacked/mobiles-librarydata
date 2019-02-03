var express = require('express');
var router = express.Router();

router.get('/api/routes', function (req, res, next) {
	res.send('Routes');
});

module.exports = router;