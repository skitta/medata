import axios from "axios";

axios.defaults.baseURL = 'http://127.0.0.1:8000/api';

export function getToken(username, password) {
  return new Promise((resolve, reject) => {
    axios.post("/token-auth/", {
      username: username,
      password: password
    }).then(response => {
      resolve(response.data.token);
    }).catch(error => {
      reject(error.data);
    });
  });
}