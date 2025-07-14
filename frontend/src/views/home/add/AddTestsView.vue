<template>
  <a-page-header title="患者信息" @back="handleCancel" :ghost="false">
    <template #tags>
      <a-tag color="pink" v-if="patient?.resistance">IVIG 抵抗</a-tag>
      <a-tag color="red" v-if="patient?.relapse">复发</a-tag>
    </template>
    <template #extra>
      <a-tooltip>
        <template #title>编辑标签</template>
        <a-button type="link" size="small" @click="onUpdatePatient">
          <edit-outlined />
        </a-button>
      </a-tooltip>
      <a-tooltip>
        <template #title>提交新增数据</template>
        <a-button type="link" size="small" @click="handleSubmit" :loading="btnLoading" :disabled="!showSubmitBtn">
          <check-outlined />
        </a-button>
      </a-tooltip>
    </template>

    <a-space direction="vertical" style="width: 100%">
      <a-alert
        v-if="errorMessage"
        :message="errorMessage"
        type="error"
        show-icon
        closable
        @close="clearError"
        style="margin-bottom: 16px"
      />
      <a-patient-detail v-if="patient" :patient="patient" />
      <a-collapse v-model:activeKey="activeKey" ghost>
        <a-collapse-panel key="1" header="血常规">
          <a-inline-form name="bloodTests" label="血常规" :fields="bloodTest" />
        </a-collapse-panel>
        <a-collapse-panel key="2" header="肝功能">
          <a-inline-form name="liverFunction" label="肝功能" :fields="liverFunction" />
        </a-collapse-panel>
        <a-collapse-panel key="3" header="心脏彩超">
          <a-inline-form name="echocardiography" label="心脏彩超" :fields="echocardiography" span="4" />
        </a-collapse-panel>
        <a-collapse-panel key="4" header="感染性指标">
          <a-inline-form name="infectiousTests" label="感染性指标" :fields="infectiousTest" span="9" />
        </a-collapse-panel>
        <a-collapse-panel key="5" header="其他辅助检查">
          <a-inline-form name="customTests" label="其他辅助检查" :fields="customTest" span="4" />
        </a-collapse-panel>
        <a-collapse-panel key="6" header="样本信息">
          <a-inline-form name="samples" label="标本" :fields="samples" span="4" />
        </a-collapse-panel>
      </a-collapse>
    </a-space>

    <a-modal v-model:open="updateModalVisible" title="更新患者信息" @ok="handleUpdate">
      <a-form :model="formState" layout="vertical" name="patientUpdate">
        <a-form-item label="IVIG 抵抗" name="resistance">
          <a-radio-group v-model:value="formState.resistance">
            <a-radio :value="true">是</a-radio>
            <a-radio :value="false">否</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="复发" name="relapse">
          <a-radio-group v-model:value="formState.relapse">
            <a-radio :value="true">是</a-radio>
            <a-radio :value="false">否</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-page-header>
</template>

<script setup lang="ts">
import { defineAsyncComponent, reactive, ref, toRaw, computed } from "vue";
import { PageHeader as APageHeader, Space as ASpace, Collapse as ACollapse, Button as AButton, Tooltip as ATooltip, Modal as AModal, Tag as ATag, Form as AForm, Radio as ARadio, Alert as AAlert, CollapsePanel as ACollapsePanel, RadioGroup as ARadioGroup, FormItem as AFormItem } from "ant-design-vue";
import { useMainStore } from "@/stores";
import { EditOutlined, CheckOutlined } from "@ant-design/icons-vue";
import { updatePatient, updateTestByName, addTestByName } from "@/api/kawasaki";
import { useRouter } from "vue-router";
import { InlineFormField } from "@/types/components";
import type { Patient } from "@/types/api";
import { useErrorHandler } from "@/composables/useErrorHandler";

const APatientDetail = defineAsyncComponent(() =>
  import("@/components/PatientDetail.vue")
);
const AInlineForm = defineAsyncComponent(() =>
  import("@/components/InlineForm.vue")
);

const store = useMainStore();
const { errorMessage, clearError, handleError } = useErrorHandler();


