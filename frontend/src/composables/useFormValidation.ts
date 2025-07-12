import type { Rule } from 'ant-design-vue/es/form';

export function useFormValidation() {
  
  const createRequiredRule = (message: string): Rule => ({
    required: true,
    message,
    trigger: 'blur'
  });

  const createNumberRule = (fieldName: string, min = 0): Rule => ({
    required: true,
    validator: async (_rule: Rule, value: number | undefined) => {
      if (value === undefined || value === null) {
        return Promise.reject(`请输入${fieldName}`);
      }
      if (!Number.isInteger(value)) {
        return Promise.reject(`${fieldName}必须为整数`);
      }
      if (value < min) {
        return Promise.reject(`${fieldName}不能小于${min}`);
      }
      return Promise.resolve();
    },
    trigger: 'blur'
  });

  const createPositiveNumberRule = (fieldName: string): Rule => ({
    required: true,
    validator: async (_rule: Rule, value: number | undefined) => {
      if (value === undefined || value === null) {
        return Promise.reject(`请输入${fieldName}`);
      }
      if (value < 0) {
        return Promise.reject(`${fieldName}不能小于0`);
      }
      return Promise.resolve();
    },
    trigger: 'blur'
  });

  const createAsyncValidationRule = (
    validatorFn: (value: any) => Promise<boolean>,
    errorMessage: string
  ): Rule => ({
    required: true,
    validator: async (_rule: Rule, value: any) => {
      if (!value) {
        return Promise.reject(errorMessage);
      }
      const isValid = await validatorFn(value);
      if (!isValid) {
        return Promise.reject(errorMessage);
      }
      return Promise.resolve();
    },
    trigger: 'blur'
  });

  return {
    createRequiredRule,
    createNumberRule,
    createPositiveNumberRule,
    createAsyncValidationRule
  };
}