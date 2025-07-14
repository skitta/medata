import type { Patient, SelectOption } from '@/types/api';

// Store 状态类型
export interface MainState {
  patient: Patient | null;
  groups: SelectOption[];
  tests: Record<string, any>;
  complete: Record<string, boolean>;
}

// Store 的 Actions 参数类型
export interface TestData {
  name: string;
  data: any;
}

export interface CompleteData {
  name: string;
  data: any;
}