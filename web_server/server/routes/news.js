var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();


// get paginated news summaries for user
router.get('/userid/:userId/pageNum/:pageNum', function(req, res, next) {
  var user_id = req.params['userId'];
  var page_num = req.params['pageNum'];
  console.log(`Fetch news for ${user_id}, page ${page_num}`);
  rpc_client.getNewsSummariesForUser(user_id, page_num, (response) => {
    res.json(response);
  });

});

module.exports = router;
