<template>
  <div id="sidenav-collapse-main" class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100">
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse class="menuText" :class="{ 'nav-text': true, 'active': $route.name === 'Dashboard' }" nav-text="메인" :to="{ name: 'Dashboard' }">
          <template #icon>
            <icon name="dashboard" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse :class="{ 'nav-text': true, 'active': $route.name === 'Tables' }" nav-text="증권" :to="{ name: 'Tables' }">
          <template #icon>
            <icon name="tables" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse :class="{ 'nav-text': true, 'active': $route.name === 'Billing' }" nav-text="뉴스" :to="{ name: 'Billing' }">
          <template #icon>
            <icon name="billing" />
          </template>
        </sidenav-collapse>
      </li>
    </ul>
  </div>

  <div  id="alarm" class="modal" tabindex="-1" style="display: none">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ stock_name }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>{{ time_now }}</p>
          <p>{{ stock_content }}</p>
        </div>
        <div class="modal-footer">
          <button  type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="close">Close</button>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
import Icon from "@/components/Icon.vue";
import SidenavCollapse from "./SidenavCollapse.vue";
import axios from "axios";
import {onBeforeUnmount, onMounted, ref} from "vue";

export default {
  name: "SidenavList",
  components: {
    Icon,
    SidenavCollapse,
  },
  props: {
    cardBg: {
      type: String,
      default: ""
    },
  },
  setup() {

    function close() {
      document.getElementById("alarm").style.display= "none";
    }
    const stock_name = ref('');
    const time_now = ref('');
    const stock_content = ref('');

    const now = new Date();

    const year = now.getFullYear();
    const month = now.getMonth() + 1; // 월은 0부터 시작하므로 1을 더합니다.
    const day = now.getDate();
    const hours = now.getHours();
    const minutes = now.getMinutes();

    const session = window.sessionStorage
    const url = "http://221.156.60.18:8989/ping";
    const token = JSON.parse(sessionStorage.getItem("token"))

    const rendering = async () => {
      console.log("sessionStorage", sessionStorage)

      if (sessionStorage.length == 0) {
        router.push({name: "Sign In"})
      } else {
        console.log("token", token)
        let pingHeader = {
          headers : {
            "Authorization" : `Bearer ${token.token_data.accessToken}`,
            "Refresh-Token" : `Bearer ${token.token_data.refreshToken}`,
            "finance-agent" : "SAM9MO/0.0.1"
          }
        }

        console.log("pingHeader", pingHeader)
        const response = await axios.get(url, pingHeader).catch(() => null)

        const new_access_token = response.headers["new-access-token"]
        console.log("new_access_token", new_access_token)

        if (new_access_token != null) {
          token.token_data.accessToken = new_access_token
          sessionStorage.setItem("token", JSON.stringify(token))
        }
      }
    }

    rendering()

    const Alarm_All = async () => {
      const url = "http://221.156.60.18:9101/alarm"

      let favorite_stock = JSON.parse(session.getItem("favorite_stock"))
      // console.log("favorite_stock", favorite_stock.favorite_stock)
      favorite_stock = favorite_stock.favorite_stock
      // console.log("favorite_stock", favorite_stock)
      const response = await axios.get(url).catch(() => null)
      console.log("favorite_stock",favorite_stock)
      if (!response) return null

      const alarm_result = response.data
      //[Object.keys(favorite_stock[j])[0]].fluctuation)
      // console.log("주식등락률API",alarm_result)
      for (let i = 0; i < alarm_result.length; i++) {
        for (let j = 0; j < favorite_stock.length; j++) {
          if (alarm_result[i].stock_num === Object.keys(favorite_stock[j])[0] && favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation !== "") {
            if (favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation_toggle === "plus" && favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation >= alarm_result[i].percent_change) {
              document.getElementById("alarm").style.display = "block";//plus
              console.log("style", document.getElementById("alarm").style.display)
              stock_name.value = `종목명 ${favorite_stock[j][Object.keys(favorite_stock[j])[0]].name}`
              console.log("종목명", stock_name.value)
              time_now.value = `현재시간 : ${year}년 ${month}월 ${day}일 ${hours}시간 ${minutes}분`
              console.log("시간", time_now.value)
              stock_content.value = `주식상승률: ${favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation}`
              console.log("주식상승률", stock_content.value)
              setTimeout(3000)
            } else if (favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation_toggle === "minus" && favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation <= alarm_result[i].percent_change) {
              document.getElementById("alarm").style.display = "block";//minus
              stock_name.value = `종목명 ${favorite_stock[j][Object.keys(favorite_stock[j])[0]].name}`
              console.log("elseif종목명", stock_name.value)
              time_now.value = `현재시간 : ${year}년 ${month}월 ${day}일 ${hours}시간 ${minutes}분`
              console.log("시간", time_now.value)
              stock_content.value = `주식하락률: ${favorite_stock[j][Object.keys(favorite_stock[j])[0]].fluctuation}`
              console.log("주식하락률", stock_content.value)
            } else {
              continue //위 조건에 안맞으면 다음 조건으로 넘어가버림
            }
          } else {
            continue //위 조건에 안맞으면 다음 조건으로 넘어가버림
          }
        }
      }
    };

    // const Alarm= async () => {
    //
    // }


    let intervalId = null;

    onMounted(async () => {
      await Alarm_All;

      intervalId = setInterval(Alarm_All, 20000);
    });


    onBeforeUnmount(() => {
      clearInterval(intervalId);
    });

    return{
      stock_name,
      time_now,
      stock_content,
      close
    }

  },

  data() {
    return {
      title: "Vite Soft UI Dashboard",
      controls: "dashboardsExamples",
      isActive: "active",
    };
  },
  methods: {
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return routeArr[1];
    },
  },
};
</script>

<style scoped>

.nav-text {
  color: white !important;
}

.nav-text.active {
  color: black !important;
}

</style>



