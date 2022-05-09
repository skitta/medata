<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  setup() {
    const store = useStore();

    if (sessionStorage.getItem("store")) {
      store.replaceState(Object.assign({}, store.state, JSON.parse(sessionStorage.getItem("store"))));
    }

    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem("store", JSON.stringify(store.state));
    });

    return {};
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
</style>
