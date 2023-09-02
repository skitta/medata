<template>
  <a-config-provider :locale="zhCN">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </a-config-provider>
</template>

<script>
import { defineComponent } from "vue";
import { useStore } from "vuex";
import { ConfigProvider } from "ant-design-vue";
import zhCN from 'ant-design-vue/es/locale/zh_CN';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';

dayjs.locale('zh-cn');

export default defineComponent({
  components: {
    AConfigProvider: ConfigProvider,
  },
  setup() {
    const store = useStore();

    if (sessionStorage.getItem("store")) {
      store.replaceState(Object.assign({}, store.state, JSON.parse(sessionStorage.getItem("store"))));
    }

    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem("store", JSON.stringify(store.state));
    });

    return {
      zhCN,
      dayjs,
    };
  },
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
