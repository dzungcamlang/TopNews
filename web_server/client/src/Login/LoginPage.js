import Auth from '../Auth/Auth';
import LoginForm from './LoginForm';
import React from 'react';
import PropTypes from 'prop-types';

class LoginPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      errors:{},
      user:{
        email:'',
        password:''
      }
    };
  }

  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;

    console.log('email', email);
    console.log('password', password);
    // fake authentication
    Auth.authenticateUser('fake_token', email);
  }

  // change user email or password
  changeUser(event) {
    const field = event.target.name; // either email or password
    const user = this.state.user;
    user[field] = event.target.value;

    this.setState({user});
  }

  render() {
    return (
      <LoginForm
        onSubmit={(e) => this.processForm(e)}
        onChange={(e) => this.changeUser(e)}
        errors={this.state.errors}
      />
    );
  }
}

// use context wo work with top-level router
LoginPage.contextTypes = {
  router: PropTypes.object.isRequired
}

export default LoginPage;
