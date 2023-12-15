<template>
  <div id="ngramchart"></div>
</template>

<script>
import axios from "axios";
import {onMounted} from "vue";
import * as am5 from "@amcharts/amcharts5";
import * as am5hierarchy from "@amcharts/amcharts5/hierarchy";

export default {
  name: "NgramChart",
  setup() {
    onMounted(() => {
      const fetchData = async () => {
        try {
          const response = await axios.get('http://221.156.60.18:8092/keyword/bubble?date=202312&stock_limit=6&keyword_limit=7',{},{
            headers: {
              'Content-Type': 'application/json'
            }
          });
          const inputData = {
            value : 0,
            children : response.data.bubble_chart_data_list
          }

          await am5.ready(function () {
            const root = am5.Root.new("ngramchart");


            const container = root.container.children.push(am5.Container.new(root, {
                width: am5.percent(100),
                height: am5.percent(100),
                layouts: root.verticalLayout
            }));

            const series = container.children.push(am5hierarchy.ForceDirected.new(root, {
              singleBranchOnly: false,
              downDepth: 2,
              topDepth: 1,
              initialDepth: 1,
              valueField: "value",
              categoryField: "name",
              childDataField: "children",
              idField: "name",
              linkWithField: "linkWith",
              manyBodyStrength: -6,
              centerStrength: 1,
              minRadius: 29,
              maxRadius: am5.percent(6),
              nodePadding: 8
            }));


            series.get("colors").setAll({step: 2});
            series.links.template.set("strength", 0.5);
            series.data.setAll([inputData]);
            series.set("selectedDataItem", series.dataItems[0]);
            series.appear(1000, 100);
          });
        } catch (error) {
          console.error('An error occurred:', error);
        }
      };

      fetchData();
    });
  }
}
</script>

<style scoped>
#ngramchart {
  width: 100%;
  max-width: 100%;
  height: 610px;
}
</style>
