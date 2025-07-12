// 目前所有组件类型都直接使用 Ant Design Vue 的内置类型
// 如果未来需要自定义组件类型，可以在这里添加

import { DefaultOptionType } from "ant-design-vue/es/select";

// 定义组件 InlineFormFields 的类型
interface Field {
  type: 'date' | 'number' | 'string' | 'select' | 'percentage';
  label: string;
  options?: DefaultOptionType[];
};

export interface InlineFormField {
  [key: string]: Field;
}