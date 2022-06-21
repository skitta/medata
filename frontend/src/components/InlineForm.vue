<template>
  <div>
    <a-row class="table-row title">
      <template v-for="(item, key) in fields" :key="key">
        <a-col :span="5" v-if="item.type === 'date'">日期</a-col>
        <a-col :span="span" v-else>{{ item.label }}</a-col>
      </template>
    </a-row>
    <a-row>
      <a-col>
        <a-form :name="name" layout="inline" :model="dynamicValidateForm" ref="formRef">
          <a-row v-for="(inputData, index) in dynamicValidateForm.datas" :key="index" class="table-row">
            <template v-for="(item, key) in fields" :key="key">
              <a-col :span="5" v-if="item.type === 'date'">
                <a-form-item name="date">
                  <a-date-picker v-model:value="inputData.date" placeholder="选择日期" value-format="YYYY-MM-DD"
                    style="width: 100%" @change="handleChange"/>
                </a-form-item>
              </a-col>
              <a-col :span="span" v-else-if="item.type === 'number'">
                <a-form-item :name="key">
                  <a-input-number v-model:value="inputData[key]" :placeholder="item.label" @change="handleChange"/>
                </a-form-item>
              </a-col>
              <a-col :span="span" v-else-if="item.type === 'string'">
                <a-form-item :name="key">
                  <a-input v-model:value="inputData[key]" :placeholder="item.label" @change="handleChange"/>
                </a-form-item>
              </a-col>
              <a-col :span="span" v-else-if="item.type === 'select'">
                <a-form-item :name="key">
                  <a-select v-model:value="inputData[key]" :options="item.options" :placeholder="item.label" @change="handleChange"></a-select>
                </a-form-item>
              </a-col>
            </template>
            <a-col :span="1">
              <a-form-item>
                <MinusCircleOutlined v-if="dynamicValidateForm.datas.length > 0" class="dynamic-delete-button"
                  :disabled="dynamicValidateForm.datas.length === 0" @click="removeDomain(inputData)" />
              </a-form-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col>
              <a-form-item :wrapper-col="{ span: 24, offset: 2 }">
                <a-button type="dashed" @click="addDomain">
                  <PlusOutlined /> 添加{{ label }}
                </a-button>
                <a-button type="primary" v-if="showSaveButton" style="margin-left: 10px" html-type="submit"
                  @click="onSubmit">
                  <CheckOutlined /> 保存
                </a-button>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRaw } from "vue";
import { Form, DatePicker, Input, InputNumber, Row, Col, Button, Select } from "ant-design-vue";
import { MinusCircleOutlined, PlusOutlined, CheckOutlined } from '@ant-design/icons-vue';
import { useStore } from "vuex";

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
        gender: { type: 'select', label: '性别', options: [{value: 'F', label: 'Female'}] },
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
    const formRef = ref();
    const dynamicValidateForm = reactive({
      datas: [],
    });
    const showSaveButton = ref(false);

    const store = useStore();

    const removeDomain = (inputData) => {
      let index = dynamicValidateForm.datas.indexOf(inputData);
      if (index !== -1) {
        dynamicValidateForm.datas.splice(index, 1);
        showSaveButton.value = true;
      }
    };

    const addDomain = () => {
      let newdata = {}
      for (let key in props.fields) {
        newdata[key] = ''
      }
      dynamicValidateForm.datas.push(newdata);
      showSaveButton.value = true;
    };

    const handleChange = () => {
      showSaveButton.value = true;
    };

    // TODO：验证数据是否合法

    const onSubmit = () => {
      if (dynamicValidateForm.datas.length === 0) {
        showSaveButton.value = false;
        return;
      }
      store.dispatch('addTests', { name: props.name, data: toRaw(dynamicValidateForm.datas) });
      console.log('store', store.getters.getTests);
      showSaveButton.value = false;
    };

    return {
      formRef,
      dynamicValidateForm,
      showSaveButton,
      removeDomain,
      addDomain,
      handleChange,
      onSubmit
    };
  }
})
</script>

<style scoped>
.table-row {
  width: 100%;
  margin-bottom: 8px;
  padding: 8px;
}

.title {
  font-size: 14px;
  font-weight: bold;
  background-color: #fafafa;
}

.title .ant-col {
  padding-left: 10px;
}

.ant-input-number {
  width: 100%;
}
</style>