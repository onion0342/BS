<template>
  <el-scrollbar style="width: 100%; height: 100%">
    <div style="display: flex; align-items: center; margin-top: 20px; margin-left: 20px;">
      <img src="../assets/BSlogo.png" alt="Logo" class="circular-image" />
      <div style="font-size: 2em; font-weight: bold; margin-left: 10px;">
        PriceMatchHub
      </div>
    </div>
    <div style="width: 40%; margin: 0 auto; padding-top: 5vh">
      <div class="loginBox">
        <div style="margin-left: 10px; text-align: start; font-size: 16px;">
          <div style=" height: 40px; margin: auto; display: flex; align-items: center; justify-content: center">
            <div style ="font-size: 1.5rem;font-weight: bolder; margin-top: 20px; text-align: center">
              用 户 登 录
            </div>
          </div>
          <el-divider/>
          <el-form label-position="right" label-width="100px" style=" font-weight: bolder; font-size: 10px">
            <el-form-item label="账号"  style = "margin-top: 20px;">
              <el-input v-model="account" style="width: 22.5vw; margin-left: 1rem" maxlength="50" clearable
                        placeholder="输入用户名 / 手机号 / 邮箱"/>
            </el-form-item>
            <el-form-item label="密码" style = "margin-top: 20px;">
              <el-input v-model="password" style="width: 22.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
            </el-form-item>
          </el-form>
        </div>

        <div style="margin-top: 30px; display:flex;justify-content: center">
          <el-button type="primary"  @click="handle()">
            登录
          </el-button>
          <el-button :icon="Edit" @click = "signup">
            注册新用户
          </el-button>
        </div>

      </div>
    </div>
  </el-scrollbar>
</template>
<script>
import axios from "axios";
import { ElMessage } from "element-plus";
import { Edit } from "@element-plus/icons-vue";

export default {
  computed: {
    Edit() {
      return Edit
    }
  },
  data() {
    return {
      account: "",
      password: "",
      pwd_hash: "",
    };
  },
  methods: {
    signup(){
      window.location.href = "/login/signup"
    },
    check() {
      if(this.account == "") {
        ElMessage.error("未输入用户名 / 手机号 / 邮箱")
        return false
      }
      if(this.password == "") {
        ElMessage.error("未输入密码")
        return false
      }
      return true
    },
    hash() {
      this.pwd_hash = this.$sha256(this.password)
    },
    handle() {
      if(!this.check())
        return
      this.hash()
      axios
        .post("http://127.0.0.1:8000/pricematchhub/user/login/", {
          account: this.account,
          pwd_hash: this.pwd_hash,
        })
        .then((response) => {
          //console.log(response)
          if(response.data.code == 0) {
            ElMessage.success(response.data.msg)
            window.location.href =
              "/PriceMatchHub?user_id=" + response.data.payload.user_id;
          } else {
            ElMessage.error(response.data.err)
          }
        })
        .catch((error) => {
          ElMessage.error(error.response.data.err);
        })
    },
  },
  mounted() {
  },
};
</script>

<style scoped>
.loginBox {
  height: 300px;
  width: 600px;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}

.circular-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 0px;
}
</style>