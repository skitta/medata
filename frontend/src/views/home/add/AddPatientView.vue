<template>
  <a-card title="添加新患者">
    <a-alert
      v-if="errorMessage"
      :message="errorMessage"
      type="error"
      show-icon
      closable
      @close="clearError"
      style="margin-bottom: 16px"
    />
    <a-form name="Patient" ref="formRef" :model="formState" :rules="rules" v-bind="layout">
      <a-form-item has-feedback label="登记号" name="registered_ID">
        <a-input v-model:value="formState.registered_ID" />
      </a-form-item>
      <a-form-item label="住院号" name="document_ID">
        <a-input v-model:value="formState.document_ID" />
      </a-form-item>
      <a-form-item has-feedback label="姓名" name="full_name">
        <a-input v-model:value="formState.full_name" />
      </a-form-item>
      <a-form-item has-feedback label="性别" name="gender">
        <a-select v-model:value="formState.gender">
          <a-select-option value="M">男</a-select-option>
          <a-select-option value="F">女</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item has-feedback label="年龄(月)" name="age">
        <a-input-number v-model:value="formState.age" style="width: 100%" />
      </a-form-item>
      <a-form-item has-feedback label="入院日期" name="in_date">
        <a-date-picker v-model:value="formState.in_date" value-format="YYYY-MM-DD" style="width: 100%" />
      </a-form-item>
      <a-form-item has-feedback label="身高(cm)" name="height">
        <a-input-number v-model:value="formState.height" style="width: 100%" />
      </a-form-item>
      <a-form-item has-feedback label="体重(kg)" name="weight">
        <a-input-number v-model:value="formState.weight" style="width: 100%" />
      </a-form-item>
      <a-form-item has-feedback label="分组" name="group">
        <a-select v-model:value="formState.group" :options="groupOptions"></a-select>
      </a-form-item>
      <a-form-item label="IVIG 抵抗" name="resistance">
        <a-radio-group v-model:value="formState.resistance">
          <a-radio :value="true">是</a-radio>
          <a-radio :value="false">否</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item label="复发病历" name="relapse">
        <a-radio-group v-model:value="formState.relapse">
          <a-radio :value="true">是</a-radio>
          <a-radio :value="false">否</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button type="primary" @click="showModal">确认</a-button>
      </a-form-item>
    </a-form>
    <a-modal v-model:open="modalVisible" title="确认信息" @ok="handleOk" :confirm-loading="confireLoading">
      <p>{{ modalMsg }}</p>
    </a-modal>
  </a-card>
</template>

<script setup lang="ts">
import { ref, reactive, toRaw, onMounted } from "vue";
import {
  Card as ACard, Form as AForm, Input as AInput, Select as ASelect, DatePicker as ADatePicker, InputNumber as AInputNumber, Button as AButton, Modal as AModal, Radio as ARadio, Alert as AAlert, SelectOption as ASelectOption, RadioGroup as ARadioGroup, FormItem as AFormItem
} from "ant-design-vue";
import { useMainStore } from "@/stores";
import { getGroups, getPatients, getTestsByPatientId, addPatient } from "@/api/kawasaki";
import { useRouter } from "vue-router";
import type { Patient, SelectOption } from "@/types/api";
import type { Rule } from 'ant-design-vue/es/form';
import type { FormInstance } from 'ant-design-vue';
import { useErrorHandler } from "@/composables/useErrorHandler";
import { useFormValidation } from "@/composables/useFormValidation";

const formRef = ref<FormInstance | undefined>();
const { errorMessage, clearError, handleError } = useErrorHandler();
const { createRequiredRule, createNumberRule, createAsyncValidationRule } = useFormValidation();
const formState = reactive<Patient>({
  registered_ID: "",
  document_ID: "",
  full_name: "",
  gender: "",
  age: 0,
  in_date: "",
  height: 0,
  weight: 0,
  resistance: false,
  relapse: false,
});
const groupOptions = ref<SelectOption[]>([]);
onMounted(async () => {
  groupOptions.value = await getGroups();
});

const modalVisible = ref(false);
const modalMsg = ref("");
const confireLoading = ref(false);


// 验证登记号是否已存在
let existPatient: Patient | null = null;
const checkRegisteredID = createAsyncValidationRule(
  async (value: string) => {
    const data = await getPatients({ search: value });
    if (data.count > 0) {
      existPatient = data.results[0];
      modalMsg.value = "登记号已存在，是否直接加载？";
      modalVisible.value = true;
      return false;
    } else {
      existPatient = null;
      modalMsg.value = "";
      modalVisible.value = false;
      clearError();
      return true;
    }
  },
  "登记号已存在"
);

const rules: Record<string, Rule[]> = {
  registered_ID: [checkRegisteredID],
  full_name: [createRequiredRule("请输入姓名")],
  gender: [createRequiredRule("请选择性别")],
  age: [createNumberRule("年龄")],
  in_date: [createRequiredRule("请选择日期")],
  height: [createNumberRule("身高", 0)],
  weight: [createNumberRule("体重", 0)],
  group: [createRequiredRule("请选择分组")],
};

const layout = {
  labelCol: { span: 4 },
  wrapperCol: { span: 18 },
};

const showModal = () => {
  formRef.value
    ?.validate()
    .then(() => {
      modalMsg.value = "确认后部分字段将无法更改，是否确认？";
      modalVisible.value = true;
    })
    .catch(error => {
      console.log(error);
    });
}

const store = useMainStore();
const router = useRouter();

const handleOk = () => {
  confireLoading.value = true;
  clearError(); // 清除之前的错误
  
  if (existPatient && Object.keys(existPatient).length > 0) {
    // 如果数据库中存在该患者，则获取该患者的所有临床数据
    getTestsByPatientId(existPatient.id!)
      .then(data => {
        store.setTests(data);
        store.setPatient(existPatient!);
        confireLoading.value = false;
        modalVisible.value = false;
        router.push({ name: "add-tests" });
      }).catch(error => {
        confireLoading.value = false;
        modalVisible.value = false;
        handleError(error);
      });
  } else {
    // 否则提交新患者至数据库
    addPatient(toRaw(formState))
      .then(data => {
        store.setPatient(data);
        store.setTests({});
        confireLoading.value = false;
        modalVisible.value = false;
        router.push({ name: "add-tests" });
      }).catch(error => {
        confireLoading.value = false;
        modalVisible.value = false;
        handleError(error);
      });
  }
}
</script>
