<template>
  <div class="add-form">
    <a-row v-if="patient">
      <a-col :span="12" :offset="6">
        <a-card title="患者信息">
          <a-patient-detail :patient="patient" />
          <a-divider />
          <a-inline-form name="bloodTests" label="血常规" :fields="bloodTest" />
          <a-divider />
          <a-inline-form name="liverFunction" label="肝功能" :fields="liverFunction" span="6" />
          <a-divider />
          <a-inline-form name="echocardiography" label="心脏彩超" :fields="echocardiography" span="4" />
          <a-divider />
          <a-inline-form name="otherTests" label="其他辅助检查" :fields="otherTest" span="9" />
          <a-divider />
          <a-inline-form name="samples" label="标本" :fields="samples" span="4" />
          <a-divider />
          <a-button type="primary" danger @click="handleCancel">取消</a-button>
          <a-button type="primary" style="margin-left: 16px" @click="confirmSubmit" :disabled="disableSubmit">提交
          </a-button>
        </a-card>
        <a-modal v-model:visible="visible" title="确认信息" @ok="handleSubmit">
          <p>确认后将无法更改，是否确认？</p>
        </a-modal>
      </a-col>
    </a-row>
    <a-row v-if="!patient">
      <a-col :span="12" :offset="6">
        <a-card title="添加新患者">
          <a-patient-form />
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { defineComponent, defineAsyncComponent, toRefs, reactive, ref, getCurrentInstance } from "vue";
import { Card, Row, Col, Divider, Button, Modal } from "ant-design-vue";
import { useStore } from "vuex";
import { computed } from "@vue/reactivity";

export default defineComponent({
  name: "AddView",

  components: {
    ACard: Card,
    ARow: Row,
    ACol: Col,
    ADivider: Divider,
    AButton: Button,
    AModal: Modal,
    APatientDetail: defineAsyncComponent(() =>
      import("@/components/PatientDetail.vue")
    ),
    APatientForm: defineAsyncComponent(() =>
      import("@/components/PatientForm.vue")
    ),
    AInlineForm: defineAsyncComponent(() =>
      import("@/components/InlineForm.vue")
    ),
  },

  setup() {
    const store = useStore();
    const currentInstance = getCurrentInstance();
    const { $http } = currentInstance.appContext.config.globalProperties;
    const headers = {
      Authorization: `Token ${store.getters.getToken}`,
    }
    const state = reactive({
      patient: computed(() => store.getters.getPatient),
      bloodTest: {
        date: { type: 'date', label: '日期' },
        wbc: { type: 'number', label: 'WBC' },
        ne: { type: 'number', label: 'NE%' },
        ly: { type: 'number', label: 'LY%' },
        mo: { type: 'number', label: 'MO%' },
        rbc: { type: 'number', label: 'RBC' },
        plt: { type: 'number', label: 'PLT' }
      },
      liverFunction: {
        date: { type: 'date', label: '日期' },
        ast: { type: 'number', label: 'AST' },
        alt: { type: 'number', label: 'ALT' },
        pa: { type: 'number', label: 'PA' },
      },
      echocardiography: {
        date: { type: 'date', label: '日期' },
        lmca: { type: 'number', label: '左主干' },
        lmca_z: { type: 'number', label: '左主干Z值' },
        rca: { type: 'number', label: '右支' },
        rca_z: { type: 'number', label: '右支Z值' },
      },
      otherTest: {
        date: { type: 'date', label: '日期' },
        pct: { type: 'number', label: 'PCT' },
        crp: { type: 'number', label: 'CRP' },
        // tg: { type: 'number', label: 'TG' },
      },
      samples: {
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
      }
    });
    const visible = ref(false);
    const disableSubmit = computed(() => {
      const completed = store.getters.getComplete;
      for (let key in completed) {
        if (completed[key] === false) {
          return true;
        }
      }
      return false;
    });

    const handleCancel = () => {
      store.dispatch("setPatient", null);
      store.dispatch('setTests', {});
    };

    const confirmSubmit = () => {
      visible.value = true;
    };

    const handleSubmit = async () => {
      const patient = store.getters.getPatient;
      const tests = store.getters.getTests;
      try {
        const res = await $http.post(`/kawasaki/patients/`, patient, { headers });
        const patientId = res.data.id;
        Object.keys(tests).forEach(key => {
          for (let oneTest of tests[key]) {
            oneTest.patient = patientId;
            $http.post(`/kawasaki/${key}/`, oneTest, { headers });
          }
        });
        handleCancel();
        visible.value = false;
      } catch (error) {
        console.log(error);
      }
    };

    return {
      ...toRefs(state),
      handleCancel,
      confirmSubmit,
      visible,
      disableSubmit,
      handleSubmit,
    };
  }
})
</script>

<style scoped>
.ant-row {
  margin-bottom: 20px;
}
</style>