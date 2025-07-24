<template>
  <a-page-header title="患者信息" @back="handleBack" :ghost="false">
    <template #tags>
      <a-tag color="pink" v-if="patient?.resistance">IVIG 抵抗</a-tag>
      <a-tag color="red" v-if="patient?.relapse">复发</a-tag>
    </template>
    <template #extra>
      <a-tooltip title="编辑标签">
        <a-button type="link" size="small" @click="isUpdateModalVisible = true">
          <edit-outlined />
        </a-button>
      </a-tooltip>
      <a-tooltip title="提交新增数据">
        <a-button type="link" size="small" @click="handleSubmit" :loading="isSubmitting" :disabled="!isSubmitEnabled">
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
        <a-collapse-panel v-for="section in testSections" :key="section.key" :header="section.header">
          <a-inline-form :name="section.name" :label="section.header" :fields="section.fields" :span="section.span ?? '3'" />
        </a-collapse-panel>
      </a-collapse>
    </a-space>

    <a-modal v-model:open="isUpdateModalVisible" title="更新患者信息" @ok="handleUpdatePatient">
      <a-form :model="patientUpdateForm" layout="vertical" name="patientUpdate">
        <a-form-item label="IVIG 抵抗" name="resistance">
          <a-radio-group v-model:value="patientUpdateForm.resistance">
            <a-radio :value="true">是</a-radio>
            <a-radio :value="false">否</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="复发" name="relapse">
          <a-radio-group v-model:value="patientUpdateForm.relapse">
            <a-radio :value="true">是</a-radio>
            <a-radio :value="false">否</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal 
      v-model:open="isLeaveConfirmVisible" 
      title="确认离开" 
      @ok="confirmLeave"
      @cancel="isLeaveConfirmVisible = false"
      ok-text="确定离开"
      cancel-text="取消"
    >
      <p>您有未提交的数据，离开页面将丢失这些修改。确定要离开吗？</p>
    </a-modal>
  </a-page-header>
</template>

<script setup lang="ts">
import { defineAsyncComponent, reactive, ref, computed, onMounted, watch } from "vue";
import { useMainStore } from "@/stores";
import { EditOutlined, CheckOutlined } from "@ant-design/icons-vue";
import { updatePatient, updateTestByName, addTestByName, getTestsByPatientId } from "@/api/kawasaki";
import { useRouter, onBeforeRouteLeave, type NavigationGuardNext } from "vue-router";
import { useErrorHandler } from "@/composables/useErrorHandler";
import { testSections } from "./testSections.ts";

const APatientDetail = defineAsyncComponent(() => import("@/components/PatientDetail.vue"));
const AInlineForm = defineAsyncComponent(() => import("@/components/InlineForm.vue"));

const store = useMainStore();
const router = useRouter();
const { errorMessage, clearError, handleError } = useErrorHandler();

const patient = computed(() => store.patient);
const activeKey = ref<string[]>(['1']);
const isSubmitting = ref(false);
const isUpdateModalVisible = ref(false);
const isLeaveConfirmVisible = ref(false);
let nextRoute: NavigationGuardNext | null = null;

const patientUpdateForm = reactive({
  resistance: false,
  relapse: false,
});

watch(isUpdateModalVisible, (isVisible) => {
  if (isVisible && patient.value) {
    patientUpdateForm.resistance = patient.value.resistance;
    patientUpdateForm.relapse = patient.value.relapse;
  }
});

const isSubmitEnabled = computed(() => {
  const completed = store.complete;
  return Object.keys(completed).length > 0 && Object.values(completed).every(val => val);
});

const handleUpdatePatient = async () => {
  if (!patient.value) return;
  clearError();
  try {
    const data = { 
      ...patientUpdateForm, 
      version: patient.value.version || 0 
    };
    const updatedPatient = await updatePatient(patient.value.id!, data);
    store.setPatient(updatedPatient);
    isUpdateModalVisible.value = false;
  } catch (error) {
    handleError(error as any);
    isUpdateModalVisible.value = false;
  }
};

const handleBack = () => {
  router.back();
};

const confirmLeave = () => {
  isLeaveConfirmVisible.value = false;
  if (nextRoute) {
    nextRoute();
    nextRoute = null;
  }
};

const postData = async () => {
  if (!patient.value) return;

  const changes = store.getChangedTests();
  const hasChanges = Object.values(changes).some(c => c.added.length > 0 || c.updated.length > 0);
  if (!hasChanges) return;

  const operations = Object.entries(changes).flatMap(([testName, change]) => [
    ...change.added.map(item => addTestByName(testName, { ...item, patient: patient.value!.id })
      .catch(error => ({ error, item, type: 'add', testName }))
    ),
    ...change.updated.map(item => updateTestByName(testName, item.id, item)
      .catch(error => ({ error, item, type: 'update', testName }))
    )
  ]);

  const results = await Promise.all(operations);
  
  const errors = results.filter(r => r && r.error);
  if (errors.length > 0) {
    const errorMessages = errors.map(e => 
      `[${e.testName}] ${e.type} failed: ${e.error.message || e.error}`
    );
    throw new Error(`部分数据更新失败:\n${errorMessages.join('\n')}`);
  }

  await reloadPatientData();
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  clearError();
  try {
    await postData();
    store.setComplete({});
  } catch (error) {
    handleError(error as any);
  } finally {
    isSubmitting.value = false;
  }
};

const reloadPatientData = async () => {
  if (!patient.value?.id) return;
  try {
    const data = await getTestsByPatientId(patient.value.id);
    if (data && typeof data === 'object') {
      store.setTests(data);
    }
  } catch (error) {
    handleError(error as any);
  }
};

onBeforeRouteLeave((to, from, next) => {
  if (isSubmitEnabled.value) {
    isLeaveConfirmVisible.value = true;
    nextRoute = () => {
      store.setComplete({});
      next();
    };
    next(false);
  } else {
    next();
  }
});

onMounted(() => {
  if (patient.value && (!store.tests || Object.keys(store.tests).length === 0)) {
    reloadPatientData();
  }
});
</script>
