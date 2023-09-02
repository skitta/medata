<template>
  <div class="nav-view-container">
    <a-row justify="space-around">
      <a-col :xs="24" :md="colSpan + 4" :xl="colSpan">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { Row, Col } from "ant-design-vue";
import { onBeforeRouteUpdate, useRouter } from "vue-router";
import { computed } from "@vue/reactivity";

export default defineComponent({
  name: "AddView",
  components: {
    ARow: Row,
    ACol: Col,
  },

  setup() {
    const router = useRouter();
    const colSpan = computed(() => {
      return router.currentRoute.value.meta.colSpan;
    });
    onBeforeRouteUpdate(async (to) => {
      if (to.name === 'add') {
        return false;
      }
    });

    return {
      colSpan,
    };
  },
});
</script>
