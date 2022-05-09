<template>
  <div>
    <a-row :gutter="16">
      <a-col :span="8">
        <a-card>
          样本量
          <a-row>
            <a-col
              v-for="(value, key) in sampleCounts"
              :key="key"
              :span="24 / groups.length"
            >
              <a-statistic
                :title="key"
                :value="value"
                suffix="人"
              ></a-statistic>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card>
          性别比例 (男:女)
          <a-row>
            <a-col
              v-for="(item, key) in genderCounts"
              :key="key"
              :span="24 / groups.length"
            >
              <a-statistic
                :title="key"
                :value="(item.M / item.F).toFixed(2)"
              ></a-statistic>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card>
          平均年龄
          <a-row>
            <a-col
              v-for="(value, key) in ageAverage"
              :key="key"
              :span="24 / groups.length"
            >
              <a-statistic
                :title="key"
                :value="(value / 12).toFixed(2)"
                suffix="岁"
              ></a-statistic>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>
    <div class="plot">
      <a-card title="样本-时间分布">
        <div id="count_line"></div>
      </a-card>
    </div>
    <div class="plot">
      <a-card title="年龄分布">
        <a-row>
          <a-col v-for="g in groups" :key="g" :span="24 / groups.length">
            <div class="plot-title">{{ g }}</div>
            <div
              :id="`age_hist_${g.replaceAll(' ', '_')}`"
              class="plot-content"
            ></div>
          </a-col>
        </a-row>
      </a-card>
    </div>
  </div>
</template>

<script>
import {
  defineComponent,
  getCurrentInstance,
  onMounted,
  reactive,
  toRefs,
} from "vue";
import { Line, Histogram } from "@antv/g2plot";
import { Row, Col, Card, Statistic } from "ant-design-vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "DashboardView",
  components: {
    ARow: Row,
    ACol: Col,
    ACard: Card,
    AStatistic: Statistic,
  },
  setup() {
    const currentInstance = getCurrentInstance();
    const { $http } = currentInstance.appContext.config.globalProperties;
    const store = useStore();
    const headers = {
      Authorization: `Token ${store.getters.getToken}`,
    }

    const state = reactive({
      sampleCounts: {},
      groups: [],
      genderCounts: {},
      ageAverage: {},
    });

    const getData = async () => {
      const res = await $http.get("/kawasaki/summary/", { headers });
      const { data } = res;
      state.sampleCounts = data.sample_counts;
      state.groups = data.groups;
      state.genderCounts = data.gender_counts;
      state.ageAverage = data.age_mean;
    };

    const setLinePlot = async () => {
      const res = await $http.get("/kawasaki/count-by-month/", { headers });
      const { data } = res;
      if (data != null && data.length != 0) {
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
      }
    };

    const setHistPlot = async () => {
      const res = await $http.get("/kawasaki/age-by-group/", { headers });
      const { data } = res;
      for (const [key, value] of Object.entries(data)) {
        if (value != null && value.length != 0) {
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
.plot {
  margin-top: 20px;
}

.plot-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  widows: 100%;
  text-align: center;
}

.plot-content {
  padding: 20px;
}
</style>
