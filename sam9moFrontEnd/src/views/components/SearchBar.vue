<template>
  <div>
    <div class="input-group">
      <span class="input-group-text text-body">
        <i class="fas fa-search" aria-hidden="true"></i>
      </span>
      <input
          type="text"
          class="form-control"
          v-model="searchQuery"
          @input="fetchSearchSuggestions"
          :placeholder="$store.state.isRTL ? '' : '종목명,지수명 입력.'"
      />
    </div>

    <div v-if="suggestions.length">
      <h2>추천 검색어</h2>
      <ul>
        <li v-for="(suggestion, index) in suggestions" :key="index">
          {{ suggestion }}
        </li>
      </ul>
    </div>

    <div v-if="searchResults.length">
      <h2>검색 결과</h2>
      <button v-for="(result, index) in searchResults" :key="index" @click="fetchData(result)">
        {{ result }}
      </button>

      <div v-if="data">

      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const searchQuery = ref('');
    const suggestions = ref([]);
    const searchResults = ref([]);
    const data = ref(null);

    const fetchSearchSuggestions = async () => {
      const response = await axios.get('http://121.179.83.68:8881/stock_api', {
        params: {
          query: searchQuery.value,
        },
      });

      suggestions.value = response.data;
    };

    const fetchData = async (result) => {
      const response = await axios.get('/api/data', {
        params: {
          result,
        },
      });

      data.value = response.data;
    };
    watch(searchQuery, fetchSearchSuggestions);

    return { searchQuery, suggestions, searchResults, data, fetchData };
  },
};
</script>
