<template>
  <ChartName :selectedStock="selectedStock"></ChartName>

  <div>
    <div class="row">
      <div class="col-md-6">
        <div class="candle-mystock shadow-lg">
          <button class="btn-candle shadow-sm" @click="fetchChartData('day')">일봉</button>
          <button class="btn-candle shadow-sm" @click="fetchChartData('week')">주봉</button>
          <button class="btn-candle shadow-sm" @click="fetchChartData('month')">월봉</button>
          <button type="button " class="btn-alarm shadow-sm" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
            알림설정
          </button>
          <i type="button" class="far fa-times-circle closed" @click="$emit('close')"></i>
          <apexcharts type="candlestick" height="400" :options="chartoptions.chartOptions"
                      :series="processedChartData"></apexcharts>
          <alarm-modal :selectedStock="selectedStock"></alarm-modal>
        </div>
      </div>

      <div class="col-md-6">
        <div class="candle-mystock shadow-lg">
          <ChartInformation :selectedStock="selectedStock"></ChartInformation>
        </div>
      </div>
    </div>
  </div>

</template>


<script>
import {computed, reactive, watch} from 'vue';
import {useStore} from 'vuex';
import VueApexCharts from 'vue3-apexcharts';
import ChartName from "@/views/components/ChartName.vue";
import ChartInformation from "@/views/components/ChartInformation.vue";
import AlarmModal from "@/views/components/AlarmModal.vue";


const intervalMap = {
  day: 'daily',
  week: 'week',
  month: 'month'
};


export default {
  name: "CandleStickChart",
  components: {
    AlarmModal,
    ChartInformation,
    ChartName,
    apexcharts: VueApexCharts,
  },
  props: {
    selectedStock: {
      type: Object
    }
  },
  setup(props) {
    const state = reactive({
      series: [],
    });

    const store = useStore();
    const selectedInterval = reactive({value: 'day'});

    const chartData = computed(() => {
      console.log("차트컴포넌트", props.selectedStock.initial)
      const stockType = props.selectedStock.market;
      const interval = selectedInterval.value;
      const intervalKey = intervalMap[interval];

      return store.getters[`StockPage/${intervalKey}${stockType.charAt(0).toUpperCase() + stockType.slice(1)}`];
    });
    const processedChartData = computed(() => {
      const series_list = []
      const processedData = chartData.value.stock_data.map(item => ({
        x: item.stck_bsop_date,
        y: [item.stck_oprc, item.stck_hgpr, item.stck_lwpr, item.stck_clpr]
      }));
      series_list.push({name: chartData.value._id, data: processedData.reverse()})
      return series_list
    });

    const chartoptions = {
      chartOptions: {
        zoom: {
          enabled: false,
          datetimeUTC: false
        },
        chart: {
          height: 400,
          type: 'candlestick',
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '85%',
            endingShape: 'rounded',
            dataLabels: {
              position: 'top', // top, center, bottom
            },
          }
        },
        dataLabels: {
          enabled: false,
        },
        colors: ['#F4D03F'],
        xaxis: {
          reversed: true,
          tickAmount: 9,
          position: 'bottom',
          axisBorder: {
            show: false
          },
          labels: {
            show: true
          },
          axisTicks: {
            show: false
          },
          tooltip: {
            enabled: false,
          },

          yaxis: {
            axisBorder: {
              show: false
            },
            axisTicks: {
              show: false,
            },
            labels: {
              show: true,
              formatter: function (val) {
                return val;
              }
            }
          }
        }
      }
    }
    const fetchChartData = (interval) => {
      console.log("이거는 뭐임???",interval)
      selectedInterval.value = interval;
      store.dispatch('StockPage/fetchStockChartData', {
        stck_shrn_iscd: props.selectedStock.id,
        interval: interval,
      });
    };
    watch(() => props.selectedStock, (newStock) => {
      if (newStock) {
        fetchChartData(selectedInterval.value);
      }
    }, {immediate: true});

    return {
      state,
      chartoptions,
      fetchChartData,
      processedChartData,
    };
  }
}
</script>

<style scoped>

/* 일,주,월 버튼 디자인 */
.btn-candle {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #0e61e0;
  border: none; /* 테두리 제거 */
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: 10px;
  font-weight: bold;

}

/* 알림설정 버튼 디자인 */
.btn-alarm {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  margin-left: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #03C41499;
  border: none;
  font-weight: bold;
}

/* 일,주,월 버튼 호버링  */
.btn-candle:hover {
  background-color: #003D88FF;
  opacity: 1;
}

/* 알림설정 버튼 호버링 */
.btn-alarm:hover {
  background-color: #003D88FF;
  opacity: 1;
}

/* X닫기 버튼 */
.closed {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
}

/* 캔들차트 및 버튼들 출력영역 */
.candle-mystock {
  background-color: #ffffff;
  border-radius: 15px;
  margin-bottom: 25px;
}

.candle-mystock {
  position: relative;
}
</style>
