var client = require('./rpc_client');

client.add(1, 2, (res) => {
  console.assert(res === 3);
})

// invoke "getNewsSummariesForUser"
client.getNewsSummariesForUser('test_user', 2, function(response) {
  console.assert(response != null);
});
