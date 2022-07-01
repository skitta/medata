import axios from "axios";
import store from "@/store";

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/kawasaki/';
axios.interceptors.request.use(
  config => {
    const token = store.getters.getToken;
    if (token) {
      config.headers.Authorization = `Token ${store.getters.getToken}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

function getGroups() {
  return new Promise((resolve, reject) => {
    let groupList = store.getters.getGroups;
    if (groupList.length !== 0) {
      resolve(groupList);
    } else {
      axios.get("enrollGroups/").then(response => {
        groupList = response.data.results.map(group => ({
          value: group.id,
          label: group.name,
        }));
        store.dispatch("setGroups", groupList);
        resolve(groupList);
      }).catch(error => {
        reject(error.data);
      });
    }
  });

}

function addPatient(data) {
  return new Promise((resolve, reject) => {
    axios.post("patients/", data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function getPatients(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "patients/",
      {
        params: params
      }
    ).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function updatePatient(id, data) {
  return new Promise((resolve, reject) => {
    axios.patch(`patients/${id}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function addTestByName(name, data) {
  return new Promise((resolve, reject) => {
    axios.post(`${name}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function getTestsByPatientId(id) {
  return new Promise((resolve, reject) => {
    axios.get(`all-tests-by-patient/${id}/`).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function updateTestByName(name, id, data) {
  return new Promise((resolve, reject) => {
    axios.put(`${name}/${id}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function getSummary() {
  return new Promise((resolve, reject) => {
    axios.get("summary/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function getCountByMonth() {
  return new Promise((resolve, reject) => {
    axios.get("count-by-month/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

function getAgeByGroup() {
  return new Promise((resolve, reject) => {
    axios.get("age-by-group/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error.data);
    });
  });
}

export {
  getGroups,
  addPatient,
  getPatients,
  updatePatient,
  addTestByName,
  getTestsByPatientId,
  updateTestByName,
  getSummary,
  getCountByMonth,
  getAgeByGroup,
}