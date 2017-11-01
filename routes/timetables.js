var express = require('express');
var router = express.Router();

/* GET Services listing. */
router.get('/', function (req, res, next) {
	res.send('Services');
});

module.exports = router;
