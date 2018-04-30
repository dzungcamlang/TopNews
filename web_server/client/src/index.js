import React from 'react';
import ReactDOM from 'react-dom';

import App from './App/App';
import SignUp from './SignUp/SignUpPage';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<SignUp />, document.getElementById('root'));
registerServiceWorker();
