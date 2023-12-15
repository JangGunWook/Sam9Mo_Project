<template>
  <div class="card mb-4">
    <div class="card-header pb-0"
         style="border-top-left-radius: 15px; border-top-right-radius: 15px; background-color: #01275b;">
      <h5 class="my-text">관심종목</h5>
    </div>
    <div class="card-body px-0 pt-0 pb-0">
      <div class="table-responsive p-0">
        <table class="table align-items-center justify-content-center mb-0">
          <thead>
          <tr class="fa-sizeup">
            <th class="text-center font-weight-bolder">종목명</th>
            <th class="text-center font-weight-bolder">현재가</th>
            <th class="text-center font-weight-bolder">전일대비율</th>
            <th class="text-center font-weight-bolder">여론</th>
            <th class="text-center font-weight-bolder">시가총액(백만)</th>
            <th class="text-center font-weight-bolder">누적거래량</th>
            <th class="text-center font-weight-bolder">관심종목 해제</th>
          </tr>
          </thead>

          <tbody>
          <tr v-for="stock in myStocks" :key="stock.id" class="my-list" @click="onStockClick(stock)">
            <td class="text-center">
              <div class="d-flex px-2 py-1 justify-content-center">
                <h6 class="mb-0 text-lg">{{ stock.initial.COMPANY }}</h6>
              </div>
            </td>
            <td class="text-center">
              <transition name="fade" mode="out-in">
                <p class="text-lg font-weight-bolder mb-0"
                   :key="stock.current_trade.STCK_PRPR"
                   :style="{ color: stock.current_trade.STCK_PRPR > stock.initial.stck_prpr ? 'red' : (stock.current_trade.STCK_PRPR < stock.initial.stck_prpr ? 'blue' : 'black') }">
                  {{ (stock.current_trade.STCK_PRPR > stock.initial.stck_prpr ? '▲ +' : (stock.current_trade.STCK_PRPR < stock.initial.stck_prpr ? '▼ -' : '')) + formatNumber(stock.current_trade.STCK_PRPR ? stock.current_trade.STCK_PRPR : stock.initial.stck_prpr) }}
                </p>
              </transition>
            </td>
            <td class="align-middle text-center text-sm"
                :style="{ color: stock.current_trade.PRDY_CTRT > 0 ? 'red' : 'blue' }">
              <p class="text-lg font-weight-bolder mb-0 ">{{formatNumber(stock.current_trade.PRDY_CTRT ? stock.current_trade.PRDY_CTRT : stock.initial.prdy_ctrt)}}%</p>
            </td>
            <td class="align-middle text-center">
              <p class="text-secondary text-lg font-weight-bolder">{{ getMaxSentiment(sentiments[stock.initial.COMPANY])}}</p>
            </td>
            <td class="align-middle text-center">
              <span class="text-secondary text-lg font-weight-bolder">{{ formatNumber(stock.initial.hts_avls) }}</span>
            </td>
            <td class="align-middle text-center">
    <span class="text-secondary text-lg font-weight-bolder">{{
        formatNumber(stock.current_trade.ACML_VOL ? stock.current_trade.ACML_VOL : stock.initial.acml_vol)
      }}</span>
            </td>
            <td class="px-6 py-4 text-center text-gray-500 border-b">
              <i @click.stop="removeFromMyStocks(stock)" class="fa fa-minus-circle" style="font-size: 25px"
                 aria-hidden="true"></i>
            </td>
          </tr>

          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import {useStore} from "vuex";
import {computed} from "vue";
import axios from "axios";
import {formatNumber} from "chart.js/helpers";


export default {
  name: "MyStock",
  props: {
    sentiments: Object
  },
  methods: {formatNumber},

  setup(_, {emit}) {
    const store = useStore();
    const myStocks = computed(() => store.state.StockPage.myStocks);

    // 여론에서 가장 높은값 반환
    function getMaxSentiment(sentiment) {
      if (!sentiment) return "중립";

      let maxKey = null;
      let maxVal = -Infinity;

      for (let key in sentiment) {
        if (sentiment[key] > maxVal) {
          maxKey = key;
          maxVal = sentiment[key];
        }
      }
      switch (maxKey) {
        case "positive":
          return "긍정";
        case "negative":
          return "부정";
        default:
          return "중립";
      }
    }

    //session 객체 선언
    const sessionStorage = window.sessionStorage;
    const removeFromMyStocks = async (payload) => {
      console.log("mystock확인", payload.initial.stck_shrn_iscd)
      const favoriteStockBody = {
        "account": JSON.parse(sessionStorage.getItem("token")).account,// 추후 계정 바꿔야함 세션에서 가져오는 아이디로,
        "favorite_stock": payload.initial.stck_shrn_iscd
      }
      const url = "http://221.156.60.18:8096/favorite_stock/remove";
      const response = await axios.post(url, favoriteStockBody).catch(() => null)
      if (!response) return null

      const result = response.data

      sessionStorage.setItem("favorite_stock", JSON.stringify(result))
      const data = sessionStorage.getItem("favorite_stock")
      console.log("favorite_stock", JSON.parse(data))

      store.dispatch('StockPage/removeFromMyStocks', payload);
    };

    const fetchStockChartData = (payload) => {
      store.dispatch('StockPage/fetchStockChartData', payload);
    };

    const onStockClick = (stock) => {
      // console.log("지웅이형",stock.initial.stck_shrn_iscd)
      fetchStockChartData({ stck_shrn_iscd: stock.initial.stck_shrn_iscd, interval: 'day' });
      emit('onStockClick', stock);
    };

    return {
      myStocks,
      removeFromMyStocks,
      onStockClick,
      getMaxSentiment,
      fetchStockChartData
    };
  },
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

/* 관심 종목 리스트 호버링 */
.my-list:hover {
  background-color: #5B5B5B42;
  cursor: pointer;
  transition: background 0.3s ease, opacity 1s ease;
}

/* 관심 종목 텍스트 */
.my-text {
  color: white;
  margin-bottom: 20px;
}

.fa-sizeup {
  font-size: 20px;
}
</style>