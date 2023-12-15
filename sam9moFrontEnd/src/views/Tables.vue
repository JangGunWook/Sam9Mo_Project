<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-lg-11">
          <CandleStickChart v-if="selectedStock" :selectedStock="selectedStock"
                            @close="handleCloseClick"></CandleStickChart>
        <MyStock :stocks="myStocks" :sentiments="Sentiments" @removeFromMyStocks="removeFromMyStocks" @onStockClick="handleStockClick"/>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-11">
        <AllStock :stocks="filteredAllStocks" :sentiments="Sentiments" @addToMyStocks="addToMyStocks" @onStockClick="handleStockClick"/>

      </div>
    </div>
  </div>
</template>

<script>
import {ref, onMounted, onBeforeUnmount, computed} from 'vue';
import MyStock from "./components/MyStock.vue";
import AllStock from "@/views/components/AllStock.vue";
import CandleStickChart from "@/views/components/CandleStickChart.vue"
import {useStore} from 'vuex';

export default {
  name: "StockPage",
  components: {
    MyStock,
    AllStock,
    CandleStickChart
  },

  setup() {
    const store = useStore();
    const selectedStock = ref(null);
    const myStocks = computed(() => store.state.StockPage.myStocks);
    const allStocks = computed(() => store.state.StockPage.allStocks);
    const filteredAllStocks = computed(() => store.getters["StockPage/filteredAllStocks"])
    const Sentiments = computed( ()=>store.state.StockPage.Sentiments)

    // 모든종목
    const fetchAllStocks = async () => {
      try {
        await store.dispatch('StockPage/fetchAllStocks');
      } catch (error) {
        console.error('API 에러:', error);
      }
    };

    // 세션에서 가져온 사용자의 관심종목
    const fetchFavoriteMyStocks = async ()=>{
      try {
        await store.dispatch('StockPage/fetchFavoriteMyStocks')
        console.log("사용자의 관심종목을 가져옴")
      }catch (error){
        console.log("사용자의 관심종목을 가져오지 못함")
      }
    };

    // 여론데이터
    const fetchAllSentiments = async () =>{
      try {
        await store.dispatch('StockPage/fetchAllSentiments')
      }catch (error){
        console.log("여론데이터를 가져오는데 실패했습니다.")
      }
    };

    const addToMyStocks = (stock) => {
      store.dispatch('StockPage/addToMyStocks', stock);
    };

    const removeFromMyStocks = (stock) => {
      store.dispatch('StockPage/removeFromMyStocks', stock);
    };

    const handleStockClick = async (stock) => {
      selectedStock.value = stock;
      // console.log("특정종목 클릭시 차트 데이터로 넘어가는 selectedStock 확인작업", stock)
      try {
        await store.dispatch('StockPage/fetchStockChartData', {
          stck_shrn_iscd: selectedStock.value.initial.stck_shrn_iscd,
          interval: 'day'
        });
      } catch (error) {
        console.error('차트 데이터를 불러오는 데 실패했습니다:', error);
      }
    };

    // 차트 컴포넌트 닫기
    const handleCloseClick = () => {
      selectedStock.value = null;
    };

    let intervalId = null;

    // 페이지가 실행시 fetchAllStocks,fetchFavoriteMyStocks,fetchAllSentiments를
    // 호출하고 주기적으로 fetchAllStocks,fetchFavoriteMyStocks을 가져온다.
    onMounted(async () => {
      await fetchAllStocks()
      await fetchFavoriteMyStocks()
      await fetchAllSentiments()
      intervalId = setInterval(async () => {
        await fetchAllStocks();
        await fetchFavoriteMyStocks();
      }, 5000);
    });


    onBeforeUnmount(() => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    });

    return {
      allStocks,
      myStocks,
      addToMyStocks,
      removeFromMyStocks,
      handleStockClick,
      selectedStock,
      handleCloseClick,
      filteredAllStocks,
      Sentiments
    }
  }
};
</script>


<style scoped>


</style>
