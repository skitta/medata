<template>
  <div class="nav-view-container">
    <a-space direction="vertical" style="width: 100%">
      <a-row justify="space-between">
        <a-col :xs="12" :md="6" :lg="6" :xl="4">
          <a-input placeholder="搜索" :allow-clear="true" @press-enter="onSearch" @change="onSearch">
            <template #prefix>
              <search-outlined style="color: rgba(0,0,0,.5)" />
            </template>
          </a-input>
        </a-col>
        <a-col :md="4" :lg="2" style="text-align: right">
          <a-dropdown :trigger="['click']">
            <template #overlay>
              <a-menu @click="handleExport">
                <a-menu-item key="1">所有数据</a-menu-item>
                <a-menu-item key="2">所选数据</a-menu-item>
              </a-menu>
            </template>
            <a-button type="primary">
              <download-outlined />
              导出
            </a-button>
          </a-dropdown>

        </a-col>
      </a-row>

      <a-row>
        <a-col :span="24">
          <a-table :columns="columns" :data-source="dataSource" :pagination="pagination" :loading="loading"
            @change="handleTableChange" :bordered="true">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'registered_ID'">
                <a-button type="link" @click="gotoAdd">{{ record.registered_ID }}</a-button>
              </template>
              <template v-if="column.key === 'tags'">
                <span>
                  <a-tag v-for="tag in record.tags" :key="tag"
                    :color="tag === 'IVIG抵抗' ? 'pink' : tag === '复发' ? 'red' : 'blue'">
                    {{ tag }}
                  </a-tag>
                </span>
              </template>
            </template>
          </a-table>
        </a-col>
      </a-row>
    </a-space>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref, watch } from "vue";
import { Table, Tag, Input, Row, Col, Space, Button, Dropdown, Menu, message } from "ant-design-vue";
import { usePagination } from 'vue-request'
import { computed } from "@vue/reactivity";
import { getGroups, getPatients, getTestsByPatientId, getExportFile } from "@/api/kawasaki";
import { SearchOutlined, DownloadOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const { Item } = Menu;

export default defineComponent({
  name: "ManagerView",
  components: {
    ARow: Row,
    ACol: Col,
    ATable: Table,
    ATag: Tag,
    AInput: Input,
    ASpace: Space,
    AButton: Button,
    ADropdown: Dropdown,
    AMenu: Menu,
    AMenuItem: Item,
    SearchOutlined,
    DownloadOutlined
  },

  setup() {
    const groupList = ref([]);
    onMounted(async () => {
      groupList.value = await getGroups();
    });
    const columns = computed(() => [
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
        responsive: ["md"],
      },
      {
        title: "分组",
        dataIndex: "group",
        key: "group",
        filters: groupList.value.map(group => ({ text: group.label, value: group.value })),
        responsive: ["md"],
      },
      {
        title: "标签",
        dataIndex: "tags",
        key: "tags",
        filters: [
          { text: "IVIG抵抗", value: "resistance" },
          { text: "复发", value: "relapse" },
        ],
        responsive: ["md"],
      }
    ])
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
          group: groupList.value.find(item => item.value === patient.group)?.label || "未确定",
          tags: tags,
        };
      });
    });

    const apiParams = ref({});

    const handleTableChange = (pagination, filters, sorter) => {
      const sortField = () => {
        if (sorter.order === "ascend") {
          return sorter.field;
        } else if (sorter.order === "descend") {
          return `-${sorter.field}`;
        } else {
          return null;
        }
      };

      const { group, tags } = filters;
      let tagsFilter = {};
      tags?.forEach(key => tagsFilter[key] = true);
      const searchField = apiParams.value.search || null;

      apiParams.value = {
        page: pagination?.current,
        ordering: sortField(),
        group__in: group?.toString(),
        search: searchField,
        ...tagsFilter,
      };
    };

    const onSearch = (e) => {
      apiParams.value.page = 1;
      apiParams.value.search = e.target.value;
    }

    const store = useStore();
    const router = useRouter();
    const gotoAdd = async (e) => {
      try {
        const data = await getPatients({ search: e.target.textContent });
        const patient = data.results[0];
        store.dispatch("setPatient", patient);
        const tests = await getTestsByPatientId(patient.id);
        store.dispatch("setTests", tests);
        router.push({ name: "add-tests" });
      } catch (error) {
        console.log(error);
      }
    }

    const downloadMsgKey = "download";

    const handleExport = (e) => {
      if (e.key === "1") {
        message.loading({
          content: "正在导出...",
          key: downloadMsgKey,
        });
        getExportFile().then(() => {
          message.success({
            content: "导出成功",
            key: downloadMsgKey,
          });
        }).catch(err => {
          message.error({
            content: "导出失败",
            key: downloadMsgKey,
          });
          console.log(err);
        });
      }
    }

    watch(() => apiParams, (params) => {
      run(params.value);
    }, {
      deep: true,
    });

    return {
      columns,
      dataSource,
      pagination,
      loading,
      handleTableChange,
      onSearch,
      gotoAdd,
      handleExport,
    };
  }
})
</script>
