const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// define schema structure
const UserSchema = new mongoose.Schema({
  email: {
    type: String,
    index: {unique: true} // avoid duplicate email
  },
  password: String,
});

// define instance methods to schema
// compare password
UserSchema.methods.comparePassword = function(password, callback) {
  bcrypt.compare(password, this.password, callback);
};

// define document lifecycle hooks (middleware)
// pre-save hooker: psw = hash(psw + salt)
UserSchema.pre('save', function(next) {
  // this refers to the document
  const user = this;
  // only proceed when user password is modified
  if (!user.isModified('password')) return next();

  return bcrypt.genSalt((saltError, salt) => {
    if (saltError) { return next(saltError); }
    return bcrypt.hash(user.password, salt, (hashError, hash) => {
      if (hashError) { return next(hashError); }
      // replace plain password by hashed (pas + salt)
      user.password = hash;
      return next();
    });
  });

});

// create and export model based on schema
module.exports = mongoose.model('User', UserSchema);