const patient = computed<Patient | null>(() => store.patient);
const activeKey = ref<string[]>(['1']);
const bloodTest: InlineFormField = {
  date: { type: 'date', label: '日期' },
  wbc: { type: 'number', label: 'WBC' },
  ne: { type: 'number', label: 'NE%' },
  ly: { type: 'number', label: 'LY%' },
  mo: { type: 'number', label: 'MO%' },
  rbc: { type: 'number', label: 'RBC' },
  plt: { type: 'number', label: 'PLT' }
};
const liverFunction: InlineFormField = {
  date: { type: 'date', label: '日期' },
  ast: { type: 'number', label: 'AST' },
  alt: { type: 'number', label: 'ALT' },
  tbil: { type: 'number', label: '总胆红素' },
  dbil: { type: 'number', label: '直接胆红素' },
  tb: { type: 'number', label: '总蛋白' },
  alb: { type: 'number', label: '白蛋白' },
};
const echocardiography: InlineFormField = {
  date: { type: 'date', label: '日期' },
  lmca: { type: 'number', label: '左主干' },
  lmca_z: { type: 'number', label: '左主干Z值' },
  rca: { type: 'number', label: '右支' },
  rca_z: { type: 'number', label: '右支Z值' },
};
const infectiousTest: InlineFormField = {
  date: { type: 'date', label: '日期' },
  pct: { type: 'number', label: 'PCT' },
  crp: { type: 'number', label: 'CRP' },
};
const customTest: InlineFormField = {
  name: { type: 'string', label: '检验名称' },
  date: { type: 'date', label: '日期' },
  result: { type: 'number', label: '结果' },
  notes: { type: 'string', label: '备注' }
};
const samples: InlineFormField = {
  date: { type: 'date', label: '日期' },
  label: { type: 'string', label: '标签' },
  sample_type: {
    type: 'select', label: '样本类型', options: [
      { label: '全血', value: '0' },
      { label: '血清', value: '1' },
      { label: '血浆', value: '2' },
      { label: 'PBMCs', value: '3' },
      { label: '其他', value: '4' },
    ]
  },
  sample_status: {
    type: 'select', label: '样本状态', options: [
      { label: '待处理', value: '0' },
      { label: '已处理', value: '1' },
      { label: '已销毁', value: '2' },
    ]
  },
  note: { type: 'string', label: '备注' },
};

const formState = reactive<{
  resistance: boolean;
  relapse: boolean;
}>({
  resistance: false,
  relapse: false,
});

const btnLoading = ref(false);
const showSubmitBtn = computed(() => {
  const completed: { [key: string]: boolean } = store.complete;
  if (Object.keys(completed).length === 0) {
    return false;
  }
  for (let key in completed) {
    if (completed[key] === false) {
      return false;
    }
  }
  return true;
});
const updateModalVisible = ref(false);

const onUpdatePatient = () => {
  if (!patient.value) return;
  formState.resistance = patient.value.resistance;
  formState.relapse = patient.value.relapse;
  updateModalVisible.value = true;
};

const handleUpdate = () => {
  if (!patient.value) return;
  clearError(); // 清除之前的错误
  const data = { 
    ...toRaw(formState), 
    version: patient.value.version || 0 
  };
  updatePatient(patient.value.id!, data).then(data => {
    updateModalVisible.value = false;
    store.setPatient(data);
  }).catch(error => {
    updateModalVisible.value = false;
    handleError(error);
  });
};

const router = useRouter();
const handleCancel = () => {
  // 若数据未提交，提醒用户确认
  if (showSubmitBtn.value) {
    console.log(showSubmitBtn.value);
    return;
  }
  store.setComplete({});
  router.back();
};

const postData = () => {
  if (!patient.value) return Promise.resolve([]);
  const tests: Record<string, any[]> = store.tests;

  // tests根据id来区分操作：
  // 1. patient id 为必须字段
  // 2. test id 由数据库自动生成，据此可以判断是新增还是更新
  let promiseList: Promise<any>[] = [];
  for (let key in tests) {
    for (let [index, oneTest] of tests[key].entries()) {
      // 如果id为空，则为新增，否则为更新
      if (oneTest.id !== undefined) {
        promiseList.push(
          updateTestByName(key, oneTest.id, oneTest)
        );
      } else {
        oneTest.patient = patient.value.id!;
        promiseList.push(
          addTestByName(key, oneTest)
            .then(data => {
              tests[key][index] = data;
            })
        );
      }
    }
  }
  return Promise.all(promiseList);
};

const handleSubmit = () => {
  btnLoading.value = true;
  clearError(); // 清除之前的错误
  
  postData().then(() => {
    btnLoading.value = false;
    // 将completed重设为初始状态
    store.setComplete({});
  }).catch(error => {
    btnLoading.value = false;
    handleError(error);
  });
}
</script>
