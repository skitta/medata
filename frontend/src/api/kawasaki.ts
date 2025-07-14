import { kawasakiApi } from '@/plugins/axios'
import type { AxiosResponse } from 'axios'
import type {
  ApiResponse,
  Patient,
  EnrollGroup,
  Summary,
  MonthlyCount,
  AgeDataByGroup,
  ExportParams,
  SelectOption
} from "@/types/api";


function download(response: AxiosResponse<Blob>): void {
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
    // @ts-ignore - legacy IE support
    navigator.msSaveBlob(blob, fileName);
  }
}

export function getGroups(): Promise<SelectOption[]> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get<ApiResponse<EnrollGroup>>("enrollGroups/").then(response => {
      const groupList: SelectOption[] = response.data.results.map(group => ({
        value: group.id,
        label: group.name,
      }));
      resolve(groupList);
    }).catch(error => {
      reject(error);
    });
  });
}

export function addPatient(data: Partial<Patient>): Promise<Patient> {
  return new Promise((resolve, reject) => {
    kawasakiApi.post<Patient>("patients/", data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function getPatients(params?: ExportParams): Promise<ApiResponse<Patient>> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get<ApiResponse<Patient>>(
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

export function updatePatient(id: number, data: Partial<Patient>): Promise<Patient> {
  return new Promise((resolve, reject) => {
    kawasakiApi.patch<Patient>(`patients/${id}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function exportPatients(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
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

export function addTestByName(name: string, data: any): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.post(`${name}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function getTestsByPatientId(id: number): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(`all-tests-by-patient/${id}/`).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function updateTestByName(name: string, id: number, data: any): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.put(`${name}/${id}/`, data).then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function exportBloodTests(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
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

export function exportLiverFunctions(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
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

export function exportEchocardiography(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
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

export function exportInfectiousTests(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
      "infectiousTests/export/",
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

export function exportSamples(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
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

export function getSummary(): Promise<Summary> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get<Summary>("summary/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function getCountByMonth(): Promise<MonthlyCount[]> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get<MonthlyCount[]>("count-by-month/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function getAgeByGroup(): Promise<AgeDataByGroup> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get<AgeDataByGroup>("age-by-group/").then(response => {
      resolve(response.data);
    }).catch(error => {
      reject(error);
    });
  });
}

export function getExportFile(): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get("export/all/", { responseType: 'blob' }).then(response => {
      download(response);
      resolve(response.headers);
    }).catch(error => {
      reject(error);
    });
  });
}

export function exportCustomTests(params?: ExportParams): Promise<any> {
  return new Promise((resolve, reject) => {
    kawasakiApi.get(
      "customTests/export/",
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
