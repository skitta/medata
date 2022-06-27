<template>
  <div class="add-form">
    <a-row v-if="patient">
      <a-col :span="12" :offset="6">
        <a-card title="患者信息">
          <template #extra>
            <a-tag color="pink" v-if="patient.resistance">IVIG 抵抗</a-tag>
            <a-tag color="red" v-if="patient.relapse">复发</a-tag>
            <a-button type="link" size="small" @click="onUpdatePatient">
              <edit-outlined />
            </a-button>
          </template>
          <a-patient-detail :patient="patient" />
        </a-card>

        <a-card title="临床资料">
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
          <a-button type="default" @click="handleCancel" :disabled="disableCancel">返回</a-button>
          <a-button type="primary" style="margin-left: 16px" @click="handleSubmit" :loading="btnLoading"
            :disabled="disableSubmit">提交
          </a-button>
        </a-card>

        <a-modal v-model:visible="updateModalVisible" title="更新患者信息" @ok="handleUpdate">
          <a-form :model="formState" layout="vertical" name="patientUpdate">
            <a-form-item label="IVIG 抵抗" v-model:value="formState.resistance" name="resistance">
              <a-radio-group v-model:value="formState.resistance">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item label="复发" v-model:value="formState.relapse" name="relapse">
              <a-radio-group v-model:value="formState.relapse">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-form>
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
import { defineComponent, defineAsyncComponent, toRefs, reactive, ref, getCurrentInstance, toRaw } from "vue";
import { Card, Row, Col, Divider, Button, Modal, Tag, Form, Radio, message } from "ant-design-vue";
import { useStore } from "vuex";
import { computed } from "@vue/reactivity";
import { EditOutlined } from "@ant-design/icons-vue";

const { Item } = Form;
const { Group } = Radio;

export default defineComponent({
  name: "AddView",

  components: {
    ACard: Card,
    ARow: Row,
    ACol: Col,
    ADivider: Divider,
    AButton: Button,
    AModal: Modal,
    ATag: Tag,
    AForm: Form,
    AFormItem: Item,
    ARadioGroup: Group,
    ARadio: Radio,
    EditOutlined,
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
    const formState = reactive({
      resistance: false,
      relapse: false,
    })

    const btnLoading = ref(false);
    const disableCancel = computed(() => {
      return btnLoading.value;
    });
    const disableSubmit = computed(() => {
      const completed = store.getters.getComplete;
      if (Object.keys(completed).length === 0) {
        return true;
      }
      for (let key in completed) {
        if (completed[key] === false) {
          return true;
        }
      }
      return false;
    });
    const updateModalVisible = ref(false);

    const onUpdatePatient = () => {
      formState.resistance = state.patient.resistance;
      formState.relapse = state.patient.relapse;
      updateModalVisible.value = true;
    };

    const handleUpdate = () => {
      $http.patch(
        `/kawasaki/patients/${state.patient.id}/`,
        toRaw(formState),
        { headers }
      ).then(res => {
        updateModalVisible.value = false;
        store.dispatch("setPatient", res.data);
      }).catch(err => {
        message.error(err.response.data.detail);
      });
    };

    const handleCancel = () => {
      store.dispatch("setPatient", null);
      store.dispatch('setTests', {});
    };

    const postData = () => {
      const tests = store.getters.getTests;

      // tests根据id来区分操作：
      // 1. patient id 为必须字段
      // 2. test id 由数据库自动生成，据此可以判断是新增还是更新
      let promiseList = [];
      for (let key in tests) {
        for (let [index, oneTest] of tests[key].entries()) {
          // 如果id为空，则为新增，否则为更新
          if (oneTest.id !== undefined) {
            promiseList.push(
              $http.put(`/kawasaki/${key}/${oneTest.id}/`, oneTest, { headers })
            );
          } else {
            oneTest.patient = state.patient.id;
            promiseList.push(
              $http.post(`/kawasaki/${key}/`, oneTest, { headers })
              .then(res => {
                tests[key][index] = res.data;
              })
            );
          }
        }
      }
      return Promise.all(promiseList);
    };

    const handleSubmit = () => {
      btnLoading.value = true;
      postData().then(() => {
        btnLoading.value = false;
        // 将completed重设为初始状态
        store.dispatch('setComplete', {});
        message.success('数据提交成功');
      }).catch(error => {
        btnLoading.value = false;
        message.error('数据提交失败');
        console.log(error);
      });
    }

    return {
      ...toRefs(state),
      formState,
      btnLoading,
      disableCancel,
      disableSubmit,
      updateModalVisible,

      onUpdatePatient,
      handleUpdate,
      handleCancel,
      handleSubmit,
    };
  }
})
</script>

<style scoped>
.ant-row {
  margin-bottom: 20px;
}

.ant-card {
  margin-bottom: 20px;
}
</style>