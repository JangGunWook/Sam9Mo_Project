<template>
  <aside
      id="sidenav-main"
      class="my-3 overflow-auto border-0 sidenav navbar navbar-vertical navbar-expand-xs border-radius-xl shadow-sm"
      :class="$store.state.isRTL ? 'me-3 rotate-caret' : 'ms-3'"
      :data-color="sidenavActiveBgColors"
      style="background-color:#01275b !important;"
  >
    <div class="sidenav-header">
      <i
          id="iconSidenav"
          class="top-0 p-3 cursor-pointer fas fa-times text-secondary opacity-5 position-absolute end-0 d-none d-xl-none"
          aria-hidden="true"
      ></i>
      <a class="m-0 navbar-brand" href="/">
<!--        <img :src="logo" class="navbar-brand-img h-100" alt="main_logo" />-->
        <h4 class="ms-4 font-weight-bold pro-text" style="color: white">Sentimental Investment</h4>
      </a>
    </div>
    <hr class="mt-0 horizontal dark" />
    <sidenav-list :card-bg="customClass" />
  </aside>
</template>
<script>
import SidenavList from "./SidenavList.vue";
import logo from "@/assets/img/logo-ct.png";

export default {
  name: "IndexComponent",
  components: {
    SidenavList,
  },
  props: {
    customClass: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      logo,
      sidenavActiveBgColors: 'success'
    };
  },
};
</script>

<style scoped>

.navbar-brand span {
  color: white !important;
}
.pro-text{
  position: relative;
  right: 49px;
  font-size: 22px;
}
</style>
