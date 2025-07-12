import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import Components from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';

// https://vitejs.dev/config/
export default defineConfig(({mode}) => ({
  plugins: [
    vue(),
    Components({
      resolvers: [
        AntDesignVueResolver({
          importStyle: true,
          resolveIcons: true
        })
      ]
    })
  ],
  //   resolve: {
  //     alias: {
  //       '@': path.resolve(__dirname, 'src')
  //     }
  //   },
  build: {
    assetsDir: 'static'
  },
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true
      }
    }
  },
  define: {
    __VUE_PROD_DEVTOOLS__: mode !== 'production'
  }
}))
