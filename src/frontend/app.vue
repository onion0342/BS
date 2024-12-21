<template>
  <div class="main">
    <el-container>
      <el-container>
        <el-header style="height: 0vh"></el-header>
        <el-main style="height: 100%; width: 100%">
          <el-scrollbar height="100%">
            <RouterView
              class="content"
              style="
                height: 100vh;
                max-height: 100%;
                background-color: white;
                color: black;
              "
            />
          </el-scrollbar>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { Link } from "@element-plus/icons-vue";

export default {
  methods: {},
};
</script>

<style scoped>
#app {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #dcdcdc;
  width: 99vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 99vw;
  height: 100vh;
  background-color: #dcdcdc;
}

.title {
  background-color: #ffffff;
  height: 60px;
}

.aside {
  min-height: 100vh;
  width: 200px;
  background-color: black;
}
</style>
