import Auth from '../Auth/Auth';
import LoginForm from './LoginForm';
import React from 'react';
import PropTypes from 'prop-types';

class LoginPage extends React.Component {
  constructor(props, context) {
    super(props, context);
    console.log('[Location Props States]:');
    console.log(this.props.location.state);
    const location_state = this.props.location.state ? this.props.location.state : {};
    this.state = {
      errors:{},
      user:{
        email:'',
        password:''
      },
      location_state: location_state
    };
  }

  // send POST request to server and handle response
  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;

    console.log('email', email);
    console.log('password', password);

    // send post req to Node server
    const url = 'http://' + window.location.hostname + ':3000/auth/login';
    const request = new Request(
      url,
      {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email:this.state.user.email,
          password:this.state.user.password
        })
      }
    );

    // handle response
    fetch(request).then(
      response => {
        // User authenticated, store token and redirect to root component
        if (response.status === 200) {
          this.setState({
            errors: {}
          });
          response.json().then(json => {
            console.log('User login, response from server: ' + json);
            Auth.authenticateUser(json.token, email);
            this.context.router.replace('/');
          });
        } else {
          console.log('Login failed');
          response.json().then(json => {
            const errors = json.errors ? json.errors : {};
            // The error message displayed after user failed to log in
            errors.summary = json.message;
            this.setState({errors});
          });
        }
      }
    );
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
        state={this.state.location_state}
      />
    );
  }
}

// use context wo work with top-level router
LoginPage.contextTypes = {
  router: PropTypes.object.isRequired
}

export default LoginPage;
