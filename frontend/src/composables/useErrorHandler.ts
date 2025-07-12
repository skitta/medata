import { ref } from 'vue';

export interface ApiError {
  response?: {
    status: number;
    data?: {
      detail?: string;
      [key: string]: any;
    };
  };
  message?: string;
}

export function useErrorHandler() {
  const errorMessage = ref('');

  const clearError = () => {
    errorMessage.value = '';
  };

  const handleError = (error: ApiError) => {
    console.error(error);
    
    if (error.response?.status === 409) {
      errorMessage.value = '数据冲突：其他用户可能已修改此数据，请刷新页面重试';
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail;
    } else if (error.response?.data) {
      // 处理字段验证错误
      const errors = error.response.data;
      const errorMessages: string[] = [];
      
      for (const field in errors) {
        if (Array.isArray(errors[field])) {
          errorMessages.push(`${field}: ${errors[field].join(', ')}`);
        } else {
          errorMessages.push(`${field}: ${errors[field]}`);
        }
      }
      errorMessage.value = errorMessages.join('; ');
    } else {
      errorMessage.value = error.message || '操作失败，请重试';
    }
  };

  const showError = (message: string) => {
    errorMessage.value = message;
  };

  return {
    errorMessage,
    clearError,
    handleError,
    showError
  };
}