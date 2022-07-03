<template>
  <div class="dashboard">
    <a-space direction="vertical" :size="16" style="width: 100%">
      <a-row :gutter="16">
        <a-col :span="8">
          <a-card :loading="sampleCountsLoading">
            样本量
            <a-row>
              <a-col v-for="(value, key) in sampleCounts" :key="key" :span="24 / groups.length">
                <a-statistic :title="key" :value="value" suffix="人"></a-statistic>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
        <a-col :span="8">
          <a-card :loading="genderRateLoading">
            性别比例 (男:女)
            <a-row>
              <a-col v-for="(item, key) in genderCounts" :key="key" :span="24 / groups.length">
                <a-statistic :title="key" :value="(item.M / item.F).toFixed(2)"></a-statistic>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
        <a-col :span="8">
          <a-card :loading="ageLoading">
            平均年龄
            <a-row>
              <a-col v-for="(value, key) in ageAverage" :key="key" :span="24 / groups.length">
                <a-statistic :title="key" :value="(value / 12).toFixed(2)" suffix="岁"></a-statistic>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
      </a-row>
      <a-row>
        <a-col :span="24">
          <a-card title="样本-时间分布" :loading="linePlotLoading">
            <div id="count_line"></div>
          </a-card>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col v-for="g in groups" :key="g" :span="24 / groups.length">
          <a-card :title="`年龄分布(${g})`">
            <div :id="`age_hist_${g.replaceAll(' ', '_')}`"></div>
          </a-card>
        </a-col>
      </a-row>
    </a-space>
  </div>
</template>

<script>
import {
  defineComponent,
  onMounted,
  reactive,
  toRefs,
  nextTick
} from "vue";
import { Line, Histogram } from "@antv/g2plot";
import { Row, Col, Card, Statistic, Space } from "ant-design-vue";
import { getSummary, getCountByMonth, getAgeByGroup } from "@/api/kawasaki";

export default defineComponent({
  name: "DashboardView",
  components: {
    ARow: Row,
    ACol: Col,
    ACard: Card,
    AStatistic: Statistic,
    ASpace: Space
  },
  setup() {
    const state = reactive({
      sampleCounts: {},
      sampleCountsLoading: true,
      groups: [],
      genderCounts: {},
      genderRateLoading: true,
      ageAverage: {},
      ageLoading: true,
      linePlotLoading: true,
      histPlotLoading: true,
    });

    const getData = async () => {
      const data = await getSummary();
      state.sampleCounts = data.sample_counts;
      state.sampleCountsLoading = false;
      state.groups = data.groups;
      state.genderCounts = data.gender_counts;
      state.genderRateLoading = false;
      state.ageAverage = data.age_mean;
      state.ageLoading = false;
    };

    const setLinePlot = async () => {
      const data = await getCountByMonth();
      state.linePlotLoading = false;
      if (data !== null && data.length !== 0) {
        nextTick(() => {
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

    const setHistPlot = async () => {
      const data = await getAgeByGroup();
      state.histPlotLoading = false;
      for (const [key, value] of Object.entries(data)) {
        if (value !== null && value.length !== 0) {
          nextTick(() => {
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

    return {
      ...toRefs(state),
    };
  },
});
</script>

<style scoped>
.dashboard {
  padding: 24px;
  margin: 20px 40px;
}
</style>
