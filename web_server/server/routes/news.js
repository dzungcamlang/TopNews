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

// post user news click log
router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
  var user_id = req.params['userId'];
  var news_id = req.params['newsId'];
  console.log('Logging user news click...');
  rpc_client.logNewsClickForUser(user_id, news_id);
  // non-response request
  res.status(200);
})


module.exports = router;
