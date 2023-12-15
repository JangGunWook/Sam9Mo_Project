<template>
<!--느리면 API새로 호출-->
  <div class="mb-4 card">
    <div class="p-3 card-body">
      <div class="d-flex">
        <div>
          <div class="numbers">
            <p class="mb-0 text-lg text-capitalize font-weight-bold">{{ selectedStocks.market}}</p>
            <h4 id="company" class="mb-0 font-weight-bolder">
              {{ selectedStocks.initial.COMPANY}}
              <span class="text-lg font-weight-bolder">{{formatNumber(selectedStocks.current_trade.PRDY_CTRT ? selectedStocks.current_trade.PRDY_CTRT : selectedStocks.initial.prdy_ctrt)}}%</span>
            </h4>

              <transition name="fade" mode="out-in">
                <h3 class="font-weight-bolder mb-0"
                   :key="selectedStocks.current_trade.STCK_PRPR"
                   :style="{ color: selectedStocks.current_trade.STCK_PRPR > selectedStocks.initial.stck_prpr ? 'red' : (selectedStocks.current_trade.STCK_PRPR < selectedStocks.initial.stck_prpr ? 'blue' : 'black') }">
                  {{ (selectedStocks.current_trade.STCK_PRPR > selectedStocks.initial.stck_prpr ? '▲ +' : (selectedStocks.current_trade.STCK_PRPR < selectedStocks.initial.stck_prpr ? '▼ -' : '')) + formatNumber(selectedStocks.current_trade.STCK_PRPR ? selectedStocks.current_trade.STCK_PRPR : selectedStocks.initial.stck_prpr) }}
                </h3>
              </transition>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex';
import { watch,reactive } from 'vue';
import {formatNumber} from "chart.js/helpers";
export default {
  name: "ChartName",
  methods: {formatNumber},

  props: {
    selectedStock: {
      type: Object
    }
  },

  setup(props) {
    const store = useStore();
    const selectedStocks = reactive(props.selectedStock);
    // console.log("확인",props.selectedStock)

    watch(() => [store.state.StockPage.myStocks, store.state.StockPage.allStocks], () => {
      const matchingStock = [...store.state.StockPage.myStocks, ...store.state.StockPage.allStocks].find(
          (stock) => props.selectedStock.id === stock.initial.stck_shrn_iscd
      );
      if (matchingStock) {
        Object.assign(selectedStocks, matchingStock); // reactive 객체를 직접 변경합니다.
      }
    });
    return {
      selectedStocks
    };
  }
};
</script>

<style scoped>

/* 종목가 변동 시, 출력값에 애니메이션 효과 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>