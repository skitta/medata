<template>
  <div class="nav-view-container">
    <a-space direction="vertical" style="width: 100%">
      <a-alert
        v-if="alertMessage"
        :message="alertMessage"
        :type="alertType"
        show-icon
        closable
        @close="clearAlert"
        style="margin-bottom: 16px"
      />
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
            <a-button type="primary" :loading="exportLoading">
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

<script setup lang="ts">
import { onMounted, ref, watch, computed } from "vue";
import { Table as ATable, Tag as ATag, Input as AInput, Row as ARow, Col as ACol, Space as ASpace, Button as AButton, Dropdown as ADropdown, Menu as AMenu, MenuItem as AMenuItem, Alert as AAlert } from "ant-design-vue";
import { usePagination } from 'vue-request'
import { getGroups, getPatients, getTestsByPatientId, getExportFile } from "@/api/kawasaki";
import { SearchOutlined, DownloadOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";
import { useMainStore } from "@/stores";
import { SelectOption } from "@/types/api";

const groupList = ref<SelectOption[]>([]);
const alertMessage = ref("");
const alertType = ref<"error" | "warning" | "success" | "info">("info");
const exportLoading = ref(false);

const clearAlert = () => {
  alertMessage.value = "";
};

const showAlert = (message: string, type: "error" | "warning" | "success" | "info" = "info") => {
  alertMessage.value = message;
  alertType.value = type;
};

onMounted(async () => {
  groupList.value = await getGroups();
});

const columns = computed((): any[] => [
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
    responsive: ["md"] as any,
  },
  {
    title: "分组",
    dataIndex: "group",
    key: "group",
    filters: groupList.value.map(group => ({ text: group.label, value: group.value })),
    responsive: ["md"] as any,
  },
  {
    title: "标签",
    dataIndex: "tags",
    key: "tags",
    filters: [
      { text: "IVIG抵抗", value: "resistance" },
      { text: "复发", value: "relapse" },
    ],
    responsive: ["md"] as any,
  }
]);

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
    total: data.value?.count || 0,
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
  }) || [];
});

const apiParams = ref<any>({});

const handleTableChange = (pagination: any, filters: any, sorter: any) => {
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
  const tagsFilter: { [key: string]: boolean } = {};
  tags?.forEach((key: string) => tagsFilter[key] = true);
  const searchField = apiParams.value.search || null;

  apiParams.value = {
    page: pagination?.current,
    ordering: sortField(),
    group__in: group?.toString(),
    search: searchField,
    ...tagsFilter,
  };
};

const onSearch = (e: any) => {
  apiParams.value.page = 1;
  apiParams.value.search = e.target.value;
}

const store = useMainStore();
const router = useRouter();
const gotoAdd = async (e: any) => {
  try {
    const data = await getPatients({ search: e.target.textContent });
    const patient = data.results[0];
    if (patient && patient.id) {
      store.setPatient(patient);
      const tests = await getTestsByPatientId(patient.id);
      store.setTests(tests);
      router.push({ name: "add-tests" });
    }
  } catch (error) {
    console.log(error);
  }
}

const handleExport = (e: any) => {
  if (e.key === "1") {
    exportLoading.value = true;
    clearAlert(); // 清除之前的提示
    
    getExportFile().then(() => {
      exportLoading.value = false;
      showAlert("导出成功！文件已开始下载", "success");
    }).catch(err => {
      exportLoading.value = false;
      console.error("导出失败", err);
      showAlert("导出失败，请重试", "error");
    });
  }
}

watch(() => apiParams, (params) => {
  run(params.value);
}, {
  deep: true,
});
</script>
