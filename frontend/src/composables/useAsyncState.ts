import { ref, computed } from 'vue';
import { useErrorHandler, type ApiError } from './useErrorHandler';

export function useAsyncState<T>(asyncFn: (...args: any[]) => Promise<T>, immediate = true) {
  const loading = ref(false);
  const data = ref<T | null>(null);
  const { errorMessage, handleError, clearError } = useErrorHandler();

  const execute = async (...args: any[]) => {
    loading.value = true;
    clearError();
    
    try {
      const result = await asyncFn(...args);
      data.value = result;
      return result;
    } catch (error) {
      handleError(error as ApiError);
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const reset = () => {
    data.value = null;
    loading.value = false;
    clearError();
  };

  const isReady = computed(() => !loading.value && data.value !== null);

  if (immediate) {
    execute();
  }

  return {
    loading,
    data,
    errorMessage,
    execute,
    reset,
    isReady,
    clearError,
    handleError
  };
}
