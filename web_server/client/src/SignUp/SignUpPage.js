import SignUpForm from './SignUpForm';
import React from 'react';
import PropTypes from 'prop-types';

class SignUpPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state={
      errors: {},
      user: {
        email:'',
        password:'',
        confirm_password:''
      }
    };
  }

  // POST signup form and handle response accordingly
  processForm(event) {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;
    const confirm_password = this.state.user.confirm_password;

    console.log('email:', email);
    console.log('password', password);
    console.log('confirm_password', confirm_password);

    // post signup data.
    const url = 'http://' + window.location.hostname + ':3000' + '/auth/signup';
    const request = new Request(
      url,
      {method:'POST', headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: this.state.user.email,
        password: this.state.user.password
      })
    });

    // handle response
    fetch(request).then(response => {
      // user sign up successfully, redirect to login page
      if (response.status === 200) {
        this.setState(
          {errors: {}}
        );
        this.context.router.replace('/login');
      } else {
        response.json().then(json => {
          console.log('Signup failed, response from server: ' + json);
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          this.setState({errors});
        });
      }
    });
  }

  // update states.user upon input, also handle password matching
  changeUser(event) {
    const field = event.target.name;  // email || password || confirm_password
    const user = this.state.user;
    user[field] = event.target.value;

    this.setState({user});

    const errors = this.state.errors;
    if (this.state.user.password !== this.state.user.confirm_password) {
      errors.password = "Passwords don't match.";
    } else {
      errors.password = '';
    }
    this.setState({errors});
  }

  render() {
    return (
      <SignUpForm
      onSubmit={(e) => this.processForm(e)}
       onChange={(e) => this.changeUser(e)}
       errors={this.state.errors}
       />
    );
  }
}

SignUpPage.contextTypes = {
  router: PropTypes.object.isRequired
}

export default SignUpPage;
