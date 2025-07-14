<template>
  <a-descriptions :bordered="true">
    <a-descriptions-item label="登记号">{{ patient.registered_ID }}</a-descriptions-item>
    <a-descriptions-item label="住院号">{{ patient.document_ID }}</a-descriptions-item>
    <a-descriptions-item label="姓名">{{ patient.full_name }}</a-descriptions-item>
    <a-descriptions-item label="性别">{{ patient.gender === 'M' ? '男':'女' }}</a-descriptions-item>
    <a-descriptions-item label="年龄">{{ patient.age }} 月</a-descriptions-item>
    <a-descriptions-item label="入院日期">{{ patient.in_date }}</a-descriptions-item>
    <a-descriptions-item label="身高">{{ patient.height }} cm</a-descriptions-item>
    <a-descriptions-item label="体重">{{ patient.weight }} kg</a-descriptions-item>
    <a-descriptions-item label="分组">{{ store.getGroupNameById(patient.group) }}</a-descriptions-item>
  </a-descriptions>
</template>

<script setup lang="ts">
import { Descriptions as ADescriptions, DescriptionsItem as ADescriptionsItem } from "ant-design-vue";
import { useMainStore } from "@/stores";
import { Patient } from "@/types/api";

const props = defineProps({
  patient: {
    type: Object as () => Patient,
    required: true
  }
});

const store = useMainStore();
</script>
