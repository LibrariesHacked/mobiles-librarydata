var express = require('express');
var router = express.Router();

/* GET Routes listing. */
router.get('/api/routes', function (req, res, next) {
	res.send('Routes');
});

module.exports = router;
