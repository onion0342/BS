<template>
  <el-scrollbar style="width: 100%; height: 100%">
    <div class="header">
      <div class="logo-and-title">
        <img src="../assets/BSlogo.png" alt="Logo" class="circular-image" />
        <div class="title">PriceMatchHub</div>
      </div>
      <div class="search-section">
        <div class="search-box-wrapper">
          <el-input v-model="query" placeholder="搜索你感兴趣的商品..." class="search-input" maxlength="20" clearable />
          <span class="search-input-spacer"></span>
          <el-button type="primary" @click="this.search">搜索</el-button>
        </div>
      </div>
      <!-- 获取订阅列表按钮 -->
      <img src="../assets/sort.png" alt="Search" @click="this.isDisplaySortBox = true" class="sort-icon" />
      <div class="user-center" @mouseover="showMenu = true" @mouseleave="showMenu = false">
        <img src="../assets/user_center.png" alt="User Center" @click="this.goToUserCenter" class="user-icon" />
        <div v-if="showMenu" class="dropdown-menu">
          <div class="dropdown-item" @click="this.goToUserCenter">个人中心</div>
          <div class="dropdown-item" @click="this.logout">登出</div>
        </div>
      </div>
    </div>
    <div class="results-container" ref="container">
      <div v-for="item in searchResults" :key="item.id" class="product-card" ref="cards">
        <div class="product-image">
          <img :src="item.imageUrl" alt="Product Image" />
        </div>
        <div class="product-info">
          <h3>{{ cleanSpanTags(item.name) }}</h3>
          <p><strong>价格:</strong> <span class="price">{{ item.price }}</span></p>
          <p><strong>价格更新时间:</strong> {{ formatDate(item.priceUpdateTime) }}</p>
          <p><strong>平台:</strong> {{ item.platform }}</p>
          <p><strong>成交量:</strong> {{ item.salesVolume }}</p>
          <p><strong>店铺名:</strong> {{ item.storeName }}</p>
          <p><strong>店铺位置:</strong> {{ item.storeLocation }}</p>
          <p v-if="item.description !== 'none'"><strong>商品描述:</strong> {{ item.description }}</p>
        </div>
        <div class="product-actions">
          <el-button type="primary" @click="openDetailsPage(item.clickUrl)">查看详情</el-button>
          <el-button type="primary" @click="subPruduct(item.id)">订阅商品</el-button>
        </div>
      </div>
    </div>

    <el-dialog v-model="isDisplaySortBox" :title="'商品排序'" width="30%" align-center>
      <div class="sort-box">
        <div class="price-sort">
          <label for="minPrice">最低价格:</label>
          <el-input-number v-model="sort.minPrice" :min="0" placeholder="请输入最低价格" id="minPrice" class="price-input"></el-input-number>
          <!--<el-slider v-model="sort.minPrice" :min="0" :max="1000" @change="updateMinPrice" class="price-slider"></el-slider>-->
        </div>
        <div class="price-sort">
          <label for="maxPrice">最高价格:</label>
          <el-input-number v-model="sort.maxPrice" :min="0" placeholder="请输入最高价格" id="maxPrice" class="price-input"></el-input-number>
          <!--<el-slider v-model="sort.maxPrice" :min="0" :max="1000" @change="updateMaxPrice" class="price-slider"></el-slider>-->
        </div>
        <div class="price-sort">
          <label>排序顺序:</label>
          <el-select v-model="sort.order" placeholder="请选择排序顺序">
            <el-option label="升序" value="asc"></el-option>
            <el-option label="降序" value="desc"></el-option>
          </el-select>
        </div>
      </div>
 
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="this.resetSort">重置</el-button>
          <el-button @click="this.handleSort">确认</el-button>
          <el-button @click="this.isDisplaySortBox = false">取消</el-button>
        </span>
      </template>
    </el-dialog>

  </el-scrollbar>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      user_id: 0,
      query: "",
      showMenu: false,
      searchResults: [],
      copySearchResults: [],
      isDisplaySortBox: false,
      sort: {
        minPrice: 0,
        maxPrice: 1000,
        order: 'asc',
      },
    };
  },
  methods: {
    goToUserCenter() {
      this.showMenu = false
      window.location.href = 
        "/PriceMatchHub/usercenter?user_id=" + this.user_id
    },
    logout() {
      this.showMenu = false
      window.location.href =
        "/login"
    },
    getDataFromURL() {
      const url = new URL(window.location)
      const params = new URLSearchParams(url.search)
      this.user_id = params.get('user_id')
    },
    getDataFromTaobao(key) {

    },
    getDataFromJingdong(key) {

    },
    search() {
      this.getDataFromTaobao(this.query)
      this.getDataFromJingdong(this.query)
      this.getProducts(this.query)
    },
    getProducts(key) {
      axios
        .post("http://127.0.0.1:8000/pricematchhub/get/products", {
          key: key,
        })
        .then((response) => {
          if(response.data.code == 0) {
            this.searchResults = response.data.payloads
            this.copySearchResults = this.searchResults.slice()
            this.handleSort()
            ElMessage.success(response.data.msg)
          } else {
            ElMessage.error(response.data.err)
          }
        })
        .catch((error) => {
          ElMessage.error(error.response.data.err)
        })
    },
    cleanSpanTags(text) {
      return text.replace(/<span[^>]*>(.*?)<\/span>/gi, '')
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return `${date.getFullYear()}-${('0' + (date.getMonth() + 1)).slice(-2)}-${('0' + date.getDate()).slice(-2)}`
    },
    openDetailsPage(url) {
      window.open(url, '_blank')
    },
    updateMinPrice(value) {
      this.sort.minPrice = parseFloat(value.toFixed(2))
    },
    updateMaxPrice(value) {
      this.sort.maxPrice = parseFloat(value.toFixed(2))
    },
    handleSort() {
      let filteredResults = this.copySearchResults.filter(item => {
        return item.price >= this.sort.minPrice && item.price <= this.sort.maxPrice
      })
      if (this.sort.order === 'desc') {
        filteredResults.sort((a, b) => b.price - a.price);
      } else {
        filteredResults.sort((a, b) => a.price - b.price);
      }
      this.searchResults = filteredResults;
      this.isDisplaySortBox = false
    },
    resetSort() {
      this.sort.minPrice = 0
      this.sort.maxPrice = 1000
      this.sort.order = 'asc'
      this.handleSort()
      this.isDisplaySortBox = false
    },
    subPruduct(id) {

    },
  },
  mounted() {
    this.getDataFromURL()
    this.searchResults = [
        {
          id: 1,
          name: '商品名称1',
          price: 100.00,
          priceUpdateTime: '2023-10-01T12:00:00Z',
          salesVolume: '>=100',
          storeName: '店铺名1',
          storeLocation: '位置1',
          description: '商品描述1',
          imageUrl: 'http://g.search3.alicdn.com/img/i3/2211812908957/O1CN01CD6NL52G2MYZqo5sn_!!2211812908957-0-alimamacc.jpg',
          clickUrl: '',
          platform: '',
        },
      ];
    this.getProducts('')
  },
};
</script>
 
