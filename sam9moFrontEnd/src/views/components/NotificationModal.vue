<template>
  <div>
    <!-- 등락율 설정 인터페이스 -->
    <div>
      <button @click="decreasePercentage">-</button>
      <p>{{ percentage }}%</p>
      <button @click="increasePercentage">+</button>
    </div>
    <!-- 설정값 저장 버튼 -->
    <button @click="saveNotification">저장</button>
    <!-- 모달창 닫기 버튼 -->
    <button @click="$emit('close')">닫기</button>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';

export default {
  props: ['stockId'],
  setup(props, { emit }) {
    const percentage = ref(0);
    const store = useStore();

    const increasePercentage = () => {
      percentage.value += 5;
    };

    const decreasePercentage = () => {
      if (percentage.value > 0) {
        percentage.value -= 5;
      }
    };

    const saveNotification = () => {
      store.commit('SET_NOTIFICATION', { stockId: props.stockId, percentage: percentage.value });
      emit('close');
    };

    return {
      percentage,
      increasePercentage,
      decreasePercentage,
      saveNotification
    };
  }
};
</script>
