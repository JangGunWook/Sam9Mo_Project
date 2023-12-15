<template>
  <div class="card mb-4">
    <div class="card-header pb-0">
      <h5>뉴스</h5>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">

        <div class="container-fluid">
          <button type="button" class="btn btn-primary btn-sm" style="margin-right: 10px;">전체</button>
          <button type="button" class="btn btn-secondary btn-sm" style="margin-right: 10px;">정치</button>
          <button type="button" class="btn btn-secondary btn-sm" style="margin-right: 10px;">사회</button>
          <button type="button" class="btn btn-secondary btn-sm" style="margin-right: 10px;">경제</button>
          <div class="row">
            <div class="col">
              <div class="align-items-center mb-0">
                <div>
                  <td v-for="index in 5" :key="index"
                      @mouseenter="handleHover(index)"
                      @mouseleave="handleHover(null)"
                      class="hover:bg-gray-200">
                  </td>
                </div>
                <td v-for="category in categories"
                    :key="category.id"
                    class="px-6 py-4 text-lg text-gray-700 border-b"
                    @click="handleClick(index, category.id)"
                    :class="{ 'bg-gray-200': index === selectedRowIndex && category.id === selectedCategoryId }">
                  <!-- <h6>{{ category.name }}</h6>-->
                </td>



              </div>
            </div>
          </div>
        </div>
        <tbody>
        <tr>
          <td>
            <div class="d-flex px-2 py-1">

              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">John Michael</h6>
                <p class="text-xs text-secondary mb-0">john@creative-tim.com</p>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">Manager</p>
            <p class="text-xs text-secondary mb-0">Organization</p>
          </td>
          <td class="align-middle text-center text-sm">
            <vsud-badge color="success" variant="gradient" size="sm">Online</vsud-badge>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">23/04/18</span>
          </td>
          <td class="align-middle">
            <a
                href="javascript:;"
                class="text-secondary font-weight-bold text-xs"
                data-toggle="tooltip"
                data-original-title="Edit user"
            >Edit</a>
          </td>
        </tr>
        <tr>
          <td>
            <div class="d-flex px-2 py-1">

              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">Alexa Liras</h6>
                <p class="text-xs text-secondary mb-0">alexa@creative-tim.com</p>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">Programator</p>
            <p class="text-xs text-secondary mb-0">Developer</p>
          </td>
          <td class="align-middle text-center text-sm">
            <vsud-badge color="secondary" variant="gradient" size="sm">Offline</vsud-badge>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">11/01/19</span>
          </td>
          <td class="align-middle">
            <a
                href="javascript:;"
                class="text-secondary font-weight-bold text-xs"
                data-toggle="tooltip"
                data-original-title="Edit user"
            >Edit</a>
          </td>
        </tr>
        <tr>
          <td>
            <div class="d-flex px-2 py-1">

              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">Laurent Perrier</h6>
                <p class="text-xs text-secondary mb-0">laurent@creative-tim.com</p>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">Executive</p>
            <p class="text-xs text-secondary mb-0">Projects</p>
          </td>
          <td class="align-middle text-center text-sm">
            <vsud-badge color="success" variant="gradient" size="sm">Online</vsud-badge>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">19/09/17</span>
          </td>
          <td class="align-middle">
            <a
                href="javascript:;"
                class="text-secondary font-weight-bold text-xs"
                data-toggle="tooltip"
                data-original-title="Edit user"
            >Edit</a>
          </td>
        </tr>
        <tr>
          <td>
            <div class="d-flex px-2 py-1">

              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">Michael Levi</h6>
                <p class="text-xs text-secondary mb-0">michael@creative-tim.com</p>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">Programator</p>
            <p class="text-xs text-secondary mb-0">Developer</p>
          </td>
          <td class="align-middle text-center text-sm">
            <vsud-badge color="success" variant="gradient" size="sm">Online</vsud-badge>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">24/12/08</span>
          </td>
          <td class="align-middle">
            <a
                href="javascript:;"
                class="text-secondary font-weight-bold text-xs"
                data-toggle="tooltip"
                data-original-title="Edit user"
            >Edit</a>
          </td>
        </tr>
        <tr>
          <td>
            <div class="d-flex px-2 py-1">

              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">Richard Gran</h6>
                <p class="text-xs text-secondary mb-0">richard@creative-tim.com</p>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">Manager</p>
            <p class="text-xs text-secondary mb-0">Executive</p>
          </td>
          <td class="align-middle text-center text-sm">
            <vsud-badge color="secondary" variant="gradient" size="sm">Offline</vsud-badge>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">04/10/21</span>
          </td>
          <td class="align-middle">
            <a
                href="javascript:;"
                class="text-secondary font-weight-bold text-xs"
                data-toggle="tooltip"
                data-original-title="Edit user"
            >Edit</a>
          </td>
        </tr>
        <tr>
          <td>
            <div class="d-flex px-2 py-1">

              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">Miriam Eric</h6>
                <p class="text-xs text-secondary mb-0">miriam@creative-tim.com</p>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">Programtor</p>
            <p class="text-xs text-secondary mb-0">Developer</p>
          </td>
          <td class="align-middle text-center text-sm">
            <vsud-badge color="secondary" variant="gradient" size="sm">Offline</vsud-badge>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">14/09/20</span>
          </td>
          <td class="align-middle">
            <a
                href="javascript:;"
                class="text-secondary font-weight-bold text-xs"
                data-toggle="tooltip"
                data-original-title="Edit user"
            >Edit</a>
          </td>
        </tr>
        </tbody>
      </div>
    </div>
  </div>
</template>

<script>
import img1 from "../../assets/img/team-2.jpg";
import img2 from "../../assets/img/team-3.jpg";
import img3 from "../../assets/img/team-4.jpg";
import img4 from "../../assets/img/team-3.jpg";
import img5 from "../../assets/img/team-2.jpg";
import img6 from "../../assets/img/team-4.jpg";

export default {

  data() {
    return {
      selectedRowIndex: null,
      selectedCategoryId: null,
      categories: [
        {id: 1, name: ""},
        {id: 2, name: ""},
        {id: 3, name: ""},
      ],
      img1,
      img2,
      img3,
      img4,
      img5,
      img6,
    };
  },
  methods: {
    handleHover(index) {
      this.selectedRowIndex = index;
    },
    handleClick(rowIndex, categoryId) {
      this.selectedRowIndex = rowIndex;
      this.selectedCategoryId = categoryId;
    },
  },
};
</script>

