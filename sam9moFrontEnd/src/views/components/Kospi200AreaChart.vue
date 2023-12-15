<template>
  <div>
    <!-- 선택된 마켓 버튼에 selected 클래스 추가 -->
    <div class="button-container">
      <button @click="selectMarket('kospi200')" style="border-radius: 25px;">
        KOSPI200
      </button>

    </div>
    <!-- 선택된 타임라인 버튼에 selected 클래스 추가 -->
    <div v-if="selectedMarket === 'kospi200'">

      <button @click="updateDataAndTimeline('D1')" style="border-radius: 13px;"
              :class="{ selected: selectedTimeline === 'D1' }">
        1일
      </button>
      <button @click="updateDataAndTimeline('D5')" style="border-radius: 13px;"
              :class="{ selected: selectedTimeline === 'D5' }">
        5일
      </button>
      <button @click="updateDataAndTimeline('M1')" style="border-radius: 13px;"
              :class="{ selected: selectedTimeline === 'M1' }">
        1개월
      </button>
      <button @click="updateDataAndTimeline('M6')" style="border-radius: 13px;"
              :class="{ selected: selectedTimeline === 'M6' }">
        6개월
      </button>
      <button @click="updateDataAndTimeline('YTD')" style="border-radius: 13px;"
              :class="{ selected: selectedTimeline === 'YTD' }">
        1년
      </button>
    </div>
  </div>
  <div>
    <apexcharts type="area" height="120" :options="state.chartOptions"
                :series="state.series[selectedMarket] || []"></apexcharts>
  </div>
  <div>
    <apexcharts type="bar" height="120" :options="state.volumeChartOption"
                :series="state.volumeChartseries[selectedMarket] || []"></apexcharts>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import axios from "axios";
import {ref, reactive, onMounted} from 'vue'

export default {
  name: "Kospi200AreaChart",
  components: {
    apexcharts: VueApexCharts,
  },

  setup() {
    const state = reactive({
      series: {
        kospi200: []
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
          labels: {
            formatter: function (value) {
              const date = new Date(value);

              // 년,월,일
              const year = date.getFullYear();
              const month = date.getMonth() + 1;
              const day = date.getDate();

              // 한글 형식 날짜 문자열 반환
              return `${year}년 ${month}월 ${day}일`;

            }
          }
        },
        tooltip: {
          x: {
            formatter: function (value) {
              const date = new Date(value);

              // 년,월,일
              const year = date.getFullYear();
              const month = date.getMonth() + 1;
              const day = date.getDate();
              const hours = date.getHours();
              const minutes = date.getMinutes();

              return `${year}년 ${month}월 ${day}일 ${hours}시 ${minutes}분`;
            }

          },

        },
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 100]
          }
        },
        yaxis: {
          labels: {
            formatter: function (value) {
              return value.toFixed(2);
            }
          }
        }
      },
      volumeChartseries: {
        kospi200: []
      },
      volumeChartOption: {
        chart: {
          id: 'area-datetime',
          type: 'bar',
          height: 350,
          zoom: {
            autoScaleYaxis: true
          }
        },
        plotOptions: {
          bar: {
            columnWidth: '75%', // 막대의 두께를 조절
          },
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
          labels: {
            formatter: function (value) {

              const date = new Date(value);

              const year = date.getFullYear();
              const month = date.getMonth() + 1;
              const day = date.getDate();

              return `${year}년 ${month}월 ${day}일`;
            },
            tooltip: {
              x: {
                formatter: function (value) {

                  const date = new Date(value);

                  const year = date.getFullYear();
                  const month = date.getMonth() + 1;
                  const day = date.getDate();
                  const hours = date.getHours();
                  const minutes = date.getMinutes();

                  return `${year}년 ${month}월 ${day}일 ${hours}시 ${minutes}분`;
                }
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
              colors: ['#ff0000']
            },
            stroke: {
              colors: ['#ff0000']
            },
            yaxis: {
              labels: {
                formatter: function (value) {
                  return value.toFixed(2);
                }
              }
            }
          },
        }
      }
    });

    const selectedTimeline = ref(null);

    const updateDataAndTimeline = async (timeline) => {
      selectedTimeline.value = timeline;
      await fetchData(timeline, state.series);
      await fetchVolumeData(timeline);
    };

    // dashboard 페이지 구동 시, 출력 되는 기본값 차트
    onMounted(() => {
      selectMarket('kospi200');
      updateDataAndTimeline('D1');
    });

    const selectedMarket = ref(null);

    const selectMarket = (market) => {
      if (selectedMarket.value !== market) {
        state.series[market] = [];
        state.volumeChartseries[market] = [];
      }
      selectedMarket.value = market;
    };

    const fetchData = async (timeline, series) => {
      const url = `http://221.156.60.18:9199/kospi200/kospi200_${timeline}`;

      const response = await axios.get(url, {}, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      // *** JSON.parse 기억!!! ***
      const AreaChartData = JSON.parse(response.data)
      const processedData = [];

      if (AreaChartData.data) {
        AreaChartData.data.forEach(data => {
          const timestamp = new Date(data.timestamp * 1000);
          const {open, high, low, close} = data;

          processedData.push({
            x: timestamp,
            y: [open, high, low, close]
          });
        });
      }

      if (!series['kospi200']) {
        series['kospi200'] = [];
      }

      series['kospi200'] = [{name: 'kospi200', data: processedData}];
    };
    const fetchVolumeData = async (timeline) => {
      const url = `http://221.156.60.18:9199/kospi200/kospi200_${timeline}`;
      const response = await axios.get(url, {}, {
        headers: {
          'Content-Type': 'application/json'
        }
      });


      const AreaChartData = JSON.parse(response.data)
      const processedData = [];

      if (AreaChartData.data) {
        AreaChartData.data.forEach(data => {
          const timestamp = new Date(data.timestamp * 1000);
          const {volume} = data;

          processedData.push({
            x: timestamp,
            y: [volume]
          });
        });
      }

      if (!state.volumeChartseries['kospi200']) {
        state.volumeChartseries['kospi200'] = [];
      }

      state.volumeChartseries['kospi200'] = [{name: 'kospi200', data: processedData}];
    };

    const updateData = async (timeline) => {
      await fetchData(timeline, state.series);
    };

    const updateVolumeChartData = async (timeline) => {
      await fetchVolumeData(timeline);
    };

    return {
      updateVolumeChartData,
      state,
      selectMarket,
      selectedMarket,
      updateData,
      updateDataAndTimeline,
      selectedTimeline
    };
  }
}
</script>

<style scoped>
.button-container {
  display: flex;
  align-items: center;
}

.selected-market {
  font-size: 15px;
  margin-left: 10px;
}

button {
  margin: 5px;
  padding: 5px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 15px;
}

button:hover {
  background-color: #45a049;
}

/* 선택된 버튼 스타일 */
button.selected {
  background-color: #878c93;
}
</style>
