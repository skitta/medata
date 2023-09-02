<template>
  <a-layout>
    <a-layout-header>
      <div class="logo" />
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

<script>
import { defineComponent, onMounted, reactive, toRefs } from "vue";
import { Layout, Menu, Button } from "ant-design-vue";
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
    AButton: Button,
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

    // const logout = () => {
    //   router.push({
    //     name: "login",
    //   });
    // }

    onMounted(() => {
      changeRouter({ selectedKeys: state.selectedKeys });
    });

    onBeforeRouteUpdate(async (to) => {
      if (to.name === 'home') {
        return false;
      }
    })

    return {
      ...toRefs(state),
      changeRouter,
      // logout,
    };
  },
});
</script>

<style scoped>
.ant-layout-content {
  /* ant-layout-header: 64px, ant-layout-footer: 70px */
  min-height: calc(100vh - 134px)
}

.logo {
  float: left;
  width: 44px;
  height: 44px;
  margin: 10px 24px 10px 0;
  /* background: rgba(255, 255, 255, 0.3); */
  background-image: url("~@/assets/logo.svg");
  background-size: auto;
  background-repeat: no-repeat;
  background-position: center;
}

.logout {
  position: absolute;
  top: 0;
  right: 50px;
}

/* .ant-row-rtl .logo {
  float: right;
  margin: 16px 0 16px 24px;
} */

[data-theme="dark"] .site-layout-content {
  background: #141414;
}
</style>