<style scoped>
 
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #ddd;
}
 
.logo-and-title {
  display: flex;
  align-items: center;
}
 
.title {
  font-size: 1.5em;
  font-weight: bold;
  margin-left: 10px;
}
 
.user-center {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-left: auto;
  padding-right: 20px;
}
 
.user-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  transition: transform 0.3s ease, filter 0.3s ease;
}

.user-icon:hover {
  transform: scale(1.1);
  filter: brightness(1.2);
}

.sort-icon {
  width: 40px;
  height: 40px;
  transition: transform 0.3s ease, filter 0.3s ease;
}

.sort-icon:hover {
  transform: scale(1.1);
  filter: brightness(1.2);
}
 
.search-section {
  flex: 1;
  display: flex;
  padding-left: 10%;
  align-items: center;
  background-color: #ffffff;
}
  
.search-box-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 800px;
}
 
.search-input {
  flex: 1;
  padding: 10px;
  font-size: 1em;
  background-color: #ffffff;
}
 
.search-input-spacer {
  width: 10px;
}
 
.el-button {
  padding: 10px 20px;
  font-size: 1em;
  border: none;
  border-radius: 4px 4px 4px 4px;
  background-color: #409eff;
  color: #ffffff;
}
 
.results-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px;
}
 
.product-card {
  width: calc(20% - 16px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: visible;
  height: 100%;
  transition: transform 0.3s ease;
  position: relative;
}

.product-card:hover {
  transform: scale(1.05);
}

.product-image {
  overflow: visible;
  position: relative;
}
 
.product-image img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease, filter 0.3s ease;
  z-index: 1;
}

.product-card:hover .product-image img {
  transform: scale(1.05) translateY(-7%);
  filter: brightness(1.05);
  transform-origin: bottom;
  z-index: 2;
}
 
.product-info {
  padding: 16px;
}
 
.product-info p {
  margin: 8px 0;
}
 
.product-actions {
  display: flex;
  justify-content: flex-end;
  padding: 8px;
  background-color: #f5f5f5;
}
 
.product-actions .el-button {
  margin-left: 8px;
}

.circular-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  transition: transform 0.3s ease, filter 0.3s ease;
  cursor: pointer;
}

.circular-image:hover {
  transform: scale(1.1);
  filter: brightness(1.2);
}

.dropdown-menu {
  position: absolute;
  width: 100px;
  top: 100%;
  right: 0;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.dropdown-item {
  padding: 10px;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  color: #000000;
}

.dropdown-item:hover {
  background-color: #f0f0f0;
  color: #ffa500;
}
 
.dropdown-menu-enter-active, .dropdown-menu-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.dropdown-menu-enter, .dropdown-menu-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.price {
  color: rgb(35, 62, 240);
  font-size: 1.5em;
}

.sort-box {
  padding: 10px;
}

.el-select {
  width: 50%;
  margin-left: 10px;
}

.el-input-number {
  margin-left: 10px;
}

.price-sort {
  margin-top: 10px;
}
</style>