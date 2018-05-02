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

module.exports = {
  add: add
};
