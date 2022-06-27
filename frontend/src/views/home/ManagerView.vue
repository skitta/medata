<template>
  <a-table :columns="columns" :data-source="dataSource" :pagination="pagination" :loading="loading"
    @change="handleTableChange">
    <template #tags="{ text: tags }">
      <span>
        <a-tag v-for="tag in tags" :key="tag" :color="tag === 'IVIG抵抗' ? 'pink' : tag === '复发' ? 'red' : 'blue'">
          {{ tag }}
        </a-tag>
      </span>
    </template>
  </a-table>
</template>

<script>
import { defineComponent } from "vue";
import { Table, Tag } from "ant-design-vue";
import { usePagination } from 'vue-request'
import { computed } from "@vue/reactivity";
import { getGroups, getPatients } from "@/api/kawasaki";

const columns = [
  {
    title: "登记号",
    dataIndex: "registered_ID",
    key: "registered_ID",
  },
  {
    title: "姓名",
    dataIndex: "full_name",
    key: "full_name",
  },
  {
    title: "入院日期",
    dataIndex: "in_date",
    key: "in_date",
  },
  {
    title: "分组",
    dataIndex: "group",
    key: "group",
  },
  {
    title: "标签",
    dataIndex: "tags",
    key: "tags",
    slots: {
      customRender: "tags",
    },
  }
]

export default defineComponent({
  components: {
    ATable: Table,
    ATag: Tag,
  },

  setup() {
    const { data, run, loading, current, pageSize } = usePagination(getPatients);

    const pagination = computed(() => {
      return {
        current: current.value,
        pageSize: pageSize.value,
        total: data.value?.count,
      };
    });

    const dataSource = computed(() => {
      const groupList = getGroups();
      return data.value?.results.map(patient => {
        let tags = [];
        if (patient.resistance) {
          tags.push("IVIG抵抗");
        }
        if (patient.relapse) {
          tags.push("复发");
        }
        return {
          key: patient.id,
          registered_ID: patient.registered_ID,
          full_name: patient.full_name,
          in_date: patient.in_date,
          group: groupList.find(item => item.value === patient.group)?.label || "未确定",
          tags: tags,
        };
      });
    });

    const handleTableChange = (pagination) => {
      run({
        current: pagination?.current
      });
    };

    return {
      columns,
      dataSource,
      pagination,
      loading,
      handleTableChange,
    };
  }
})
</script>

<style scoped>
</style>