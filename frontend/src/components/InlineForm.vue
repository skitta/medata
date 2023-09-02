<template>
<div class="inline-form-overflow">
  <div class="inline-form">
    <a-row class="table-row title">
      <template v-for="(item, key) in fields" :key="key">
        <a-col :span="5" v-if="item.type === 'date'">日期</a-col>
        <a-col :span="span" v-else>{{ item.label }}</a-col>
      </template>
    </a-row>
    <a-row>
      <a-col :span="24">
        <a-form :name="name" layout="inline" :model="dynamicValidateForm">
          <a-row v-for="(inputData, index) in dynamicValidateForm.datas" :key="index" class="table-row">
            <template v-for="(item, key) in fields" :key="key">
              <a-col :span="5" v-if="item.type === 'date'">
                <a-form-item name="date">
                  <a-date-picker v-model:value="inputData.date" placeholder="选择日期" value-format="YYYY-MM-DD"
                    style="width: 100%" @change="handleChange" />
                </a-form-item>
              </a-col>
              <a-col :span="span" v-else-if="item.type === 'number'">
                <a-form-item :name="key">
                  <a-input-number v-model:value="inputData[key]" :placeholder="item.label" @change="handleChange" />
                </a-form-item>
              </a-col>
              <a-col :span="span" v-else-if="item.type === 'string'">
                <a-form-item :name="key">
                  <a-input v-model:value="inputData[key]" :placeholder="item.label" @change="handleChange" />
                </a-form-item>
              </a-col>
              <a-col :span="span" v-else-if="item.type === 'select'">
                <a-form-item :name="key">
                  <a-select v-model:value="inputData[key]" :options="item.options" :placeholder="item.label"
                    @change="handleChange"></a-select>
                </a-form-item>
              </a-col>
            </template>
            <a-col :span="1">
              <a-form-item v-if="dynamicValidateForm.datas.length > 0" style="margin: 0">
                <a-button type="link" :disabled="disableDelete(inputData)" @click="removeDomain(inputData)"
                  style="padding: 2px">
                  <MinusCircleOutlined />
                </a-button>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col>
              <a-form-item :wrapper-col="{ span: 24 }" style="margin-left: 10px">
                <a-button type="dashed" @click="addDomain">
                  <PlusOutlined /> 添加{{ label }}
                </a-button>
                <a-button type="primary" v-if="showSaveButton" style="margin-left: 10px" @click="onSave"
                  :disabled="disableSave">
                  <CheckOutlined /> 保存
                </a-button>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </a-col>
    </a-row>
  </div>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRaw, watch } from "vue";
import { Form, DatePicker, Input, InputNumber, Row, Col, Button, Select } from "ant-design-vue";
import { MinusCircleOutlined, PlusOutlined, CheckOutlined } from '@ant-design/icons-vue';
import { useStore } from "vuex";
import { computed } from "@vue/reactivity";

const { Item } = Form;

export default defineComponent({
  name: "InlineForm",

  components: {
    AForm: Form,
    AFormItem: Item,
    ADatePicker: DatePicker,
    AInput: Input,
    AInputNumber: InputNumber,
    ARow: Row,
    ACol: Col,
    AButton: Button,
    ASelect: Select,
    MinusCircleOutlined,
    PlusOutlined,
    CheckOutlined
  },

  props: {
    name: {
      type: String,
    },
    label: {
      type: String,
    },
    fields: {
      type: Object,
      default: () => ({
        date: { type: 'date', label: '日期' },
        wbc: { type: 'number', label: 'WBC' },
        ne: { type: 'percentage', label: 'NE%' },
        label: { type: 'string', label: '标签' },
        gender: { type: 'select', label: '性别', options: [{ value: 'F', label: 'Female' }] },
        rbc: { type: 'number', label: 'RBC' },
        plt: { type: 'number', label: 'PLT' }
      })
    },
    span: {
      type: String,
      default: "3"
    }
  },

  setup(props) {
    const store = useStore();
    const dynamicValidateForm = reactive({
      datas: store.getters.getTestByName(props.name) ?? [],
    });
    const showSaveButton = ref(false);
    const disableSave = ref(true);
    const disableDelete = computed(() => {
      return (inputData) => {
        if (inputData.id !== undefined) {
          return true;
        } else {
          return false;
        }
      };
    });

    // 删除表单项事件
    const removeDomain = (inputData) => {
      let index = dynamicValidateForm.datas.indexOf(inputData);
      if (index !== -1) {
        dynamicValidateForm.datas.splice(index, 1);
      }
    };

    // 添加表单项事件
    const addDomain = () => {
      let newdata = {}
      for (let key in props.fields) {
        newdata[key] = ''
      }
      dynamicValidateForm.datas.push(newdata);
    };

    // 修改表单项事件
    const handleChange = () => {
      showSaveButton.value = true;
    };

    // 提交表单事件
    let storedDataLength = store.getters.getTestByName(props.name)?.length ?? 0;
    const onSave = () => {
      // 逻辑事件：
      // 对于一个空 datas，完成了一次表单填写，并点击了保存按钮 => store 保存了键值对数据
      // 然后删除了该表单，并点击了保存按钮 => store 将保存空键值对数据
      // 以下条件判断将删除该空键值对数据
      if (dynamicValidateForm.datas.length === 0) {
        store.dispatch('delTest', props.name);
        storedDataLength = 0;
      } else {
        store.dispatch('addTests', { name: props.name, data: toRaw(dynamicValidateForm.datas) });
        storedDataLength = store.getters.getTestByName(props.name).length;
      }
      showSaveButton.value = false;
    };

    // 监听所有表单是否完成，以控制完成状态
    watch([showSaveButton, disableSave], ([showBtnValue, disabled]) => {
      if (showBtnValue === false && disabled === false) {
        dynamicValidateForm.datas.forEach((item) => {
          if (item.id === undefined) {
            store.dispatch('addComplete', {
              name: props.name,
              data: true
            });
          }
        })
      } else {
        store.dispatch('addComplete', {
          name: props.name,
          data: false
        });
      }
    });

    // 监听表单数据是否完整，以控制保存按钮的启用状态
    watch(dynamicValidateForm.datas, (currentValue) => {
      showSaveButton.value = (currentValue.length === storedDataLength) ? false : true;
      currentValue.forEach(item => {
        for (let key in item) {
          if (item[key] === '') {
            disableSave.value = true;
            return;
          }
        }
        disableSave.value = false;
      });
    });

    return {
      dynamicValidateForm,
      showSaveButton,
      removeDomain,
      addDomain,
      handleChange,
      onSave,
      disableSave,
      disableDelete
    };
  }
})
</script>

<style scoped>
.inline-form-overflow {
  max-width: fit-content;
  overflow: auto;
}

.inline-form {
  min-width: 680px;
  padding: 10px 0;
}

.table-row {
  width: 100%;
  margin-bottom: 8px;
  padding: 8px;
}

.title {
  /* font-size: 14px; */
  /* font-weight: bold; */
  background-color: #fafafa;
}

.title .ant-col {
  padding-left: 10px;
}

.ant-input-number {
  width: 100%;
}
</style>