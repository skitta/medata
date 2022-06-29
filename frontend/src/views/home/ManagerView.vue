<template>
  <a-space direction="vertical" style="width: 100%">
    <a-row>
      <a-col :span="4">
        <a-input placeholder="搜索" @press-enter="onSearch">
          <template #prefix>
            <search-outlined style="color: rgba(0,0,0,.5)" />
          </template>
        </a-input>
      </a-col>
    </a-row>

    <a-row>
      <a-col :span="24">
        <a-table :columns="columns" :data-source="dataSource" :pagination="pagination" :loading="loading"
          @change="handleTableChange" :bordered="true">
          <template #bodyCell="{ column, text }">
            <span v-if="column.dataIndex === 'tags'">
              <a-tag v-for="tag in text" :key="tag" :color="tag === 'IVIG抵抗' ? 'pink' : tag === '复发' ? 'red' : 'blue'">
                {{ tag }}
              </a-tag>
            </span>
          </template>
        </a-table>
      </a-col>
    </a-row>
  </a-space>

</template>

<script>
import { defineComponent } from "vue";
import { Table, Tag, Input, Row, Col, Space } from "ant-design-vue";
import { usePagination } from 'vue-request'
import { computed } from "@vue/reactivity";
import { getGroups, getPatients } from "@/api/kawasaki";
import { SearchOutlined } from "@ant-design/icons-vue";

const groupList = getGroups();

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
    sorter: true,
    width: '20%'
  },
  {
    title: "分组",
    dataIndex: "group",
    key: "group",
    filters: groupList.map(group => ({ text: group.label, value: group.value })),
  },
  {
    title: "标签",
    dataIndex: "tags",
    key: "tags",
    filters: [
      { text: "IVIG抵抗", value: "resistance" },
      { text: "复发", value: "relapse" },
    ],
  }
]

export default defineComponent({
  components: {
    ARow: Row,
    ACol: Col,
    ATable: Table,
    ATag: Tag,
    AInput: Input,
    ASpace: Space,
    SearchOutlined,
  },

  setup() {
    const { data, run, loading, current, pageSize } = usePagination(getPatients, {
      pagination: {
        currentKey: "page",
        pageSizeKey: "results",
      }
    });

    const pagination = computed(() => {
      return {
        current: current.value,
        pageSize: pageSize.value,
        total: data.value?.count,
      };
    });

    const dataSource = computed(() => {
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

    const handleTableChange = (pagination, filters, sorter) => {
      const sortField = () => {
        if (sorter.order === "ascend") {
          return sorter.field;
        } else if (sorter.order === "descend") {
          return `-${sorter.field}`;
        } else {
          return null;
        }
      }

      const { group, tags } = filters

      const tagsFilter = {}
      tags?.forEach(key => tagsFilter[key] = true)

      run({
        page: pagination?.current,
        ordering: sortField(),
        group__in: group?.toString(),
        ...tagsFilter,
      });
    };

    const onSearch = (e) => {
      run({
        page: 1,
        search: e.target.value,
      });
    }

    return {
      columns,
      dataSource,
      pagination,
      loading,
      handleTableChange,
      onSearch,
    };
  }
})
</script>

<style scoped>
</style>