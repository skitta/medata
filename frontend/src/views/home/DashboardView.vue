<template>
  <div class="nav-view-container">
    <a-space direction="vertical" :size="16" style="width: 100%">
      <!-- 统计信息 -->
      <a-row :gutter="16">
        <a-col :xs="24" :md="12" :lg="8">
          <a-card :loading="sampleCountsLoading">
            样本量
            <a-row>
              <a-col v-for="(value, key) in summary.sample_counts" :key="key" :span="summary.groups && summary.groups.length ? 24 / summary.groups.length : 24">
                <a-statistic :title="key" :value="value" suffix="人"></a-statistic>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="12" :lg="8">
          <a-card :loading="genderRateLoading">
            性别比例 (男:女)
            <a-row>
              <a-col v-for="(item, key) in summary.gender_counts" :key="key" :span="summary.groups && summary.groups.length ? 24 / summary.groups.length : 24">
                <a-statistic :title="key" :value="(item.M / item.F).toFixed(2)"></a-statistic>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="12" :lg="8">
          <a-card :loading="ageLoading">
            平均年龄
            <a-row>
              <a-col v-for="(value, key) in summary.age_mean" :key="key" :span="summary.groups && summary.groups.length ? 24 / summary.groups.length : 24">
                <a-statistic :title="key" :value="(value / 12).toFixed(2)" suffix="岁"></a-statistic>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
      </a-row>
      <!-- 平滑的折线图 -->
      <a-row>
        <a-col :span="24">
          <a-card title="样本-时间分布" :loading="linePlotLoading">
            <div id="count_line"></div>
          </a-card>
        </a-col>
      </a-row>
      <!-- 柱状图 -->
      <a-row :gutter="16">
        <a-col v-for="g in summary.groups" :key="g" :xs="24" :lg="summary.groups && summary.groups.length ? 24 / summary.groups.length : 24">
          <a-card :title="`年龄分布(${g})`">
            <div :id="`age_hist_${g.replaceAll(' ', '_')}`"></div>
          </a-card>
        </a-col>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="ts">
import {
  onMounted,
  nextTick,
  ref,
} from "vue";
import { Row as ARow, Col as ACol, Card as ACard, Statistic as AStatistic, Space as ASpace } from "ant-design-vue";
import { getSummary, getCountByMonth, getAgeByGroup } from "@/api/kawasaki";
import type { Summary, MonthlyCount, AgeDataByGroup } from "@/types/api";

const summary = ref<Summary>({
  sample_counts: {},
  groups: [],
  gender_counts: {},
  age_mean: {},
});
const sampleCountsLoading = ref<boolean>(true);
const genderRateLoading = ref<boolean>(true);
const ageLoading = ref<boolean>(true);
const linePlotLoading = ref<boolean>(true);
const histPlotLoading = ref<boolean>(true);

const getData = async (): Promise<void> => {
  summary.value = await getSummary();
  sampleCountsLoading.value = false;
  genderRateLoading.value = false;
  ageLoading.value = false;
};

const setLinePlot = async (): Promise<void> => {
  const data: MonthlyCount[] = await getCountByMonth();
  linePlotLoading.value = false;
  if (data !== null && data.length !== 0) {
    nextTick(async () => {
      // 动态导入图表库
      const { Line } = await import("@antv/g2plot");
      const line = new Line("count_line", {
        data: data,
        xField: "date",
        yField: "count",
        smooth: true,
        meta: {
          date: {
            alias: "日期",
          },
          count: {
            alias: "样本量",
          },
        },
      });
      line.render();
    })
  }
};

const setHistPlot = async (): Promise<void> => {
  const data: AgeDataByGroup = await getAgeByGroup();
  histPlotLoading.value = false;
  for (const [key, value] of Object.entries(data)) {
    if (value !== null && value.length !== 0) {
      nextTick(async () => {
        // 动态导入图表库
        const { Histogram } = await import("@antv/g2plot");
        const hist_id = `age_hist_${key.replaceAll(" ", "_")}`;
        const hist = new Histogram(hist_id, {
          data: value,
          binField: "value",
          binWidth: 1,
          tooltip: {
            showMarkers: false,
            position: "top",
          },
          interactions: [
            {
              type: "element-highlight",
            },
          ],
          meta: {
            range: {
              min: 0,
              tickInterval: 1,
              alias: "年龄段",
            },
            count: {
              max: 10,
              tickInterval: 2,
              nice: true,
              alias: "样本量",
            },
          },
        });
        hist.render();
      })
    }
  }
};

onMounted(async () => {
  await getData();
  setLinePlot();
  setHistPlot();
});
</script>

<style>
.nav-view-container {
  padding: 24px;
  margin: 20px 40px;
}

@media screen and (max-width: 768px) {
  .nav-view-container {
    padding: 0;
    margin: 20px 10px;
  }
}
</style>
