// exports utility function for authentication

class Auth {
  /**
  * Authenticate a user and save a token in local storage
  * @param {string} token
  * @param {string} email
  */
  static authenticateUser(token, email) {
    localStorage.setItem('token', token);
    localStorage.setItem('email', email);
  }

  /**
  * Authenticate user, this does not replace server side authentication
  * @returns {boolean}
  */
  static isUserAuthenticated() {
    return localStorage.getItem('token') !== null;
  }

  /**
  * Deauthenticate user and remove token from local storage
  * @returns {boolean}
  */
  static deauthenticateUser() {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
  }

  static getToken() {
    return localStorage.getItem('token');
  }

  static getEmail() {
    return localStorage.getItem('email');
  }

}

export default Auth;
