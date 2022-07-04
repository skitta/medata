import axios from "axios";

if (process.env.NODE_ENV == 'development') {    
  axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
} else if (process.env.NODE_ENV == 'production') {    
  axios.defaults.baseURL = 'https://0.0.0.0:8000/api/'; // TODO: change to production url
}

axios.defaults.timeout = 10000;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';

export function getToken(username, password) {
  return new Promise((resolve, reject) => {
    axios.post("token-auth/", {
      username: username,
      password: password
    }).then(response => {
      resolve(response.data.token);
    }).catch(error => {
      reject(error); 
    });
  });
}