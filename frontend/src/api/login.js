import axios from "axios";
import Cookies from "js-cookie";

axios.defaults.baseURL = 'https://192.168.1.10/api/';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
axios.defaults.headers.post['X-CSRFToken'] = Cookies.get('csrftoken') || '';

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
