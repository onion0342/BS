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
        <img src="../assets/user_center.png" alt="User Center" @click="goToUserCenter" class="user-icon" />
        <div v-if="showMenu" class="dropdown-menu">
          <div class="dropdown-item" @click="goToUserCenter">个人中心</div>
          <div class="dropdown-item" @click="logout">登出</div>
        </div>
      </div>
    </div>
    <div class="results-container">
        
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
    };
  },
  methods: {
    goToUserCenter() {
      this.showMenu = false
      window.location.href = "/"
      
    },
    logout() {

      this.showMenu = false
      window.location.href = "/"
    },
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
  flex: 2;
  padding: 20px;
  overflow-y: auto;
  background-color: #ffffff;
}
 
.circular-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
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