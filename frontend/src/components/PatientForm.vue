<template>
<div>
  <a-form name="Patient" ref="formRef" :model="formState" :rules="rules" :label-col="{ span: 4 }"
    :wrapper-col="{ span: 18 }">
    <a-form-item label="登记号" name="registered_ID">
      <a-input v-model:value="formState.registered_ID" />
    </a-form-item>
    <a-form-item label="住院号" name="document_ID">
      <a-input v-model:value="formState.document_ID" />
    </a-form-item>
    <a-form-item label="姓名" name="full_name">
      <a-input v-model:value="formState.full_name" />
    </a-form-item>
    <a-form-item label="性别" name="gender">
      <a-select v-model:value="formState.gender">
        <a-select-option value="M">男</a-select-option>
        <a-select-option value="F">女</a-select-option>
      </a-select>
    </a-form-item>
    <a-form-item label="年龄(月)" name="age">
      <a-input-number v-model:value="formState.age" style="width: 100%" />
    </a-form-item>
    <a-form-item label="入院日期" name="in_date">
      <a-date-picker v-model:value="formState.in_date" value-format="YYYY-MM-DD" style="width: 100%" />
    </a-form-item>
    <a-form-item label="身高(cm)" name="height">
      <a-input-number v-model:value="formState.height" style="width: 100%" />
    </a-form-item>
    <a-form-item label="体重(kg)" name="weight">
      <a-input-number v-model:value="formState.weight" style="width: 100%" />
    </a-form-item>
    <a-form-item label="分组" v-model:value="formState.group" name="group">
      <a-select v-model:value="formState.group" :options="groupOptions"></a-select>
    </a-form-item>
    <a-form-item label="状态" v-model:value="formState.status" name="status">
      <a-select v-model:value="formState.status" :options="statusOptions"></a-select>
    </a-form-item>
    <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
      <a-button type="primary" @click="showModal">确认</a-button>
    </a-form-item>
  </a-form>
  <a-modal v-model:visible="visible" title="确认信息" @ok="handleOk">
    <p>确认后将无法更改，是否确认？</p>
  </a-modal>
</div>
</template>

<script>
import { defineComponent, ref, reactive, getCurrentInstance, onMounted, toRaw } from "vue";
import {
  Form, Input, Select, DatePicker, InputNumber, Button, Modal
} from "ant-design-vue";
import { useStore } from "vuex";

const { Item } = Form;
const { Option } = Select;

export default defineComponent({
  name: "PatientForm",
  components: {
    AForm: Form,
    AFormItem: Item,
    AInput: Input,
    ASelect: Select,
    ASelectOption: Option,
    ADatePicker: DatePicker,
    AInputNumber: InputNumber,
    AButton: Button,
    AModal: Modal,
  },
  setup() {
    const formRef = ref();
    const formState = reactive({
      registered_ID: "",
      document_ID: "",
      full_name: "",
      gender: "",
      age: undefined,
      in_date: undefined,
      height: undefined,
      weight: undefined,
      group: "",
      status: "",
    });

    const groupOptions = ref([]);

    const statusOptions = ref([
      { label: "在院", value: "1" },
      { label: "随访中", value: "2" },
      { label: "已完成", value: "3" },
    ]);

    const visible = ref(false);

    const currentInstance = getCurrentInstance();
    const { $http } = currentInstance.appContext.config.globalProperties;
    const store = useStore();
    const headers = {
      Authorization: `Token ${store.getters.getToken}`,
    }

    const getGroups = async () => {
      try {
        const response = await $http.get("/kawasaki/enrollGroups/", { headers });
        groupOptions.value = response.data.results.map(group => ({
          value: group.id,
          label: group.name,
        }));
        store.dispatch("setGroups", groupOptions.value);
      } catch (error) {
        console.log(error);
      }
    }

    let checkAge = async (rule, value) => {
      if (!value) {
        return Promise.reject("请输入年龄");
      }
      if (!Number.isInteger(value)) {
        return Promise.reject("年龄必须为整数");
      } else if (value < 0) {
        return Promise.reject("年龄不能小于0");
      } else {
        return Promise.resolve();
      }
    };

    let checkHeightAndWeight = async (rule, value) => {
      if (!value) {
        return Promise.reject("请输入数字");
      }
      if (value < 0) {
        return Promise.reject("不能小于0");
      }
      return Promise.resolve();
    };

    //TODO: 检索登记号是否已存在
    const checkRegisteredID = async (rule, value) => {
      if (!value) {
        return Promise.reject("请输入登记号");
      }
      try {
        const response = await $http.get(`/kawasaki/patients?search=${value}`, { headers });
        if (response.data.count > 0) {
          return Promise.reject("登记号已存在");
        }
      } catch (error) {
        console.log(error);
      }
      return Promise.resolve();
    };

    const rules = {
      registered_ID: [{ required: true, validator: checkRegisteredID, trigger: "blur" }],
      document_ID: [{ required: true, message: "请输入住院号", trigger: "blur" }],
      full_name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
      gender: [{ required: true, message: "请选择性别", trigger: "blur" }],
      age: [{ required: true, validator: checkAge, trigger: "blur" }],
      in_date: [{ required: true, message: "请选择日期", trigger: "blur" }],
      height: [{ required: true, validator: checkHeightAndWeight, trigger: "blur" }],
      weight: [{ required: true, validator: checkHeightAndWeight, trigger: "blur" }],
      group: [{ required: true, message: "请选择分组", trigger: "blur" }],
      status: [{ required: true, message: "请选择状态", trigger: "blur" }],
    };

    const showModal = () => {
      formRef.value
        .validate()
        .then(() => {
          visible.value = true;
        })
        .catch(error => {
          console.log(error);
        });
    }

    const handleOk = () => {
      store.dispatch("setPatient", toRaw(formState));
      visible.value = false;
    }

    onMounted(async () => {
      await getGroups();
    });

    return {
      formRef,
      formState,
      rules,
      groupOptions,
      statusOptions,
      visible,
      showModal,
      handleOk,
    };
  }
})
</script>

<style scoped>
</style>