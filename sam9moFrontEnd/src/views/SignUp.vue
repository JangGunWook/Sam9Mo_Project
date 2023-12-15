<template>

  <!--  <navbar btn-background="bg-gradient-primary" />-->
  <div
      class="pt-5 m-3 page-header align-items-start min-vh-50 pb-11 border-radius-lg"
      :style="{
      backgroundImage:   `url(${bgImg})`,
    }"
  >
    <!--    <div >-->
    <!--      <h4>Sam 9F Mo. 10만 전자의 꿈. </h4>-->
    <!--    </div>-->
    <span class="mask bg-gradient-dark opacity-6"></span>
    <div class="container">
      <div class="row justify-content-center">
        <div class="mx-auto text-center col-lg-5">
          <h1 class="mt-5 mb-2 text-white">환영합니다!</h1>
          <p class="text-white text-lead">
            "Trust, Samsung 10F Dreams Come True!"
          </p>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <div class="row mt-lg-n12 mt-md-n11 mt-n10 justify-content-center">
      <div class="mx-auto col-xl-4 col-lg-5 col-md-7">
        <div class="card z-index-0">
          <div class="pt-4 text-center card-header">
            <h3>Sentimental Investment</h3>
          </div>
          <div class="card-body">
            <form role="form">
              <div class="mb-3">
                <input v-model="userName" type="text" class="form-control form-control-default invalid" name="name" placeholder="이름" isrequired="false">
              </div>
              <div class="mb-3">
                <input v-model="userEmail" type="email" class="form-control form-control-default invalid" name="email" placeholder="이메일" isrequired="false">
              </div>
              <div class="mb-3">
                <input v-model="userPassword" type="password" class="form-control form-control-default invalid" name="password" placeholder="패스워드" isrequired="false">
              </div>
              <div class="mb-3">
                <input v-model="searchTerm" type="text" class="form-control form-control-default invalid" name="stocks" placeholder="관심종목" isrequired="false">
              </div>
              <ul
                  v-if="searchStocks.length"
                  class="list-group"
              >
                <li
                    v-for="stock in searchStocks"
                    :key="stock.name"
                    @click="selectStock(stock.name)"
                    class="list px-0 mb-2 border-0 list-group-item d-flex align-items-center"
                >
                  {{ stock.name }}
                </li>
              </ul>
              <vsud-button v-for="(stock, index) in selectedStock" :key="index" color="primary" variant="gradient" class="my-1 mb-2" style="margin-right: 5px;" @click="deleteStock(stock)">{{stock}}</vsud-button>

              <vsud-checkbox id="flexCheckDefault" checked>
                I agree the
                <a
                    href="javascript:;"
                    class="text-dark font-weight-bolder"
                >Terms and Conditions</a>
              </vsud-checkbox>

              <div class="text-center">
                <vsud-button color="dark" full-width variant="gradient" class="my-4 mb-2" @click="signUpHandler">회원가입</vsud-button>
              </div>
              <p class="text-sm mt-3 mb-0">
                이미 계정이 있으신가요?
                <a
                    href="#/sign-in"
                    class="text-dark font-weight-bolder"
                >로그인</a>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import VsudCheckbox from "@/components/VsudCheckbox.vue";
import VsudButton from "@/components/VsudButton.vue";
import bgImg from "@/assets/img/curved-images/curved6.jpg";
import stocks from "../data/stocks.json"
import {ref, computed} from 'vue'
import axios from 'axios';
import router from '../router';

export default {
  name: "SignUp",
  components: {
    Navbar,
    VsudCheckbox,
    VsudButton,
  },
  setup() {

    let searchTerm = ref('')
    let selectedStock = ref([])

    let userName = ref('')
    let userEmail = ref('')
    let userPassword = ref('')

    const searchStocks = computed(() => {
      if (searchTerm.value === '') {
        return []
      }

      let matches = 0

      return stocks.filter(stock => {
        if (stock.name.toLowerCase().includes(searchTerm.value.toLowerCase()) && matches < 10) {
          matches++
          return stocks
        }
      })
    });

    const selectStock = (stock) => {
      selectedStock.value.push(stock)
      searchTerm.value = ''

    }

    const deleteStock = (stock) => {
      selectedStock.value = selectedStock.value.filter(item => item !== stock)
      searchTerm.value = ''
    }

    const signUpHandler = async (event) => {

      event.preventDefault();

      if (userName.value == 0) {
        alert("이름을 입력하세요")
        return
      }
      if (userEmail.value == 0) {
        alert("이메일을 입력하세요")
        return
      }
      if (userPassword.value == 0) {
        alert("비밀번호을 입력하세요")
        return
      }

      const fetchSignUpData = async () => {

        const url = 'http://221.156.60.18:8989/sign-up'

        const signUpBody = {
          "account": userEmail.value,
          "password": userPassword.value,
          "name":  userName.value
        }

        console.log("loginBody", signUpBody)

        const response = await axios.post(url, signUpBody).catch(() => null)
        if (!response) return null

        const result = response.data
        return result
      }

      const kospi_stock_list = ['005930', '373220', '000660', '207940', '005935',
        '005490', '005380', '051910', '035420', '000270',
        '006400', '068270', '003670', '035720', '105560',
        '028260', '012330', '055550', '066570', '096770',
        '032830', '003550', '323410', '033780', '086790',
        '000810', '034730', '015760', '138040', '017670',
        '018260', '011200', '329180', '010130', '009150',
        '047050', '259960', '316140', '034020', '024110']

      const selectedStock_list = selectedStock.value.map(stockName => {
        const foundStock = stocks.find(stock => stock.name === stockName);
        if (foundStock) {
          const obj = {};
          let market = ""
          if (kospi_stock_list.includes(foundStock.code)) {
            market = "kospi"
          } else {
            market = "kosdaq"
          }
          obj[foundStock.code] = { name: foundStock.name, market : market};
          return obj;
        }
        return null;
      }).filter(Boolean);

      console.log("selectedStock_list", selectedStock_list)

      const fetchFavoriteStockData = async () => {

        const url = "http://221.156.60.18:8096/favorite_stock/send";

        const favoriteStockBody = {
          "account": userEmail.value,
          "favorite_stock" : selectedStock_list
        }

        console.log("favoriteStockBody", favoriteStockBody)

        const response = await axios.post(url, favoriteStockBody).catch(() => null)
        if (!response) return null

        const result = response.data
        return result
      }

      const signUpResponse = await fetchSignUpData();
      console.log("signUpResponse", signUpResponse)

      if (signUpResponse.status == "SUCCESS") {
        const favoriteStockResponse = await fetchFavoriteStockData()
        if (!favoriteStockResponse) console.log("관심 종목 추가 시 에러", favoriteStockResponse)
        router.push({name : "Sign In"})
      } else {
        alert("회원가입에 실패했습니다. 정보를 다시 입력해주세요")
        return
      }

    }

    return {
      userName,
      userEmail,
      userPassword,
      stocks,
      searchTerm,
      searchStocks,
      selectStock,
      deleteStock,
      selectedStock,
      signUpHandler
    }
  },
  data() {
    return {
      bgImg
    }
  },
  created() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
  },
};
</script>

<style>
.list:hover {
  cursor: pointer; /* 마우스 커서를 손가락 모양으로 변경 */
  background-color: #f5f5f5; /* 배경색을 회색으로 변경 */
}
</style>