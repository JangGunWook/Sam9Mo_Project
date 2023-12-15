<template>
  <!-- 코스피,코스닥,코스피200 area 차트 -->
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-md-5">
        <div class="card-header pb-3"
             style="border-top-left-radius: 15px;
             border-top-right-radius: 15px;
             background-color: #003D88FF;">
        </div>
        <div class="card-body shadow-lg" style="border-bottom-left-radius: 15px;
             border-bottom-right-radius: 15px; background-color: #ffffff">
          <StockAreaChart/>
        </div>
      </div>

      <!-- n-gram bubble 차트 -->
      <div class="col-md-7">
        <div class="card-header pb-3"
             style="border-top-left-radius: 15px;
             border-top-right-radius: 15px;
             background-color: #003D88FF;">
        </div>
        <div class="card-body shadow-lg" style="border-bottom-left-radius: 15px;
             border-bottom-right-radius: 15px; background-color: #ffffff">
          <h5 class="bubble-text">
            Today's KeyWord
          </h5>
          <NgramChart/>
        </div>
      </div>

      <!-- NewsHashTag 차트 -->
      <div class="col-lg-12 hashtag-height">
        <div class="card z-index-2 custom-height">
          <NewsHashTagChart/>
        </div>
      </div>
    </div>
  </div>


</template>
<script>

import US from "../assets/img/icons/flags/US.png";
import DE from "../assets/img/icons/flags/DE.png";
import GB from "../assets/img/icons/flags/GB.png";
import BR from "../assets/img/icons/flags/BR.png";
import NgramChart from "@/views/components/NgramChart.vue";
import NewsHashTagChart from "@/views/components/NewsHashTag.vue";
import StockAreaChart from "@/views/components/StockAreaChart.vue";

export default {
  name: "DashboardDefault",
  components: {
    StockAreaChart,
    NewsHashTagChart,
    NgramChart,
  },
  data() {
    return {
      stats: {
        iconBackground: "bg-gradient-success",
        money: {
          title: "Today's Money",
          value: "$53,000",
          percentage: "+55%",
          iconClass: "ni ni-money-coins",
        },
        users: {
          title: "Today's Users",
          value: "2,300",
          percentage: "+3%",
          iconClass: "ni ni-world",
        },
        clients: {
          title: "New Clients",
          value: "+3,462",
          percentage: "-2%",
          iconClass: "ni ni-paper-diploma",
          percentageColor: "text-danger",
        },
        sales: {
          title: "Sales",
          value: "$103,430",
          percentage: "+5%",
          iconClass: "ni ni-cart",
        },
      },
      sales: {
        us: {
          country: "United States",
          sales: 2500,
          value: "$230,900",
          bounce: "29.9%",
          flag: US,
        },
        germany: {
          country: "Germany",
          sales: "3.900",
          value: "$440,000",
          bounce: "40.22%",
          flag: DE,
        },
        britain: {
          country: "Great Britain",
          sales: "1.400",
          value: "$190,700",
          bounce: "23.44%",
          flag: GB,
        },
        brasil: {
          country: "Brasil",
          sales: "562",
          value: "$143,960",
          bounce: "32.14%",
          flag: BR,
        },
      },
    };
  },
};
</script>
<style scoped>

.custom-height {
  height: 120px; /* 뉴스해시태그 영역 높이 */
}

.bubble-text {
  margin-top: 10px;
  font-weight: bold;
}

.hashtag-height {
  margin-top: 20px;
}

</style>