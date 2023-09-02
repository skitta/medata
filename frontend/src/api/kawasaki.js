import axios from "axios";
import store from "@/store";
import Cookies from "js-cookie";

axios.defaults.baseURL = 'https://192.168.1.10/api/kawasaki/';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
axios.defaults.headers.post['X-CSRFToken'] = Cookies.get('csrftoken') || '';

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

function download(response) {
  const blob = new Blob([response.data], { type: "text/csv" });
  const fileName = "kawasaki_export.zip";
  if ("download" in document.createElement("a")) {
    const a = document.createElement("a");
    a.download = fileName;
    a.href = window.URL.createObjectURL(blob);
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(a.href);
    document.body.removeChild(a);
  } else {
    navigator.msSaveBlob(blob, fileName);
  }
}

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
        reject(error);
      });
    }
  });

}

function addPatient(data) {
  return new Promise((resolve, reject) => {
    axios.post("patients/", data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
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
      reject(error);
    });
  });
}

function updatePatient(id, data) {
  return new Promise((resolve, reject) => {
    axios.patch(`patients/${id}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function exportPatients(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "patients/export/",
      {
        params: params
      }
    ).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

function addTestByName(name, data) {
  return new Promise((resolve, reject) => {
    axios.post(`${name}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function getTestsByPatientId(id) {
  return new Promise((resolve, reject) => {
    axios.get(`all-tests-by-patient/${id}/`).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function updateTestByName(name, id, data) {
  return new Promise((resolve, reject) => {
    axios.put(`${name}/${id}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function exportBloodTests(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "bloodTests/export/",
      {
        params: params
      }
    ).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

function exportLiverFunctions(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "liverFunction/export/",
      {
        params: params
      }
    ).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

function exportEchocardiography(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "echocardiography/export/",
      {
        params: params
      }
    ).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

function exportOtherTests(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "otherTests/export/",
      {
        params: params
      }
    ).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

function exportSamples(params) {
  return new Promise((resolve, reject) => {
    axios.get(
      "samples/export/",
      {
        params: params
      }
    ).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

function getSummary() {
  return new Promise((resolve, reject) => {
    axios.get("summary/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function getCountByMonth() {
  return new Promise((resolve, reject) => {
    axios.get("count-by-month/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function getAgeByGroup() {
  return new Promise((resolve, reject) => {
    axios.get("age-by-group/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

function getExportFile() {
  return new Promise((resolve, reject) => {
    axios.get("export/all/", {responseType: 'blob'}).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

export {
  getGroups,
  addPatient,
  getPatients,
  updatePatient,
  exportPatients,
  addTestByName,
  getTestsByPatientId,
  updateTestByName,
  exportBloodTests,
  exportLiverFunctions,
  exportEchocardiography,
  exportOtherTests,
  exportSamples,
  getSummary,
  getCountByMonth,
  getAgeByGroup,
  getExportFile
}
