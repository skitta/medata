<template>
  <div class="login">
    <!-- <particles-bg type="cobweb" :bg="true" /> -->
    <a-card hoverable class="login-card">
      <template #cover>
        <div class="login-cover">
          <img src="@/assets/doctor.svg" alt="cover" />
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

<script setup lang="ts">
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import { reactive, ref } from "vue";
import { Form as AForm, Input as AInput, Button as AButton, Card as ACard, Select as ASelect, Alert as AAlert, InputPassword as AInputPassword } from "ant-design-vue";
import { useMainStore } from "@/stores";
import { useRouter } from "vue-router";
import { getToken } from "@/api/login";

interface FormState {
  user: string;
  password: string;
  role: string;
  msg: string;
}

interface RoleOption {
  value: string;
  label: string;
}

const store = useMainStore();
store.setToken(null);

const router = useRouter();

const formState = reactive<FormState>({
  user: "",
  password: "",
  role: "doctor",
  msg: "",
});

const roleOptions: RoleOption[] = [
  {
    value: "doctor",
    label: "Doctor",
  },
  {
    value: "patient",
    label: "Patient",
  },
];

const submitLoading = ref<boolean>(false);

const handleSubmit = (): void => {
  submitLoading.value = true;
  const { user, password } = formState;

  getToken(user, password)
    .then((token: string) => {
      store.setToken(token);
      submitLoading.value = false;
    })
    .then(() => {
      router.push({ name: "home" });
    })
    .catch((err: any) => {
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

const handleInputChange = (): void => {
  formState.msg = ""
}
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
  background-image: url("@/assets/login.bg.svg");
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
