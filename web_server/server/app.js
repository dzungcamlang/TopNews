
var express = require('express');
var path = require('path');
var config = require('./config/config.json');

var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

// connect to MongoDB and load User model
require('./models/main.js').connect(config.mongoDbUri);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static',
        express.static(path.join(__dirname, '../client/build/static')));

app.use('/', index);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});


module.exports = app;
