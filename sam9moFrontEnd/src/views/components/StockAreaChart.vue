<template>
  <div>
    <div>
      <h5 class="Area-text bold-text">{{ `${uppercaseMarket}지수` }}</h5>
      <apexcharts type="area" height="280" :options="state.chartOptions"
                  :series="state.series[selectedMarket] || []"></apexcharts>
    </div>
    <div>
      <apexcharts type="bar" height="220" :options="state.volumeChartOption"
                  :series="state.volumeChartseries[selectedMarket] || []"></apexcharts>
    </div>
  </div>

  <div>
    <!-- 시장 선택 버튼 -->
    <div class="button-container">
      <button v-for="market in markets"
              :key="market.value"
              @click="selectMarket(market.value)"
              :class="['button', 'button-market','shadow-sm', { 'button-selected': selectedMarket === market.value }]">
        {{ market.text }}
      </button>
    </div>

    <!-- 타임라인 선택 버튼 -->
    <div class="button-container">
      <button v-for="timeline in timelines"
              :key="timeline.value"
              @click="updateDataAndTimeline(timeline.value)"
              :class="['button', 'button-timeline','shadow-sm', { 'button-selected': selectedTimeline === timeline.value }]"
              style="font-size: 15px">
        {{ timeline.text }}
      </button>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
import axios from "axios";
import {ref, reactive, onMounted, computed} from 'vue'

export default {
  name: "StockAreaChart",
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

        stroke: {
          colors: ['rgb(255,21,0)'],
          width: 3,
        },
        colors: ['rgb(255,0,0)'],

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
              return `${year}.${month}.${day}`;

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
              const hours = date.getHours().toString().padStart(2, '0');
              const minutes = date.getMinutes().toString().padStart(2, '0');

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
        kospi: [],
        kosdaq: [],
        kospi200: [],
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
        colors: ['rgba(4,190,12,0.57)'],
        plotOptions: {
          bar: {
            columnWidth: '90%', // 막대의 두께를 조절
            dataLabels: {
              position: 'top',
            },
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
              const year = date.getFullYear();
              const month = date.getMonth() + 1;
              const day = date.getDate();

              return `${year}.${month}.${day}`;
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
            crosshairs: {
              fill: {
                type: 'gradient',
                gradient: {
                  colorFrom: '#D8E3F0',
                  colorTo: '#BED1E6',
                  stops: [0, 100],
                  opacityFrom: 0.4,
                  opacityTo: 0.5,
                }
              }
            },
            yaxis: {
              axisBorder: {
                show: false
              },
              axisTicks: {
                show: false,
              },
              labels: {
                show: false,
                formatter: function (value) {
                  return value.toFixed(2);
                }
              }
            }
          },
        }
      }
    });
    const markets = [
      {value: 'kospi', text: 'KOSPI'},
      {value: 'kosdaq', text: 'KOSDAQ'},
      {value: 'kospi200', text: 'KOSPI200'},
    ];

    const timelines = [
      {value: 'D1', text: '1일'},
      {value: 'D5', text: '5일'},
      {value: 'M1', text: '1개월'},
      {value: 'M6', text: '6개월'},
      {value: 'YTD', text: '1년'},
    ];

    const selectedTimeline = ref('D1');

    const updateDataAndTimeline = async (timeline) => {
      selectedTimeline.value = timeline;
      await fetchData(timeline, state.series);
      await fetchVolumeData(timeline);
    };

    // dashboard 페이지 구동 시, 출력 되는 기본값 차트
    onMounted(() => {
      selectMarket(selectedMarket.value);
      updateDataAndTimeline(selectedTimeline.value);
      // selectMarket('kospi');
      // updateDataAndTimeline('D1');
    });

    const selectedMarket = ref('kospi');

    const uppercaseMarket = computed(() => {
      return selectedMarket.value.toUpperCase();
    });

    const selectMarket = async (market) => {
      if (selectedMarket.value !== market) {
        state.series[market] = [];
        state.volumeChartseries[market] = [];
      }
      selectedMarket.value = market;
      selectedTimeline.value = 'D1'
      await updateDataAndTimeline(selectedTimeline.value);
    };

    // Area 차트 API 호출
    const fetchData = async (timeline, series) => {
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

      // *** JSON.parse 기억!!! ***
      const AreaChartData = response.data;
      const processedData = [];

      if (AreaChartData.data) {
        AreaChartData.data.forEach(data => {
          const timestamp = new Date(data.timestamp * 1000);
          const {open, low, high, close} = data;

          processedData.push({
            x: timestamp,
            y: [open, low, high, close]
          });
        });
      }

      if (!series[selectedMarket.value]) {
        series[selectedMarket.value] = [];
      }

      series[selectedMarket.value] = [{name: selectedMarket.value.toUpperCase(), data: processedData}];
    };

    // Volume bar 차트 API 호출
    const fetchVolumeData = async (timeline) => {
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

      const AreaChartData = response.data;
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

      if (!state.volumeChartseries[selectedMarket.value]) {
        state.volumeChartseries[selectedMarket.value] = [];
      }
      state.volumeChartseries[selectedMarket.value] = [{name: selectedMarket.value.toUpperCase(), data: processedData}];
    };

    const updateData = async (timeline) => {
      await fetchData(timeline, state.series);
    };

    const updateVolumeChartData = async (timeline) => {
      await fetchVolumeData(timeline);
    };

    return {
      markets,
      timelines,
      updateVolumeChartData,
      state,
      selectMarket,
      selectedMarket,
      updateData,
      updateDataAndTimeline,
      selectedTimeline,
      uppercaseMarket
    };
  }
}
</script>

<style scoped>

/* 공통 버튼 스타일 */
.button {
  margin: 5px;
  padding-inline: 10px;
  font-size: 20px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  opacity: 1;
  color: #ffffff;
  border: none; /* 테두리 제거 */
}

/* 시장 버튼 초기 색상 */
.button-market {
  background-color: #0e61e0;
}

/* 시장 버튼 호버링 색상 */
.button-market:not(.button-selected):hover {
  background-color: #003D88FF;
  opacity: 1;
}

/* 타임라인 버튼 초기 색상 */
.button-timeline {
  background-color: #0e61e0;
}

/* 타임라인 버튼 호버링 시, 색상 */
.button-timeline:not(.button-selected):hover {
  background-color: #003D88FF;
  opacity: 1;
}

/* 시장,타임라인 버튼 위치 */
.button-container {
  display: flex;
  justify-content: right;
  flex-wrap: wrap;
}

/*** 비활성화 되어있는데 구동이 됨! 삭제X ***/
.button-selected,
.button-market.button-selected:hover,
.button-timeline.button-selected:hover {
  background-color: #003D88FF;
}

/* 시장 선택 텍스트 */
.bold-text {
  font-weight: bold;
}

/* 시장 선택 텍스트 위치 */
.Area-text {
  margin-top: 10px;
}

</style>
