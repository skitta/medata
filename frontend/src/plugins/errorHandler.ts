import { App } from 'vue';

export function setupErrorHandler(app: App) {
  app.config.errorHandler = (err, instance, info) => {
    console.error('Global error:', err);
    console.error('Component instance:', instance);
    console.error('Error info:', info);
    
    // 可以在这里添加错误上报逻辑
    // reportError(err, { component: instance, info });
  };

  // 处理未捕获的 Promise 错误
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    event.preventDefault();
  });
}