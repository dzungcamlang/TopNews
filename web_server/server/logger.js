var winston = require('winston');

var logger = new(winston.Logger)({
  transports: [
    new (winston.transports.Console)({
      json: false,
      level: 'debug'
    }),
    new (winston.transports.File)({
      name: 'file_error',
      json: false,
      filename: __dirname + '/error.log',
      level: 'error'
    }),
    new (winston.transports.File)({
      name: 'file_error_and_info',
      json: false,
      filename: __dirname + '/combined.log',
      level: 'info'
    })
  ],
  exceptionHandlers: [
    new (winston.transports.Console)({
      json: false,
      timestamp: true
    }),
    new (winston.transports.File)({
      json: false,
      filename: __dirname + '/exception.log'
    })
  ],
  exitOnError: false
});

module.exports = logger;
