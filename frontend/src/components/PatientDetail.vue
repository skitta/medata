<template>
  <a-descriptions>
    <a-descriptions-item label="登记号">{{ patient.registered_ID }}</a-descriptions-item>
    <a-descriptions-item label="住院号">{{ patient.document_ID }}</a-descriptions-item>
    <a-descriptions-item label="姓名">{{ patient.full_name }}</a-descriptions-item>
    <a-descriptions-item label="性别">{{ patient.gender === 'M' ? '男':'女' }}</a-descriptions-item>
    <a-descriptions-item label="年龄">{{ patient.age }} 月</a-descriptions-item>
    <a-descriptions-item label="入院日期">{{ patient.in_date }}</a-descriptions-item>
    <a-descriptions-item label="身高">{{ patient.height }} cm</a-descriptions-item>
    <a-descriptions-item label="体重">{{ patient.weight }} kg</a-descriptions-item>
    <a-descriptions-item label="分组">{{ groupName }}</a-descriptions-item>
  </a-descriptions>
</template>

<script>
import { defineComponent } from "vue";
import { Descriptions } from "ant-design-vue";
import { useStore } from "vuex";
import { computed } from "@vue/reactivity";

const { Item } = Descriptions;

export default defineComponent({
  name: "PatientDetail",
  props: {
    patient: Object,
  },

  components: {
    ADescriptions: Descriptions,
    ADescriptionsItem: Item,
  },

  setup(props) {
    const store = useStore();
    const getGroupName = (group) => {
      const groupList = store.getters.getGroups;
      const groupName = groupList.find(item => item.value === group);
      return groupName ? groupName.label : "";
    };
    const groupName = computed(() => getGroupName(props.patient.group));

    return {
      groupName,
    };
  }
})
</script>

<style scoped>

</style>