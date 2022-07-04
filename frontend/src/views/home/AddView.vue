<template>
  <div class="add">
    <a-row>
      <a-col :span="12" :offset="6">
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
import { defineComponent, onMounted } from "vue";
import { Row, Col } from "ant-design-vue";
import { onBeforeRouteUpdate, useRouter } from "vue-router";

export default defineComponent({
  name: "AddView",
  components: {
    ARow: Row,
    ACol: Col,
  },

  setup() {
    const router = useRouter();

    onBeforeRouteUpdate(async (to) => {
      if (to.name === 'add') {
        return false;
      }
    });

    onMounted(async () => {
      router.push({
        name: 'add-patient',
      });
    });
    return {};
  },
});
</script>

<style scoped>
.add {
  margin: 20px 40px;
  padding: 24px;
}
</style>