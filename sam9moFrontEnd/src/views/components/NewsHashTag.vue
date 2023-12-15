<template>
  <div style="text-align: center;">
    <div class="hashtag-height" style="background-color: #003D88FF">
      <h5 style="color: #ffffff">뉴스 해시태그 순위</h5>
    </div>

    <div v-if="keywordCountList.length > 0" class="button-container" style="overflow: auto;">
      <div class="d-flex p-3 gap-2 mb-3 text-white justify-content-center flex-wrap " style="width: 100%">
        <div id="hash" class="btn-group">
          <vsud-button type="button"
                       v-for="(item, index) in keywordCountList"
                       :key="index"
                       class="button-style"
                       :style="{padding: `${item.keyword.length * 1.5}px 10px`}">
            <a :href="item.link"
               target="_blank"
               class="fs-6 button-text"
               style="color:#ffffff;">
              #{{ index + 1 }}. {{ item.keyword }}
              <span class="visually-hidden">
              <i class="fas fa-thumbs-up">{{ item.count }}</i>
            </span>
            </a>
          </vsud-button>
        </div>
      </div>
    </div>
    <div v-else>새로운 뉴스가 업데이트 되는 중입니다. 잠시만 기다려주세요...</div>
  </div>
</template>

<script>
import axios from "axios";
import VsudButton from "@/components/VsudButton.vue";

export default {
  name: "NewsHashTagChart",
  components: {VsudButton},

  data() {
    return {
      keywordCountList: [],
    };
  },
  mounted() {
    let today = new Date();
    let year = String(today.getFullYear());
    let month = String(today.getMonth() + 1).padStart(2, "0");
    let date = String(today.getDate()).padStart(2, "0");

    this.fetchKeywordCountList(year + month + date);
  },
  methods: {
    fetchKeywordCountList(date) {
      axios.get(`http://221.156.60.18:8092/keyword/count?date=${date}`)
          .then((response) => {
            this.keywordCountList = response.data.keyword_count_list;
          })
          .catch((error) => {
            console.error(error);
          });
    },
  },
};
</script>

<style scoped>

.button-container {
  display: flex;
  align-items: center;
}

button {
  border-radius: 15px;
  margin-right: 5px;
  padding: 15px;
  background-color: #0e61e0;
  //color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.5s ease;
}

button:hover {
  background-color: #003D88FF;
}


.button-style {
  transition: background 0.3s ease, opacity 0.3s ease;
  opacity: 1;
}


.hashtag-height{
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}



</style>
