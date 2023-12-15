<template>
  <div>
    <div class="button-container">
      <button @click="selectMarket('kospi')" style="border-radius: 25px;">
        코스피
      </button>
      <button @click="selectMarket('kosdaq')" style="border-radius: 25px;">
        코스닥
      </button>
      <button @click="selectMarket('kospi200')" style="border-radius: 25px;">
        코스피200
      </button>
      <div class="selected-market">
        선택된 종목: {{ selectedMarket }}
      </div>
    </div>
    <div v-if="selectedMarket">
      <button @click="updateData('D1')" style="border-radius: 13px;">
        1일
      </button>
      <button @click="updateData('D5')" style="border-radius: 13px;">
        5일
      </button>
      <button @click="updateData('M1')" style="border-radius: 13px;">
        1개월
      </button>
      <button @click="updateData('M6')" style="border-radius: 13px;">
        6개월
      </button>
      <button @click="updateData('YTD')" style="border-radius: 13px;">
        1년
      </button>
    </div>
  </div>
  <div>
    <apexcharts type="area" height="200" :options="state.chartOptions"
                :series="state.series[selectedMarket] || []"></apexcharts>
    <!--    <apexcharts type="area" height="450" :options="state.chartOptions" :series="state.series"></apexcharts>-->
  </div>

</template>


<script>

import VueApexCharts from 'vue3-apexcharts'
import axios from "axios";
import {ref, reactive} from 'vue'

export default {
  name: "VolumeAreaChart",
  components: {
    apexcharts: VueApexCharts,
  },
  setup() {
    const state = reactive({
      series: {
        kospi: [],
        kosdaq: [],
        kospi200: [],
      },
      chartOptions: {
        chart: {
          id: 'area-datetime',
          type: 'area',
          height: 350,
          zoom: {
            autoScaleYaxis: true
          }
        },
        dataLabels: {
          enabled: false
        },
        markers: {
          size: 0,
          style: 'hollow',
        },
        xaxis: {
          type: 'datetime',
          tickAmount: 6,
        },
        tooltip: {
          x: {
            format: 'dd MMM yyyy HH:mm'
          }
        },
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 100]
          },
          colors:['#FF0000']
        },
        stroke:{
          colors: ['#FF0000']
        },
        yaxis: {
          labels: {
            formatter: function (value) {
              return value.toFixed(2);
            }
          }
        }
      },
    });
    // const selection = ref(null);
    // const chart = ref(null);
    const selectedMarket = ref(null);


    const selectMarket = (market) => {
      if(selectedMarket.value !== market){
        state.series[market] = [];
      }
      selectedMarket.value = market;
    };

    const updateData = async (timeline) => {
      // state.series.length = 0;
      try {
        let url;
        if (selectedMarket.value === 'kospi') {
          url = `http://221.156.60.18:9199/kospi/kospi_${timeline}`;

        } else if (selectedMarket.value === 'kosdaq') {
          url = `http://221.156.60.18:9199/kosdaq/kosdaq_${timeline}`;

        } else if (selectedMarket.value === 'kospi200') {
          url = `http://221.156.60.18:9199/kospi200/kospi200_${timeline}`;
        }

        const response = await axios.get(url, {}, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        const AreaChartData = JSON.parse(response.data)
        console.log(AreaChartData.data[0])
        const processedData = [];

        if (AreaChartData.data) {
          console.log('API 응답 데이터 배열 길이: ', response.data.length);
          AreaChartData.data.forEach(data => {
            // console.log('timestamp:', data.timestamp);
            const timestamp = new Date(data.timestamp * 1000);
            const {volume} = data;
            // console(open, high, low, volume)

            processedData.push({
              x: timestamp,
              y: [volume]
            });
          });
        }
        if(!state.series[selectedMarket.value]){
          state.series[selectedMarket.value] = [];
        }
        state.series[selectedMarket.value] = [{name: selectedMarket.value, data: processedData}];
        // console.log('state.series[selectedMarket.value]:', state.series[selectedMarket.value]);
      } catch (error) {
        console.error(error);
      }
    };

    return {
      state,
      selectMarket,
      selectedMarket,
      updateData
    }
  }
}
</script>

<style scoped>
.button-container {
  display: flex;
  align-items: center;
}

.selected-market {
  font-size: 20px;
  margin-left: 10px;
}

button {
  margin: 5px;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
s
button:hover {
  background-color: #45a049;
}
</style>