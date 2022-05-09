<template>
    <a-card>
          {{ title }}
          <a-row>
            <a-col
              v-for="(value, key) in dictObject"
              :key="key"
              :span="24 / dictObject.length"
            >
              <a-statistic
                :title="key"
                :value="value"
                :suffix="suffix"
              ></a-statistic>
            </a-col>
          </a-row>
        </a-card>
</template>

<script>
import { defineComponent } from "@vue/runtime-core";
import { Card, Row, Col, Statistic } from "ant-design-vue";

export default defineComponent({
    name: "ObjectCard",
    components: {
        ACard: Card,
        ARow: Row,
        ACol: Col,
        AStatistic: Statistic,
    },
    props: {
        dictObject: {
            type: Object,
            default: () => {return {"Disease":25, "Control":75}},
        },
        title: {
            type: String,
            default: "Object to card",
        },
        suffix: {
            type: String,
            default: "",
        },
    },
});
</script>
