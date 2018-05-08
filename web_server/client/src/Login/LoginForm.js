import './LoginForm.css';
import { Link } from 'react-router';
import React from 'react';

// LoginForm receives three props from parent components and return a login form
const LoginForm = ({
  onSubmit,
  onChange,
  errors,
  state
}) => (
  <div className='container'>
    <div className='card-panel login-panel'>
      <form className='col s12' action='/' onSubmit={onSubmit}>
        {/* Form title and error summary */}
        <h4 className='center-align'>Login</h4>
        {errors.summary && <div className='row'><p className='error-message'>
        {errors.summary}</p></div>}
        {/* Show additional info for redirected users */}
        {state && state.info && <div className='row'><p className='info'>
        {state.info}</p></div>}
        {/* Email and error message */}
        <div className='row'>
          <div className='input-field col s12'>
            <input className='validate' id='email' type='email' name='email'
            onChange={onChange} />
            <label htmlFor='email'>Email</label>
          </div>
        </div>
        {errors.email && <div className='row'><p className='error-message'>
        {errors.email}</p></div>}
        {/* Password and error message */}
        <div className='row'>
          <div className='input-field col s12'>
            <input className='validate' id='password' type='password' name='password'
            onChange={onChange} />
            <label htmlFor='password'>Password</label>
          </div>
        </div>
        {errors.password && <div className='row'><p className='error-message'>
        {errors.password}</p></div>}
        {/* Buttons */}
        <div className='row right-align'>
          <input type='submit' className='waves-effect waves-light btn indigo lighten-1'
          value='Log in' />
        </div>
        <div className='row'>
          <p className='right-align'>New to Top News? <Link to='/signup'>Sign Up</Link></p>
        </div>
      </form>
    </div>
  </div>
);

export default LoginForm;
