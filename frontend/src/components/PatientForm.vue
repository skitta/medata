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
      <a-form-item label="IVIG 抵抗" v-model:value="formState.resistance" name="resistance">
        <a-radio-group v-model:value="formState.resistance">
          <a-radio :value="true">是</a-radio>
          <a-radio :value="false">否</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item label="复发病历" v-model:value="formState.relapse" name="relapse">
        <a-radio-group v-model:value="formState.relapse">
          <a-radio :value="true">是</a-radio>
          <a-radio :value="false">否</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button type="primary" @click="showModal">确认</a-button>
      </a-form-item>
    </a-form>
    <a-modal v-model:visible="modalVisible" title="确认信息" @ok="handleOk" :confirm-loading="confireLoading">
      <p>{{ modalMsg }}</p>
    </a-modal>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, getCurrentInstance, onMounted, toRaw } from "vue";
import {
  Form, Input, Select, DatePicker, InputNumber, Button, Modal, Radio, message
} from "ant-design-vue";
import { useStore } from "vuex";

const { Item } = Form;
const { Option } = Select;
const { Group } = Radio;

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
    ARadioGroup: Group,
    ARadio: Radio,
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
      resistance: false,
      relapse: false
    });
    const groupOptions = ref([]);

    const modalVisible = ref(false);
    const modalMsg = ref("");
    const confireLoading = ref(false);

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
    let existPatient = {};
    const checkRegisteredID = async (rule, value) => {
      if (!value) {
        return Promise.reject("请输入登记号");
      }

      try {
        const response = await $http.get(`/kawasaki/patients?search=${value}`, { headers });
        if (response.data.count > 0) {
          existPatient = response.data.results[0];
          modalMsg.value = "登记号已存在，是否直接加载？";
          modalVisible.value = true;
          return Promise.reject("登记号已存在");
        } else {
          existPatient = {};
          modalMsg.value = "";
          modalVisible.value = false;
          return Promise.resolve();
        }
      } catch (error) {
        console.log(error);
        return Promise.reject("检索登记号失败");
      }
    };

    const rules = {
      registered_ID: [{ required: true, validator: checkRegisteredID, trigger: "blur" }],
      // document_ID: [{ required: true, message: "请输入住院号", trigger: "blur" }],
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
          modalMsg.value = "确认后部分字段将无法更改，是否确认？";
          modalVisible.value = true;
        })
        .catch(error => {
          console.log(error);
        });
    }

    const handleOk = () => {
      confireLoading.value = true;
      if (Object.keys(existPatient).length > 0) {
        // 如果数据库中存在该患者，则获取该患者的所有临床数据
        $http.get(
          `/kawasaki/all-tests-by-patient/${existPatient.id}/`,
          { headers }
        ).then(response => {
          store.dispatch("setTests", response.data);
          store.dispatch("setPatient", existPatient);
          confireLoading.value = false;
          modalVisible.value = false;
        }).catch(error => {
          console.log(error);
          confireLoading.value = false;
          modalMsg.value = "加载数据失败";
          message.error("加载数据失败");
        });
      } else {
        // 否则提交新患者至数据库
        $http.post(
          "/kawasaki/patients/",
          toRaw(formState),
          { headers }
        ).then(response => {
          store.dispatch("setPatient", response.data);
          confireLoading.value = false;
          modalVisible.value = false;
        }).catch(error => {
          console.log(error);
          confireLoading.value = false;
          modalMsg.value = "提交数据失败";
          message.error("提交数据失败");
        });
      }
    }

    onMounted(async () => {
      await getGroups();
    });

    return {
      formRef,
      formState,
      groupOptions,
      modalVisible,
      modalMsg,
      confireLoading,
      rules,
      showModal,
      handleOk,
    };
  }
})
</script>

<style scoped>
</style>