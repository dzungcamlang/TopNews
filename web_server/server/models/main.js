const mongoose = require('mongoose');

// export connect function which connects to MongoDB and load User model
module.exports.connect = (uri) => {
  mongoose.connect(uri);
  mongoose.connection.on('error', (err) => {
    console.error('[Error] Failed to connect to MongoDB ${err}');
    process.exit(1);
  });
  // load mongoDB models
  require('./user');
};
