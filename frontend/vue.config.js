const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  // support for django static dir
  assetsDir: 'static'
})
