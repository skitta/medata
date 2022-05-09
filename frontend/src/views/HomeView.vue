<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        @select="changeRouter"
      >
        <a-menu-item key="dashboard">
          <template #icon>
            <bar-chart-outlined />
          </template>
          总览
        </a-menu-item>
        <a-menu-item key="2">
          <template #icon>
            <plus-square-outlined />
          </template>
          添加
        </a-menu-item>
        <a-menu-item key="3">
          <template #icon>
            <user-outlined />
          </template>
          后台
        </a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <div class="layout-content">
        <router-view></router-view>
      </div>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      copyright@2022 by Chen Tao
    </a-layout-footer>
  </a-layout>
</template>

<script>
import { defineComponent, onMounted, reactive, toRefs } from "vue";
import { Layout, Menu } from "ant-design-vue";
import {
  BarChartOutlined,
  PlusSquareOutlined,
  UserOutlined,
} from "@ant-design/icons-vue";
import { onBeforeRouteUpdate, useRouter } from "vue-router";

const { Header, Content, Footer } = Layout;
const { Item } = Menu;

export default defineComponent({
  name: "HomeView",
  components: {
    ALayout: Layout,
    ALayoutHeader: Header,
    AMenu: Menu,
    AMenuItem: Item,
    ALayoutContent: Content,
    ALayoutFooter: Footer,
    BarChartOutlined,
    PlusSquareOutlined,
    UserOutlined,
  },
  setup() {
    const state = reactive({
      selectedKeys: ["dashboard"],
    });

    const router = useRouter();
    const changeRouter = ({ selectedKeys }) => {
      router.push({
        name: selectedKeys[0],
      });
    };

    onMounted(() => {
      changeRouter({ selectedKeys: state.selectedKeys });
    });

    onBeforeRouteUpdate(async (to) => {
      if(to.name === 'home') {
        return false;
      }
    })

    return {
      ...toRefs(state),
      changeRouter,
    };
  },
});
</script>

<style>
.layout-content {
  padding: 24px;
  margin-top: 20px;
  margin-bottom: 20px;
}
.logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}
.ant-row-rtl .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme="dark"] .site-layout-content {
  background: #141414;
}
</style>
