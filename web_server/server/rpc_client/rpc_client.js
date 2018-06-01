var jayson = require('jayson');

var client = jayson.client.http({
  port: 4040,
  hostname: 'localhost'
});

// method name should match that exposed by RPC server
function add(a, b, callback) {
  client.request('add', [a, b], (err, response) => {
    if (err) throw err;
    console.log('response of add: ', response.result);
    callback(response.result);
  });
}

// get news summaries for a user from RPC server
function getNewsSummariesForUser(user_id, page_num, callback) {
  client.request('getNewsSummariesForUser', [user_id, page_num],
    (err, response) => {
      if (err) throw err;
      console.log(`Get response of getNewsSummary for ${user_id}, page ${page_num}`);
      callback(response.result);
    });
}

// send user click log
function logNewsClickForUser(user_id, news_id) {
  client.request('logNewsClickForUser', [user_id, news_id],
    (err, response) => {
      if (err) throw err;
      console.log(response);
    })
}

module.exports = {
  add: add,
  getNewsSummariesForUser: getNewsSummariesForUser,
  logNewsClickForUser: logNewsClickForUser
};
