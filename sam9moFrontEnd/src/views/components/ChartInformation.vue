<template>
  <div class="card mb-4">
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <div class="stock-layout d-flex flex align-items-start">
            <button class="btn-synthesis shadow-sm" @click="selectTab('종합')">종합</button>
            <button class="btn-news shadow-sm" @click="selectTab('뉴스')">뉴스</button>
          </div>

          <tbody v-if="selectedTab === '종합'" style="height: 405px; overflow-y: auto;">
          <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
              <table class="table align-items-center justify-content-center mb-0">
                <thead>
                <tr style="height: 100px;">
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">주식 전일
                    최저가:{{ formatNumber(selectedStocks.initial.stck_prdy_lwpr) }}
                  </th>
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">주식 전일
                    최고가:{{ formatNumber(selectedStocks.initial.stck_prdy_hgpr) }}
                  </th>
                </tr>
                <tr style="height: 100px;">
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">전일종가:{{
                      formatNumber(selectedStocks.initial.stck_prdy_clpr)
                    }}
                  </th>
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">누적 거래량:{{
                      formatNumber(selectedStocks.current_trade.ACML_VOL ? selectedStocks.current_trade.ACML_VOL : selectedStocks.initial.acml_vol)
                    }}
                  </th>
                </tr>
                <tr style="height: 100px;">
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">누적 거래 대금:{{
                      formatNumber(selectedStocks.current_trade.ACML_VOL ? selectedStocks.current_trade.ACML_VOL : selectedStocks.initial.acml_tr_pbmn)
                    }}</th>
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">PER:{{
                      selectedStocks.initial.per
                    }}
                  </th>
                </tr>
                <tr style="height: 100px;">

                  <th class="text-center font-weight-bolder" style="font-size: 20px;">PBR:{{
                      selectedStocks.initial.pbr
                    }}
                  </th>
                  <th class="text-center font-weight-bolder" style="font-size: 20px;">EPS:{{
                      selectedStocks.initial.eps
                    }}
                  </th>
                </tr>
                </thead>
              </table>
            </div>
          </div>
          </tbody>
        </table>

        <div class="news-list" @scroll="CompanyCheckScroll;" v-if="selectedTab === '뉴스'">
          <div v-for="(news,index) in companynews" :key="index">
            <div style="display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
              <div>
                <h4>{{ news.news_title }}</h4>
                <p>{{ news.content_summary }}</p>
                <p>{{ news.keyword }}</p>
              </div>
              <div style="align-self: flex-end; position: relative; bottom: 35px;">
                <button class="detail-button shadow-sm" @click="handleButtonClick(news.news_link)">상세보기</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, onMounted, reactive, watch} from "vue";
import axios from "axios";
import {formatNumber} from "chart.js/helpers";

export default {
  name: "ChartInformation",
  methods: {formatNumber},
  props: {
    selectedStock: {
      type: Object
    }
  },

  setup(props) {
    const selectedStocks = reactive(props.selectedStock);
    const selectedTab = ref('종합');
    const companynews = ref([]);
    const companypage = ref(1);

    const selectTab = (tabName) => {
      selectedTab.value = tabName;
      if (tabName === '뉴스') {
        CompanyNews();
      }
    };

    const CompanyNews = async () => {
      try {
        const res = await axios.get(`http://221.156.60.18:8092/news/stock/${selectedStocks.id}?page_Idx=${companypage.value}`);
        if (Array.isArray(res.data.news_list)) {
          companynews.value = [...companynews.value, ...res.data.news_list];
        }
      } catch (error) {
        console.error(error);
      }
    };

    const CompanyCheckScroll = (event) => {
      if (selectedTab.value !== '뉴스') return;

      let element = event.target;
      if (element.scrollHeight - element.scrollTop <= element.clientHeight + 200) {
        companypage.value += 1;
        CompanyNews();
      }
    }

    const handleButtonClick = (newsLink) => {
      window.open(newsLink, '_blank');
    }

    watch(() => props.selectedStock, (newStock) => {
      Object.assign(selectedStocks, newStock);
      if (selectedTab.value === '뉴스') {
        companypage.value = 1;
        companynews.value = [];
        CompanyNews();
      } else if (selectedTab.value === '종합') {
        companypage.value = 1;
        companynews.value = [];
        CompanyNews(); // '종합' 탭에서도 주식이 바뀔 때 뉴스 정보를 미리 불러옴
      }
    });

    onMounted(() => {
      CompanyNews();
    });

    return {
      selectedStocks,
      selectedTab,
      companynews,
      selectTab,
      CompanyCheckScroll,
      handleButtonClick
    };
  },
}
</script>


<style scoped>

/* 뉴스 버튼 디자인 */
.btn-news {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #0e61e0;
  border: none; /* 테두리 제거 */
  font-weight: bold;
  margin-top: 10px;
  margin-left: 10px;
  margin-bottom: 10px;
}

/* 뉴스 버튼 호버링 */
.btn-news:hover {
  background-color: #003D88FF;
  opacity: 1;
}

/* '종합' 버튼 디자인 */
.btn-synthesis {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #dcb208;
  border: none; /* 테두리 제거 */
  font-weight: bold;
  margin: 10px 0px 10px 10px; /* 좌측부터 상 우 하 좌 */
}

/* 종합 버튼 호버링 */
.btn-synthesis:hover {
  background-color: #a28404;
  opacity: 1;
}

/* 뉴스 리스트 */
.news-list {
  height: 406px;
  overflow-y: auto;
  padding: 15px;
}

/* 차트정보 특정종목 뉴스 버튼 디자인 */
.detail-button {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #0e61e0;
  border: none; /* 테두리 제거 */
  font-weight: bold;
}

/* 차트정보 특정종목 뉴스 버튼 호버링 */
.detail-button:hover {
  background-color: #003D88FF;
  opacity: 1;
}
</style>