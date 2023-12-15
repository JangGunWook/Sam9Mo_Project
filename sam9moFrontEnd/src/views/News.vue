<template>
  <div class="row justify-content-center custom-height">
    <div class="col-lg-10">
      <div class="card z-index-2">
        <div class="nav-wrapper position-relative end-0">
          <div class="nav nav-pills nav-fill p-1" role="tablist">

            <!-- 뉴스 카테고리 버튼 생성 -->
            <button v-for="(value, category) in categories" :key="value" class="nav-item"
                    :class="['nav-link', { 'active': selectedCategory.value === value, 'selected': selectedCategory.value === value }]"
                    @click="() => selectCategory(value)"
                    role="tab"
                    :aria-selected="selectedCategory.value === value ? 'true' : 'false'"
            >
              {{ category }}
            </button>
          </div>
        </div>

        <!-- 뉴스 목록 출력 -->
        <div v-if="selectedNews" class="news-set">
          <h3>{{ selectedNews.news_title }}</h3>
          <p>{{ selectedNews.content_summary }}</p>
          <p>키워드: {{ selectedNews.keyword }}</p>
          <p>감성 분석 결과: {{ selectedNews.news_sentiment }}</p>
          <button @click="selectedNews = null">Close</button>
        </div>

        <!-- 뉴스 카테고리 목록 요소-->
        <div class="news-list" @scroll="checkScroll">
          <div>
            <div v-for="item in news" :key="item._id">

              <div class="news-element">
                <div class="col-md-2">
                  <img :src="item.news_img" alt="이미지가 없습니다" class="news-thumbnail">
                </div>

                <div class="content-section col-md- 8">
                  <h4 class="title-section">{{ item.news_title }}</h4>
                  <p>{{ item.content_summary }}</p>
                  <div class="kword-section">
                    <p>키워드: {{ item.keyword }}</p>
                  </div>
                </div>

                <div class="col-md-3 content-container">
                  <img class="icon-set" :src="sentimentImages[item.news_sentiment]"
                       alt="Sentiment analysis result"/>
                  <h5 class="sentiment-text">{{ getSentimentText(item.news_sentiment) }}</h5> <!-- 감성분석 출력 -->
                  <button @click="() => openNews(item.news_link)" class="btn-set">상세보기</button>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {ref, onMounted, computed} from "vue";

export default {
  name: "NewsPage",

  setup() {
    const categories = {"전체": 'whole', "경제": 'money', "사회": 'society', "정치": 'politics'};
    const selectedCategory = ref('전체');
    const news = ref([]);
    const page = ref(1);
    const selectedNews = ref(null);

    // 전체 뉴스 로드
    const loadAllNews = async () => {
      try {
        const res = await axios.get(`http://221.156.60.18:8092/news/whole?page_Idx=${page.value}`);
        if (Array.isArray(res.data.news_list)) {
          news.value = [...news.value, ...res.data.news_list];
        }
      } catch (error) {
        console.error(error);
      }
    };

    const openNews = (news_link) => {
      window.open(news_link, '_blank');
    };

    // 특정 카테고리 뉴스 로드
    const loadSpecificNews = async (category) => {
      try {
        let url = ''
        if (category != "whole") {
          url = `http://221.156.60.18:8092/news/category/${category}?page_Idx=${page.value}`;
        } else {
          url = `http://221.156.60.18:8092/news/whole?page_Idx=${page.value}`;
        }
        const res = await axios.get(url);
        if (Array.isArray(res.data.news_list)) {
          news.value = [...news.value, ...res.data.news_list];
        }

      } catch (error) {
        console.error(error);
      }
    };

    // 전체,특정 카테고리 판별
    const selectCategory = (category) => {
      selectedCategory.value = category;
      news.value = [];
      page.value = 1;
      if (selectedCategory.value === '전체') {
        loadAllNews();
      } else {
        loadSpecificNews(selectedCategory.value);
      }
    };


    // 스크롤 다운 시, 스크롤 바 축소 및 추가 뉴스 출력
    const checkScroll = (event) => {
      let element = event.target;
      if (element.scrollHeight - element.scrollTop <= element.clientHeight + 200) {
        page.value += 1;
        if (selectedCategory.value === '전체') {
          loadAllNews();
        } else {
          loadSpecificNews(selectedCategory.value);
        }
      }
    };

    // 감성분석에 따른 긍정, 중립, 부정 출력
    const getSentimentText = (news_sentiment) => {
      switch (news_sentiment) {
        case 'positive':
          return '긍정';
        case 'negative':
          return '부정';
        default :
          return '중립';
      }
    };


    // 긍정,중립,부정 아이콘
    const sentimentImages = {
      positive: 'src/assets/img/news_sentiment/positive.png',
      neutral: 'src/assets/img/news_sentiment/neutral.png',
      negative: 'src/assets/img/news_sentiment/negative.png'
    };

    onMounted(() => selectCategory(selectedCategory.value));

    return {
      categories,
      selectedCategory,
      news,
      selectCategory,
      checkScroll,
      selectedNews,
      sentimentImages,
      openNews,
      getSentimentText
    };
  }
}
</script>

<style scoped>

/* 일반 상태 */
.nav-item.nav-link {
  transition: background-color 0.3s ease, color 0.3s ease; /* 색상 변경 애니메이션 */
}

/* 호버링 상태 */
.nav-item.nav-link:hover {
  background-color: #0e61e0; /* 배경색 */
}

/* 뉴스 목록 출력 영역 */
.news-list {
  height: 1100px;
  overflow-y: auto;
  padding: 20px;
}

/* 뉴스 목록 썸네일 이미지 */
.news-thumbnail {
  width: 170px; /* 이미지 넓이 */
  height: 180px; /* 이미지 높이 (auto로 설정하여 비율 유지) */
  margin-right: 20px; /* 이미지와 제목 사이의 간격 */
  margin-bottom: 35px;
}

/* 뉴스 목록 content 수평 배치 */
.news-element {
  display: flex;
}

/* 감성분석,상세보기 버튼 컨테이너 */
.content-container {
  margin-left: 40px;
}

.content-section {
  display: flex;
  flex-direction: column;
  margin-left: 20px;
}

.kword-section {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.title-section {
  display: flex;
  align-items: center;
}

.news-set {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border: 1px solid black;
}
.nav-item{
  font-size: 25px;
  font-weight: bolder;
  color: white;

}
/* 카테고리 버튼 배치 */
.nav-wrapper {
  padding: 20px;
}

/* 상세뉴스 보기 버튼 */
.btn-set {
  position: relative;
  bottom: 10px;
  left: 2px;
  border-radius: 15px;
  background-color: #0e61e0;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: bold;
  margin-top: 30px;
  padding: 5px;

  transition: background-color 0.3s ease;
}

/* 버튼 호버링 색상 */
button:hover {
  background-color: #003D88FF;
}

/* 감성분석 텍스트 */
.sentiment-text {
  margin-top: 20px;
  margin-left: 16px;
}

/* 감성분석 아이콘 */
.icon-set {
  position: relative;
  top: 15px;
  padding-left: 10px;
  padding-bottom: 10px;
}

.nav-item {
  margin-left: 5px;
}

</style>
