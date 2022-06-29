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
import { defineComponent } from "vue";
import { Row, Col } from "ant-design-vue";

export default defineComponent({
  components: {
    ARow: Row,
    ACol: Col,
  },
});
</script>

<style scoped>
.add {
  margin: 20px 40px;
  padding: 24px;
}
</style>