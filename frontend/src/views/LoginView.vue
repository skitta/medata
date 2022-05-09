<template>
  <div class="login">
    <particles-bg type="cobweb" :bg="true" />
    <a-card hoverable class="login-card">
      <template #cover>
        <div class="login-cover">
          <img src="~@/assets/doctor.svg" alt="cover" />
        </div>
      </template>
      <div>
        <a-form :model="formState" @submit="handleSubmit">
          <a-form-item>
            <a-select v-model:value="formState.role" :options="roleOptions" placeholder="Select a role">
            </a-select>
          </a-form-item>
          <a-form-item>
            <a-input v-model:value="formState.user" placeholder="Username" @change="handleInputChange">
              <template #prefix>
                <UserOutlined style="color: rgba(0, 0, 0, 0.25)" />
              </template>
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-input-password v-model:value="formState.password" placeholder="Password" @change="handleInputChange">
              <template #prefix>
                <LockOutlined style="color: rgba(0, 0, 0, 0.25)" />
              </template>
            </a-input-password>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" html-type="submit" :disabled="formState.user === '' || formState.password === ''">
              Log in
            </a-button>
          </a-form-item>
        </a-form>
        <div v-if="formState.msg.length != 0">
          <a-alert :message="formState.msg" type="error" show-icon></a-alert>
        </div>
      </div>
    </a-card>
  </div>
</template>

<script>
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import { defineComponent, reactive, getCurrentInstance } from "vue";
import { Form, Input, Button, Card, Select, Alert } from "ant-design-vue";
import { ParticlesBg } from "particles-bg-vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const { Item } = Form;
const { Password } = Input;

export default defineComponent({
  setup() {
    const currentInstance = getCurrentInstance();
    const { $http } = currentInstance.appContext.config.globalProperties;
    
    const store = useStore();
    store.dispatch('setToken', null);

    const router = useRouter();

    const formState = reactive({
      user: "",
      password: "",
      role: "doctor",
      msg: "",
    });

    const roleOptions = [
      {
        value: "doctor",
        label: "Doctor",
      },
      {
        value: "patient",
        label: "Patient",
      },
    ];

    const handleSubmit = () => {
      const { user, password } = formState;
      var formData = require("form-data");
      var data = new formData();
      data.append("username", user);
      data.append("password", password);

      var config = {
        method: 'post',
        url: '/token-auth/',
        headers: {
          ...data.getHeaders,
        },
        data: data,
      };

      $http(config)
        .then(res => {
          store.commit("setToken", res.data.token);
        })
        .then(() => {
          router.push({ name: "home" });
        })
        .catch(err => {
          console.log(err);
          formState.msg = "Username or password is incorrect";
        });
    };

    const handleInputChange = () => {
      formState.msg = ""
    }

    return {
      formState,
      roleOptions,
      handleSubmit,
      handleInputChange,
    };
  },

  components: {
    UserOutlined,
    LockOutlined,
    AForm: Form,
    AFormItem: Item,
    AInput: Input,
    AButton: Button,
    ACard: Card,
    AInputPassword: Password,
    ASelect: Select,
    ParticlesBg,
    AAlert: Alert,
  },
});

</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: rgba(102, 142, 174, 0.25);
}

.login-cover {
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: center;
  height: 200px;
  padding: 20px;
  background-image: url("~@/assets/login.bg.svg");
  background-size: auto;
  background-position: bottom;
}

.login-cover img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.login-card {
  width: 400px;
  margin: auto;
}

.ant-card-hoverable {
  cursor: default;
}

</style>
