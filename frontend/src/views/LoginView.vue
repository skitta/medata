<template>
  <div class="login">
    <particles-bg type="cobweb" :bg="true" />
    <a-card hoverable class="login-card">
      <template #cover>
        <div class="login-cover">
          <img src="~@/assets/doctor.svg" alt="cover" />
        </div>
      </template>
      <div class="login-card-container">
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
            <a-button type="primary" html-type="submit" :disabled="formState.user === '' || formState.password === ''" :loading="submitLoading">
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
import { defineComponent, reactive, ref } from "vue";
import { Form, Input, Button, Card, Select, Alert } from "ant-design-vue";
import { ParticlesBg } from "particles-bg-vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { getToken } from "@/api/login";

const { Item } = Form;
const { Password } = Input;

export default defineComponent({
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
  
  setup() {
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

    const submitLoading = ref(false);

    const handleSubmit = () => {
      submitLoading.value = true;
      const { user, password } = formState;

      getToken(user, password)
        .then(token => {
          store.commit("setToken", token);
          submitLoading.value = false;
        })
        .then(() => {
          router.push({ name: "home" });
        })
        .catch(err => {
          submitLoading.value = false;
          console.log(err);
          if (err.code === 'ERR_NETWORK') {
            formState.msg = "网络错误";
          } else if (err.code === 'ERR_BAD_REQUEST') {
            formState.msg = "用户名或密码错误";
          } else {
            formState.msg = "未知错误";
          }
        });
    };

    const handleInputChange = () => {
      formState.msg = ""
    }

    return {
      formState,
      roleOptions,
      submitLoading,
      handleSubmit,
      handleInputChange,
    };
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

.login-card {
  width: 80%;
  max-width: 400px;
  margin: auto;
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

.login-card-container {
  padding: 20px;
  padding-bottom: 0;
}

.ant-card-hoverable {
  cursor: default;
}

</style>
