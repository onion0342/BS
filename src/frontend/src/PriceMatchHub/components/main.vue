<template>
  <el-scrollbar style="width: 100%; height: 100%">
    <div style="display: flex; align-items: center; margin-top: 20px; margin-left: 20px;">
      <img src="../assets/BSlogo.png" alt="Logo" class="circular-image" />
      <div style="font-size: 2em; font-weight: bold; margin-left: 10px;">
        PriceMatchHub
      </div>
    </div>
    <div style="width: 50%; margin: 0 auto;">
      <div class="searchBox">
        <div style="margin-left: 10px; text-align: start; font-size: 16px;">
          <el-form label-position="right" label-width="100px" style=" font-weight: bolder; font-size: 10px">
            <el-form-item label="" style = "margin-top: 20px;">
              <el-input v-model="query" style="width: 30vw; margin-left: 1rem" maxlength="20" clearable/>
            </el-form-item>
          </el-form>
        </div>

      </div>
    </div>
  </el-scrollbar>
</template>
<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  computed: {

  },
  data() {
    return {
      query: "",
    }
  },
  methods: {
  },
  mounted() {
  },
};
</script>

<style scoped>
.searchBox {
  height: 100px;
  width: 800px;
  margin-top: 0px;
  margin-left: 0px;
  margin-right:0px;
  padding: 0px;
  padding-right: 0px;
  padding-top: 0px;
  text-align: center;
  border: 2px solid #ADD8E6;
}

.circular-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 0px;
}
</style>