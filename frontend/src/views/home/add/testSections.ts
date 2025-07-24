import type { InlineFormField } from "@/types/components";

interface TestSection {
  key: string;
  header: string;
  name: string;
  fields: InlineFormField;
  span?: string;
}

export const testSections: TestSection[] = [
  {
    key: '1',
    header: '血常规',
    name: 'bloodTests',
    fields: {
      date: { type: 'date', label: '日期' },
      wbc: { type: 'number', label: 'WBC' },
      ne: { type: 'number', label: 'NE%' },
      ly: { type: 'number', label: 'LY%' },
      mo: { type: 'number', label: 'MO%' },
      rbc: { type: 'number', label: 'RBC' },
      plt: { type: 'number', label: 'PLT' }
    }
  },
  {
    key: '2',
    header: '肝功能',
    name: 'liverFunction',
    fields: {
      date: { type: 'date', label: '日期' },
      ast: { type: 'number', label: 'AST' },
      alt: { type: 'number', label: 'ALT' },
      tbil: { type: 'number', label: '总胆红素' },
      dbil: { type: 'number', label: '直接胆红素' },
      tb: { type: 'number', label: '总蛋白' },
      alb: { type: 'number', label: '白蛋白' },
    }
  },
  {
    key: '3',
    header: '心脏彩超',
    name: 'echocardiography',
    span: '4',
    fields: {
      date: { type: 'date', label: '日期' },
      lmca: { type: 'number', label: '左主干' },
      lmca_z: { type: 'number', label: '左主干Z值' },
      rca: { type: 'number', label: '右支' },
      rca_z: { type: 'number', label: '右支Z值' },
    }
  },
  {
    key: '4',
    header: '感染性指标',
    name: 'infectiousTests',
    span: '6',
    fields: {
      date: { type: 'date', label: '日期' },
      pct: { type: 'number', label: 'PCT' },
      crp: { type: 'number', label: 'CRP' },
    }
  },
  {
    key: '5',
    header: '其他辅助检查',
    name: 'customTests',
    span: '6',
    fields: {
      name: { type: 'string', label: '检验名称' },
      date: { type: 'date', label: '日期' },
      result: { type: 'number', label: '结果' },
      notes: { type: 'string', label: '备注' }
    }
  },
  {
    key: '6',
    header: '样本信息',
    name: 'samples',
    span: '4',
    fields: {
      date: { type: 'date', label: '日期' },
      label: { type: 'string', label: '标签' },
      sample_type: {
        type: 'select', label: '样本类型', options: [
          { label: '全血', value: '0' },
          { label: '血清', value: '1' },
          { label: '血浆', value: '2' },
          { label: 'PBMCs', value: '3' },
          { label: '其他', value: '4' },
        ]
      },
      sample_status: {
        type: 'select', label: '样本状态', options: [
          { label: '待处理', value: '0' },
          { label: '已处理', value: '1' },
          { label: '已销毁', value: '2' },
        ]
      },
      note: { type: 'string', label: '备注' },
    }
  }
];
