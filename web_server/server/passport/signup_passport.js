// Export a passport-local strategy for user signup
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;

module.exports = new PassportLocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
  passReqToCallback: true
}, (req, email, password, done) => {
  const userData = {
    email: email.trim(),
    password: password
  };

  const newUser = new User(userData);
  // MongoDB will return error if duplicate email is detected
  newUser.save((err) => {
    if (err) {
      return done(err);
    }
    console.log(`New user created: ${newUser.email}`);
    return done(null);
  });
});
