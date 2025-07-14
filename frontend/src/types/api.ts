// 定义 API 响应类型
export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// 定义患者类型
export interface Patient {
  id?: number;
  registered_ID: string;
  document_ID: string;
  full_name: string;
  gender: 'M' | 'F' | '';
  age: number;
  in_date: string;
  weight: number;
  height: number;
  resistance: boolean;
  relapse: boolean;
  group?: number;
  version?: number;
}

// 定义分组类型
export interface EnrollGroup {
  id: number;
  name: string;
}

// 定义血液检查类型
export interface BloodTest {
  id?: number;
  patient: number;
  date: string;
  wbc: number;
  ne: number;
  ly: number;
  mo: number;
  rbc: number;
  plt: number;
  version?: number;
}

// 定义肝功能检查类型
export interface LiverFunction {
  id?: number;
  patient: number;
  date: string;
  alt: number;
  ast: number;
  tb: number;
  db: number;
  alb: number;
  pa: number;
  version?: number;
}

// 定义心脏超声检查类型
export interface Echocardiography {
  id?: number;
  patient: number;
  date: string;
  lmca: number;
  lmca_z: number;
  rca: number;
  rca_z: number;
  version?: number;
}

// 定义感染性疾病检查类型
export interface InfectiousTest {
  id?: number;
  patient: number;
  date: string;
  crp: number;
  pct: number;
  version?: number;
}

// 定义样本类型
export interface Sample {
  id?: number;
  patient: number;
  date: string;
  sample_type: '0' | '1' | '2' | '3' | '4';
  sample_status: '0' | '1' | '2';
  note: string;
  version?: number;
}

// 定义自定义检查类型
export interface CustomTest {
  id?: number;
  patient: number;
  name: string;
  date: string;
  result?: string;
  note?: string;
  version?: number;
}

// 定义统计数据类型
export interface Summary {
  sample_counts?: Record<string, number>;
  groups?: string[];
  gender_counts?: Record<string, { M: number; F: number }>;
  age_mean?: Record<string, number>;
}

// 定义月度统计类型
export interface MonthlyCount {
  date: string;
  count: number;
}

// 定义年龄分组统计类型
export interface AgeGroupData {
  value: number;
}

// 定义年龄分组数据映射
export interface AgeDataByGroup {
  [groupName: string]: AgeGroupData[];
}

// 导出参数类型
export interface ExportParams {
  [key: string]: string | number | boolean | undefined;
}

// 选项类型
export interface SelectOption {
  value: number;
  label: string;
}

// Axios 响应头类型
export interface AxiosHeaders {
  [key: string]: string;
}

// 登录请求类型
export interface LoginRequest {
  username: string;
  password: string;
}
