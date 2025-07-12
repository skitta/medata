<template>
  <a-layout>
    <a-layout-header>
      <div class="logo"></div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="horizontal" :style="{ lineHeight: '64px' }"
        @select="changeRouter">
        <a-menu-item key="dashboard">
          <template #icon>
            <bar-chart-outlined />
          </template>
          总览
        </a-menu-item>
        <a-menu-item key="add-patient">
          <template #icon>
            <plus-square-outlined />
          </template>
          添加
        </a-menu-item>
        <a-menu-item key="manager">
          <template #icon>
            <user-outlined />
          </template>
          管理
        </a-menu-item>
      </a-menu>
      <!-- <div class="logout">
        <a-button type="link" size="small" @click="logout">
          退出
        </a-button>
      </div> -->
    </a-layout-header>
    <a-layout-content>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      copyright@2022 by Chen Tao
    </a-layout-footer>
  </a-layout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { Layout as ALayout, Menu as AMenu, LayoutHeader as ALayoutHeader, LayoutContent as ALayoutContent, LayoutFooter as ALayoutFooter, MenuItem as AMenuItem } from "ant-design-vue";
import {
  BarChartOutlined,
  PlusSquareOutlined,
  UserOutlined,
} from "@ant-design/icons-vue";
import { onBeforeRouteUpdate, useRouter } from "vue-router";
import type { SelectInfo } from "ant-design-vue/es/menu/src/interface";

const selectedKeys = ref<string[]>(["dashboard"]);

const router = useRouter();
const changeRouter = (info: SelectInfo): void => {
  selectedKeys.value = info.selectedKeys as string[];
  router.push({
    name: info.selectedKeys[0] as string,
  });
};

onMounted(() => {
  changeRouter({ selectedKeys: selectedKeys.value } as SelectInfo);
});

onBeforeRouteUpdate((to) => {
  if (to.name === 'home') {
    return false;
  }
  return true;
});
</script>

<style scoped>
.ant-layout-content {
  min-height: calc(100vh - 134px)
}

.logo {
  float: left;
  width: 44px;
  height: 44px;
  margin: 10px 24px 10px 0;
  background-image: url("@/assets/logo.svg");
  background-size: auto;
  background-repeat: no-repeat;
  background-position: center;
}

.logout {
  position: absolute;
  top: 0;
  right: 50px;
}

[data-theme="dark"] .site-layout-content {
  background: #141414;
}
</style>
