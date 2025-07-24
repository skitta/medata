<template>
  <a-config-provider :locale="zhCN">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </a-config-provider>
</template>

<script setup lang="ts">
import { useMainStore } from "./stores";
import { ConfigProvider as AConfigProvider } from "ant-design-vue";
import zhCN from 'ant-design-vue/es/locale/zh_CN';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';

dayjs.locale('zh-cn');

const store = useMainStore();

const storedState = sessionStorage.getItem("store");
if (storedState) {
  store.$patch(JSON.parse(storedState));
}

store.$subscribe((_mutation, state) => {
  sessionStorage.setItem("store", JSON.stringify(state));
});
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0px;
  height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
