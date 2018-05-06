// Export a Passport-local Strategy:
// Authenticate a user by its username/password
// Server sends a json web token to the user upon authenticated

const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config/config.json');

module.exports = new PassportLocalStrategy({
  // speficy credential fields
  usernameField: 'email',
  passwordField: 'password',
  session: false,
  // enable verify callback with request object
  passReqToCallback: true
}, (req, email, password, done) => {
  const userData = {
    email: email.trim(),
    password: password
  };

  return User.findOne({ email: userData.email }, (err, user) => {
    // handle error or user not found
    if (err) { return done(err); }
    if (!user) {
      const error = new Error('Incorrect email or password');
      error.name = 'IncorrectCredentialsError';
      return done(error);
    }

    // user found, verify if password matches
    return user.comparePassword(userData.password, (passwordErr, isMatch) => {
      // handle error or psw not matching
      if (err) { return done(err); }
      if (!isMatch) {
        const error = new Error('Incorrect email or password');
        error.name = 'IncorrectCredentialsError';
        return done(error);
      }
      // password matches, user authenticated and server sends a token to user
      // user MongoDB internal id to generate unique token for each user
      const payload = {
        sub: user._id
      };
      const token = jwt.sign(payload, config.jwtSecret);
      const data = {
        name: user.email
      };

      return done(null, token, data);
    });

  });
});
