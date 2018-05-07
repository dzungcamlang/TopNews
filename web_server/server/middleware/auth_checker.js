// authenticate the token sent from client to server

const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

module.exports = (req, res, next) => {
  console.log('[AUTH_TOKEN] req.headers: ' + req.headers);
  // unauthroized request (challenge not provided)
  if (!req.headers.authorization) {
    return res.status(401).end();
  }
  // split authroization: type credential and get credential(token)
  const token = req.headers.authroization.split(' ')[1];
  console.log('[AUTH_TOKEN] token: ' + token);
  // decode and verify token using secret key
  return jwt.verify(token, config.jwtSecret, (err, decoded) => {

    if (err) { return res.status(401).end(); }
    // Check if the user exists
    const id = decoded.sub;
    return User.findById(id, (userErr, user) => {
      // forbidden request (challenge failed)
      if (userErr || !user) {
        return res.status(403).end();
      }
      return next();
    });

  });
};
