<template>
  <div class="container top-0 position-sticky z-index-sticky">
    <div class="row">
      <div class="col-12">
      </div>
    </div>
  </div>
  <main class="mt-0 main-content main-content-bg">
    <section>
      <div class="page-header min-vh-75">
        <div class="container">
          <div class="row">
            <div class="mx-auto col-xl-4 col-lg-5 col-md-6 d-flex flex-column">
              <div class="mt-8 card card-plain">
                <div class="pb-0 card-header text-start">
                  <h3 class="font-weight-bolder text-info text-gradient">어서오세요!</h3>
                  <p class="mb-0">"Trust, Samsung 10F Dreams Come True!"</p>
                </div>
                <div class="card-body">
                  <form role="form" class="text-start">
                    <label>이메일/ID</label>
                    <input v-model="userEmail" type="email" class="form-control form-control-default invalid" name="email" placeholder="이메일" isrequired="false">
                    <label>패스워드/PW</label>
                    <input v-model="userPassword" type="password" class="form-control form-control-default invalid" name="password" placeholder="패스워드" isrequired="false">
                    <vsud-switch id="rememberMe" checked>계정 정보 기억하기</vsud-switch>
                    <div class="text-center">

                      <vsud-button
                          class="my-4 mb-2"
                          variant="gradient"
                          color="info"
                          full-width
                          @click="signInHandler"
                          :to="{ name: 'Sign In' }"
                      >로그인</vsud-button>

                    </div>
                  </form>
                </div>
                <div class="px-1 pt-0 text-center card-footer px-lg-2">
                  <p class="mx-auto mb-4 text-sm">
                    계정이 없으신가요?
                    <a href="#/sign-up" class="text-info text-gradient font-weight-bold"
                    >회원가입</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="top-0 oblique position-absolute h-100 d-md-block d-none me-n8">
                <div
                    class="bg-cover oblique-image position-absolute fixed-top ms-auto h-100 z-index-0 ms-n6"
                    :style="{
                    backgroundImage:
                      `url(${bgImg})`,
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import VsudSwitch from "@/components/VsudSwitch.vue";
import VsudButton from "@/components/VsudButton.vue";
import bgImg from "@/assets/img/curved-images/curved9.jpg"
import { ref } from 'vue';
import axios from 'axios';
import router from "../router/index"

const body = document.getElementsByTagName("body")[0];

export default {
  name: "SigninPage",
  components: {
    VsudSwitch,
    VsudButton,
  },
  setup() {

    const url = 'http://221.156.60.18:8989/sign-in'
    const userEmail = ref('')
    const userPassword = ref('')

    const sessionStorage = window.sessionStorage;
    console.log("sessionStorage", sessionStorage)

    if (sessionStorage.length != 0) {
      router.push({name: "Dashboard"})
    }

    const signInHandler = async (event) => {

      event.preventDefault();

      console.log("userEmail", userEmail.value, "userPassword", userPassword.value)

      if (userEmail.value == 0) {
        alert("이메일을 입력하세요")
        return
      }
      if (userPassword.value == 0) {
        alert("비밀번호를 입력하세요")
        return
      }

      const fetchSignInData = async () => {

        const signInBody = {
          "account": userEmail.value,
          "password": userPassword.value
        }

        console.log("loginBody", signInBody)

        const signInHeader = {
          headers : {
            "finance-agent" : "SAM9MO/0.0.1"
          }
        }

        const response = await axios.post(url, signInBody, signInHeader).catch(() => null)
        if (!response) return null

        const result = response.data
        return result
      }

      const fetchStockData = async (userEmail) => {

        const url = "http://221.156.60.18:8096/favorite_stock/receive";
        const requestBody = {
          "account" : userEmail
        }
        const response = await axios.post(url, requestBody).catch(() => null)
        if (!response) return null

        const result = response
        return result
      }

      const signInResponse = await fetchSignInData()
      console.log("userEmail", userEmail.value)
      const favoritestockResponse = await fetchStockData(userEmail.value)

      console.log("signInResponse", signInResponse)
      console.log("favoritestockResponse", favoritestockResponse)

      if (!signInResponse || !signInResponse.data) {
        alert("로그인에 실패했습니다. 아이디나 비밀번호를 다시 확인하세요")
        return
      }



      const set_token_data = {
        "account" : userEmail.value,
        "token_data" : signInResponse.data
      }

      sessionStorage.setItem("token", JSON.stringify(set_token_data))
      sessionStorage.setItem("favorite_stock", JSON.stringify(favoritestockResponse.data))
      const token_data = JSON.parse(sessionStorage.getItem("token"))
      const favorite_stock_data = JSON.parse(sessionStorage.getItem("favorite_stock"))
      console.log("token_data", token_data)
      console.log("favorite_stock_data", favorite_stock_data)

      router.push({name: "Dashboard"})
    }

    return {
      userEmail,
      userPassword,
      signInHandler
    }
  },
  data() {
    return {
      bgImg
    }
  },
  beforeMount() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    body.classList.remove("bg-gray-100");
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
    body.classList.add("bg-gray-100");
  },
};
</script>