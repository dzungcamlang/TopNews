const express = require('express');
const passport = require('passort');
const router = express.Router();
// validate login/signup form
const validator = require('validator');

// signup route handler,
// first validate form,
// then call passport.authenticate w. custom callback
router.post('/signup', (req, res, next) => {
  const validationResult = validateSignupForm(req.body);
  if (!validationResult.success) {
    console.log('[Form Error] failed to validate signup form');
    return res.status(400).json({
      success: false,
      message: validationResult.message,
      errors: validationResult.errors
    });
  }
  // use passport-local strategy to authenticate signup
  // passport.authenticate() with custom callback
  return passport.authenticate('local-signup', (err) => {
    if (err) {
      console.log('[Failed Signup Auth] error: ${err}');
      // Duplicate email error, return meaningful message
      if (err.name === 'MongoError' && err.code === 11000) {
        // HTTP status 409: conflict error
        return res.status(409).json({
          success: false,
          message: 'Check form error message',
          errors: {
            email: 'This email is already taken'
          }
        });
      }
      // Other general errors
      return res.status(400).json({
        success: false,
        message: 'Could not process signup form' + + err.message
      });
    }

    // authentication passed
    return res.status(200).json({
      success: true,
      message: 'User signed up successfully. You should be able to log in now'
    });
  })(req, res, next);

});

// login route handler,
// first validate form
// then call passport.authticate w. custom callback
router.post('/login', (req, res, next) => {
  const validationResult = validateLoginForm(req.body);
  if (!validationResult.success) {
    console.log('[Form Error] failed to validate login form');
    return res.status(400).json({
      success: false,
      message: validationResult.message,
      errors: validationResult.errors
    });
  }

  return passport.authenticate('local-login', (err, token, userData) => {
    if (err) {
      // wrong email/password
      if (err.name === 'IncorrectCredentialsError') {
        return res.status(400).json({
          success: false,
          message: err.message
        });
      }
      // other general errors
      return res.status(400).json({
        success: false,
        message: 'Could not process form' + err.message
      });
    }

    // user authenticated
    return res.json({
      success: true,
      message: 'You have successfully logged in',
      token,
      user: userData
    });
  })(req, res, next);
})

// auxiliary functions to validate forms
function validateSignupForm(payload) {
  console.log('[Signup Form]: ' + payload);
  const errors = {};
  let isFormValid = true;
  let message = '';

  if (!payload || typeof payload.email !== 'string' || !validator.isEmail(payload.email)) {
    isFormValid = false;
    errors.email = 'Please provide a correct email address';
  }

  if (!payload || typeof payload.password !== 'string' || payload.password.length < 8) {
    isFormValid = false;
    errors.password = 'Password must have at least 8 characters';
  }

  if (!isFormValid) {
    message = 'Check the form for errors';
  }

  return {
    success: isFormValid,
    message,
    errors
  };
}

function validateLoginForm(payload) {
  console.log(payload);
  const errors = {};
  let isFormValid = true;
  let message = '';

  if (!payload || typeof payload.email !== 'string' || payload.email.trim().length === 0) {
    isFormValid = false;
    errors.email = 'Please provide your email address';
  }

  if (!payload || typeof payload.password !== 'string' || payload.password.length === 0) {
    isFormValid = false;
    errors.password = 'Please provide your password';
  }

  if (!isFormValid) {
    message = 'Check the form for errors';
  }

  return {
    success: isFormValid,
    message,
    errors
  };
}


module.exports = router;
