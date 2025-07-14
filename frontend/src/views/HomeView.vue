<template>
  <a-layout>
    <a-layout-header class="header">
      <a-row>
        <a-col :xs="0" :sm="2" :md="2" :lg="1" :xl="1">
          <div class="logo"></div>
        </a-col>
        <a-col :xs="2" :sm="8" :md="16" :lg="17" :xl="18">
          <a-dropdown>
            <a-button class="mobile-menu" type="primary">
              <template #icon>
                <MenuOutlined />
              </template>
            </a-button>
            <template #overlay>
              <a-menu v-model:selectedKeys="selectedKeys" theme="dark" @select="changeRouter">
                <a-menu-item key="dashboard">
                  总览
                </a-menu-item>
                <a-menu-item key="add-patient">
                  添加
                </a-menu-item>
                <a-menu-item key="manager">
                  管理
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
          <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="horizontal"
            :style="{ lineHeight: '64px' }" @select="changeRouter" class="desktop-menu">
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
        </a-col>
        <a-col :xs="22" :sm="14" :md="6" :lg="6" :xl="5" style="text-align: right">
          <div class="user-info">
            <span>您好，{{ fullName }}</span>
            <a-button type="link" size="small" @click="logout">
              退出
            </a-button>
          </div>
        </a-col>
      </a-row>
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
import { onMounted, ref, computed } from "vue";
import { Layout as ALayout, Menu as AMenu, LayoutHeader as ALayoutHeader, LayoutContent as ALayoutContent, LayoutFooter as ALayoutFooter, MenuItem as AMenuItem, Button as AButton, Row as ARow, Col as ACol, Dropdown as ADropdown } from "ant-design-vue";
import {
  BarChartOutlined,
  PlusSquareOutlined,
  UserOutlined,
  MenuOutlined,
} from "@ant-design/icons-vue";
import { onBeforeRouteUpdate, useRouter } from "vue-router";
import type { SelectInfo } from "ant-design-vue/es/menu/src/interface";
import { useAuthStore } from "@/stores/auth";

const selectedKeys = ref<string[]>(["dashboard"]);
const authStore = useAuthStore();
const fullName = computed(() => authStore.fullName);

const router = useRouter();
const changeRouter = (info: SelectInfo): void => {
  selectedKeys.value = info.selectedKeys as string[];
  router.push({
    name: info.selectedKeys[0] as string,
  });
};

const logout = () => {
  authStore.logout();
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

.user-info {
  float: right;
  color: #fff;
}

.user-info span {
  margin-right: 16px;
}

.header {
  padding: 0 40px;
}

.mobile-menu {
  display: none;
}

@media (max-width: 425px) {
  .desktop-menu {
    display: none;
  }

  .mobile-menu {
    display: block;
    float: left;
    margin-top: 16px;
  }

  .header {
  padding: 0 10px;
}
}

[data-theme="dark"] .site-layout-content {
  background: #141414;
}
</style>
