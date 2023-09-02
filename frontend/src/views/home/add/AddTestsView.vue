<template>
  <a-page-header title="患者信息" @back="handleCancel" :ghost="false">
    <template #tags>
      <a-tag color="pink" v-if="patient.resistance">IVIG 抵抗</a-tag>
      <a-tag color="red" v-if="patient.relapse">复发</a-tag>
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
      <a-patient-detail :patient="patient" />
      <a-collapse v-model:activeKey="activeKey" ghost>
        <a-collapse-panel key="1" header="血常规">
          <a-inline-form name="bloodTests" label="血常规" :fields="bloodTest" />
        </a-collapse-panel>
        <a-collapse-panel key="2" header="肝功能">
          <a-inline-form name="liverFunction" label="肝功能" :fields="liverFunction" span="6" />
        </a-collapse-panel>
        <a-collapse-panel key="3" header="心脏彩超">
          <a-inline-form name="echocardiography" label="心脏彩超" :fields="echocardiography" span="4" />
        </a-collapse-panel>
        <a-collapse-panel key="4" header="其他辅助检查">
          <a-inline-form name="otherTests" label="其他辅助检查" :fields="otherTest" span="9" />
        </a-collapse-panel>
        <a-collapse-panel key="5" header="样本信息">
          <a-inline-form name="samples" label="标本" :fields="samples" span="4" />
        </a-collapse-panel>
      </a-collapse>
    </a-space>

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
  </a-page-header>
</template>

<script>
import { defineComponent, defineAsyncComponent, toRefs, reactive, ref, toRaw } from "vue";
import { PageHeader, Space, Collapse, Button, Tooltip, Modal, Tag, Form, Radio, message } from "ant-design-vue";
import { useStore } from "vuex";
import { computed } from "@vue/reactivity";
import { EditOutlined, CheckOutlined } from "@ant-design/icons-vue";
import { updatePatient, updateTestByName, addTestByName } from "@/api/kawasaki";
import { useRouter } from "vue-router";

const { Item } = Form;
const { Group } = Radio;
const { Panel } = Collapse;

export default defineComponent({
  name: "AddTestsView",
  components: {
    APageHeader: PageHeader,
    ASpace: Space,
    ACollapse: Collapse,
    ACollapsePanel: Panel,
    AButton: Button,
    ATooltip: Tooltip,
    AModal: Modal,
    ATag: Tag,
    AForm: Form,
    AFormItem: Item,
    ARadioGroup: Group,
    ARadio: Radio,
    EditOutlined,
    CheckOutlined,
    APatientDetail: defineAsyncComponent(() =>
      import("@/components/PatientDetail.vue")
    ),
    AInlineForm: defineAsyncComponent(() =>
      import("@/components/InlineForm.vue")
    ),
  },

  setup() {
    const store = useStore();
    const state = reactive({
      patient: computed(() => store.getters.getPatient),
      activeKey: ref(['1']),
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
    const showSubmitBtn = computed(() => {
      const completed = store.getters.getComplete;
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
      formState.resistance = state.patient.resistance;
      formState.relapse = state.patient.relapse;
      updateModalVisible.value = true;
    };

    const handleUpdate = () => {
      updatePatient(state.patient.id, toRaw(formState)).then(data => {
        updateModalVisible.value = false;
        store.dispatch("setPatient", data);
      }).catch(err => {
        message.error(err);
      });
    };

    const router = useRouter();
    const handleCancel = () => {
      // 若数据未提交，提醒用户确认
      if (showSubmitBtn.value) {
        message.warning("您有数据尚未提交");
        console.log(showSubmitBtn.value);
        return;
      }
      store.dispatch("setComplete", {});
      router.back();
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
              updateTestByName(key, oneTest.id, oneTest)
            );
          } else {
            oneTest.patient = state.patient.id;
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
      showSubmitBtn,
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
</style>