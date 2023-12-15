<template>
  <div class="card mb-4">
    <div class="card-header pb-0 d-flex align-items-center justify-content-between"
         style="border-top-left-radius: 15px; border-top-right-radius: 15px; background-color: #01275b;">
      <p class="allstock-text">모든종목</p>

      <select class="form-select" style="width: 150px; margin-bottom: 15px;" v-model="selectedMarket" @change="updateMarket">
        <option value="kospi">코스피</option>
        <option value="kosdaq">코스닥</option>
      </select>
    </div>


    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center justify-content-center mb-0">
          <thead>
          <tr class="all-sizeup">
            <th class="text-center font-weight-bolder">종목명</th>
            <th class="text-center font-weight-bolder">현재가</th>
            <th class="text-center font-weight-bolder">전일대비율</th>
            <th class="text-center font-weight-bolder">여론</th>
            <th class="text-center font-weight-bolder">시가총액(백만)</th>
            <th class="text-center font-weight-bolder">누적거래량</th>
            <th class="text-center font-weight-bolder">관심종목 추가</th>
          </tr>
          </thead>

          <tbody>

          <tr v-for="stock in currentMarketStocks" :key="stock.id" class="all-list"  @click="onStockClick(stock)">
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
              <span class="text-secondary text-lg font-weight-bold" >{{getMaxSentiment(sentiments[stock.initial.COMPANY])}} </span> <!--v-if="sentiments && sentiments[stock.initial.COMPANY]"를 줄수도 있음-->
            </td>
            <td class="align-middle text-center">
              <span class="text-lg font-weight-bolder">{{ formatNumber(stock.initial.hts_avls) }}</span>
            </td>
            <td class="align-middle text-center">
    <span class="text-lg font-weight-bolder">{{
        formatNumber(stock.current_trade.ACML_VOL ? stock.current_trade.ACML_VOL : stock.initial.acml_vol)
      }}</span>
            </td>
            <td class="px-6 py-4 text-center text-gray-500 border-b">
              <i @click.stop="addToMyStocks(stock)" class="fa fa-plus-circle" style="font-size: 25px" aria-hidden="true"></i>
            </td>
          </tr>

          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import {computed, ref } from 'vue';
import { useStore } from 'vuex'
import axios from "axios";
import {formatNumber} from "chart.js/helpers";


export default {
  name: "AllStock",
  props: {
    sentiments: Object
  },
  methods: {formatNumber},

  setup(props, context) {
    const store = useStore();
    const selectedMarket = ref(store.state.StockPage.currentMarket);
    const filteredAllStocks = computed(() => store.getters["StockPage/filteredAllStocks"])
    const Sentiments = computed(() => store.state.StockPage.Sentiments);
    console.log("allstock컴포넌트에서 필터링된 모든주식", filteredAllStocks)
    // console.log("회사명 확인",stock.initial.COMPANY)
    // console.log("allstock컴포넌트에서 sentiment 확인",sentiment)

    // 긍정,중립,부정 아이콘
    const sentimentImages = {
      positive: 'src/assets/img/news_sentiment/positive.png',
      neutral: 'src/assets/img/news_sentiment/neutral.png',
      negative: 'src/assets/img/news_sentiment/negative.png'
    };

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

    // 선택된 시장의 주식 데이터를 가져옵니다.
    const currentMarketStocks = computed(() => {
      if (filteredAllStocks.value) { // allStocks가 정의되었는지 확인합니다.
        // 선택된 시장에 따른 주식 데이터를 가져옵니다.
        if (selectedMarket.value === 'kospi') {
          return filteredAllStocks.value.filter(stock => stock.market === 'kospi');
        } else {
          return filteredAllStocks.value.filter(stock => stock.market === 'kosdaq');
        }
      } else {
        return []; // allStocks가 정의되지 않았다면 빈 배열을 반환합니다.
      }
    });

    function onStockClick(stock) {
      store.dispatch('StockPage/fetchStockChartData', { stck_shrn_iscd: stock.initial.stck_shrn_iscd, interval: 'day' });
      console.log("모든종목 이건확인해햐해",stock)
      context.emit('onStockClick', stock);
      // console.log("stock",stock)
    }

    function updateMarket() {
      store.dispatch('StockPage/updateMarket', selectedMarket.value);
    }

    const addToMyStocks = async (stock)=> {
      store.dispatch('StockPage/addToMyStocks', stock);
      // const alarmstock = { stockid: stock.initial.stck_shrn_iscd, morLes: '+', username: "장건욱", price: 0.1};
      // console.log("allstock에서 넘어가는 stockid 확인",alarmstock)
      // store.dispatch("StockPage/alarmstock", alarmstock)

      //session 객체 선언
      const sessionStorage = window.sessionStorage;
      const url = "http://221.156.60.18:8096/favorite_stock/add";

      //변경
      const favoriteStockBody = {
        "account": JSON.parse(sessionStorage.getItem("token")).account, // 추후 계정 바꿔야함 세션에서 가져오는 아이디로
        "favorite_stock" : {
          [stock.initial.stck_shrn_iscd]:{ // 주식고유번호
            "name": stock.initial.COMPANY, // 회사명
            "fluctuation" : "", //숫자
            "fluctuation_toggle" : "" //plus,minus
          }
        }
      }
      // console.log("favoriteStockBody", favoriteStockBody)
      const response = await axios.post(url, favoriteStockBody).catch(() => null)
      if (!response) return null

      const result = response.data

      // favoite_stock: 세션이름 json형태로 result 넣어줌
      sessionStorage.setItem("favorite_stock", JSON.stringify(result))
      const data = sessionStorage.getItem("favorite_stock")
      console.log("favorite_stock", JSON.parse(data))

    }

    return {
      selectedMarket,
      currentMarketStocks,
      onStockClick,
      updateMarket,
      addToMyStocks,
      filteredAllStocks,
      Sentiments,
      getMaxSentiment,
    };
  }
};
</script>

<style scoped>

/* 모든 종목 리스트 호버링 */
.all-list:hover {
  background-color: #5B5B5B42;
  cursor: pointer;
  transition: background 0.3s ease, opacity 1s ease;
}

/* 모든 종목 타이틀 텍스트 */
.allstock-text{
  color: #ffffff;
  font-size: 20px;
  font-weight: bold;
}

.all-sizeup{
  font-size: 20px;
}

/* 종목가 변동 시, 출력값에 애니메이션 효과 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
