import axios from "axios";
import Cookies from "js-cookie";

// 使用环境变量配置 API 基础 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
axios.defaults.baseURL = `${API_BASE_URL}/api/`;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
axios.defaults.headers.post['X-CSRFToken'] = Cookies.get('csrftoken') || '';

export function getToken(username: string, password: string): Promise<string> {
  return new Promise((resolve, reject) => {
    axios.post<{ token: string }>("token-auth/", {
      username: username,
      password: password
    }).then(response => {
      resolve(response.data.token);
    }).catch(error => {
      reject(error);
    });
  });
}