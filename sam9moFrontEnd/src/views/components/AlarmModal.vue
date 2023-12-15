<template>
  <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
       aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">{{ selectedStocks.initial.COMPANY }} 알림설정</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div style="display: block; position: relative;">
              <span><i class="fas fa-minus-circle" style="font-size: 25px; position: relative;" @click="decreasePercentage"></i></span>
              <span style="text-align: center; align-items: center; position: absolute; margin-left: 5px;">{{ percentage.toFixed(1) }}%</span>
              <span><i class="fas fa-plus-circle" style="font-size: 25px; position: absolute; display: inline-flex; margin-left: 45px;" @click="increasePercentage"></i></span>
            </div>
            <div style="display: flex; position: absolute; margin-left: 150px; text-align: center; ">
              이상 <input id="plus" type="radio" name="plus_minus" value="plus" style="margin-right: 10px">
              이하 <input id="minus" type="radio" name="plus_minus" value="minus">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <!-- '닫기' 버튼. 이 버튼을 누르면 모달이 닫힙니다. -->
          <button type="button" class="alarm-close shadow-sm" data-bs-dismiss="modal">닫기</button>
          <!-- '알림 등록하기' 버튼. 이 버튼을 누르면 registerAlert 함수가 호출됩니다. -->
          <button type="button" class="set-alarm shadow-sm" data-bs-dismiss="modal" @click="registerAlert">알림 등록하기</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import {ref} from "vue";
import axios from "axios";
// import {useStore} from "vuex";

export default {
  name: "AlarmModal",
  props: {
    selectedStock: {
      type: Object
    }
  },
  setup(props) {
    // const store = useStore()

    const selectedStocks = ref(props.selectedStock);
    const percentage = ref(0);
    const selectedValue = ref("");

    const increasePercentage = () => {
      percentage.value += 0.1;
    };
    const decreasePercentage = () => {
      percentage.value -= 0.1;
    };

    // '알림 등록하기' 버튼을 눌렀을 때 호출되는 함수
    const registerAlert = async () => {
      // 알림 설정 정보를 객체로 만듭니다.
      // stockid: selectedStocks.value.initial.stck_shrn_iscd,  // 선택한 주식의 고유번호
      // username: "장건욱",  // 사용자 이름. 실제 구현에서는 적절한 사용자 이름을 사용해야 합니다.
      // morLes: percentage.value >= 0 ? '+' : '-',  // 퍼센트가 0 이상이면 '+', 아니면 '-'를 설정
      // price: []

      console.log("알림등록 버튼 클릭")

      const url = "http://221.156.60.18:8096/favorite_stock/update";


      // JavaScript
      const plus = document.getElementById('plus');
      const minus = document.getElementById('minus');

      if (plus.checked) {
        selectedValue.value = plus.value;
      } else if (minus.checked) {
        selectedValue.value = minus.value;
      }

      const favoriteStockBody = {
        "account": JSON.parse(sessionStorage.getItem("token")).account,
        "favorite_stock": selectedStocks.value.id,
        "fluctuation": percentage.value,  //c
        "fluctuation_toggle": selectedValue.value
      }

      console.log("알람등록시 세션에 넘어가는 값 확인", favoriteStockBody,)

      const response = await axios.post(url, favoriteStockBody).catch(() => null)
      console.log("알람response확인", response)
      const result = response.data
      result.test = "test"
      console.log("result", result, typeof (result))
      sessionStorage.setItem("favorite_stock", JSON.stringify(result))
      const data = sessionStorage.getItem("favorite_stock")
      console.log("favorite_stock", JSON.parse(data))

      // Vuex 액션을 호출하여 알림 설정 정보를 스토어에 저장합니다.
      // store.dispatch('StockPage/saveAlertSetting', favoriteStockBody);
    };

    return {
      registerAlert,
      increasePercentage,
      decreasePercentage,
      selectedStocks,
      percentage,
    };
  }
};

</script>
<style scoped>

/* 알림등록 버튼 */
.set-alarm {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #03C41499;
  border: none; /* 테두리 제거 */
  margin-left: 10px;
  font-weight: bold;
  height: 45px;
}

/* 알림등록 버튼 호버링 */
.set-alarm:hover {
  background-color: #003D88FF;
  opacity: 1;
}

/* 알림창 닫기버튼 */
.alarm-close {
  padding-inline: 10px;
  font-size: 15px;
  border-radius: 10px;
  transition: background 0.3s ease, opacity 0.3s ease;
  color: #ffffff;
  background-color: #0e61e0;
  border: none; /* 테두리 제거 */
  margin-left: 10px;
  font-weight: bold;
  height: 45px;
}

/* 알림창 닫기버튼 호버링 */
.alarm-close:hover {
  background-color: #003D88FF;
  opacity: 1;
}
</style>