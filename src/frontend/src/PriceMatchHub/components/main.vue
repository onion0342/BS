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
          <el-button type="primary" @click="search">搜索</el-button>
        </div>
      </div>
      <div class="user-center" @mouseover="showMenu = true" @mouseleave="showMenu = false">
        <img src="../assets/user_center.png" alt="User Center" @click="this.goToUserCenter" class="user-icon" />
        <div v-if="showMenu" class="dropdown-menu">
          <div class="dropdown-item" @click="this.goToUserCenter">个人中心</div>
          <div class="dropdown-item" @click="this.logout">登出</div>
        </div>
      </div>
    </div>
    <div class="results-container">
      <div v-for="item in searchResults" :key="item.id" class="product-card">
        <div class="product-image">
          <img :src="item.imageUrl" alt="Product Image" />
        </div>
        <div class="product-info">
          <h3>{{ item.name }}</h3>
          <p><strong>价格:</strong> ¥{{ item.price }}</p>
          <p><strong>价格更新时间:</strong> {{ formatDate(item.priceUpdateTime) }}</p>
          <p><strong>成交量:</strong> {{ item.salesVolume }}</p>
          <p><strong>店铺名:</strong> {{ item.storeName }}</p>
          <p><strong>店铺位置:</strong> {{ item.storeLocation }}</p>
          <p><strong>商品描述:</strong> {{ item.description }}</p>
        </div>
        <div class="product-actions">
          <el-button type="primary" @click="viewDetails(item)">查看详情</el-button>
          <el-button type="primary" @click="">订阅商品</el-button>
        </div>
      </div>
    </div>
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
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${('0' + (date.getMonth() + 1)).slice(-2)}-${('0' + date.getDate()).slice(-2)}`;
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
          clickURL: '',
        },
      ];
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
  width: calc(20% - 16px); /* 三列布局，减去gap */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}
 
.product-image img {
  width: 100%;
  height: auto;
  display: block;
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
</style>