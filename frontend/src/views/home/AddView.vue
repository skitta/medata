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

<script setup lang="ts">
import { Row as ARow, Col as ACol } from "ant-design-vue";
import { onBeforeRouteUpdate, useRouter } from "vue-router";
import { computed } from "vue";

const router = useRouter();
const colSpan = computed((): number => {
  return (router.currentRoute.value.meta?.colSpan as number) || 12;
});

onBeforeRouteUpdate((to) => {
  if (to.name === 'add') {
    return false;
  } else {
    return true;
  }
});
</script>
