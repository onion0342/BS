<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <div style="display: flex; align-items: center; margin-top: 20px; margin-left: 20px;">
      <img src="../assets/BSlogo.png" alt="Logo" class="circular-image" />
      <div style="font-size: 2em; font-weight: bold; margin-left: 10px;">
        PriceMatchHub
      </div>
    </div>
    <div style="width: 40%; margin: 0 auto; padding-top: 5vh">
      <div class="RegisterBox">

        <div style="margin-left: 10px; height: 180px ;text-align: start; font-size: 16px;">
          <div style=" height: 40px;margin: auto;display: flex;align-items: center;justify-content: center">
            <div style ="font-size: 1.5rem;font-weight: bolder; margin-top: 20px;text-align: center">
              用 户 注 册
            </div>
          </div>
          <el-divider/>
          <el-form label-position="right" label-width="100px" style=" font-weight: bolder; font-size: 10px">
            <el-form-item label="用户名"  style = "margin-top: 5px;">
              <el-input v-model="user_name" style="width: 22.5vw; margin-left: 1rem" maxlength="18" clearable
                        placeholder="输入用户名"/>
            </el-form-item>
            <el-form-item label="手机号"  style = "margin-top: 5px;">
              <el-input v-model="phone" style="width: 22.5vw; margin-left: 1rem" maxlength="18" clearable
                        placeholder="输入手机号"/>
            </el-form-item>
            <el-form-item label="邮箱"  style = "margin-top: 5px;">
              <el-input v-model="email" style="width: 18.5vw; margin-left: 1rem" maxlength="18" clearable
                        placeholder="输入邮箱"
                        @blur="emailConfirm()"/>
              <el-button type="primary"  @click="getCode()" style="margin-left: 1rem;">
                发送验证码
              </el-button>
            </el-form-item>
            <el-form-item label="密码" style = "margin-top: 5px;">
              <el-input v-model="password" style="width: 22.5vw; margin-left: 1rem" type="password" maxlength="20" clearable
                        placeholder="6到20位，只能由大小写字母和数字组成"/>
            </el-form-item>
            <el-form-item label="确认密码" style = "margin-top: 5px;">
              <el-input v-model="confirmPassword" style="width: 22.5vw; margin-left: 1rem" type="password" maxlength="20" clearable
                        placeholder="重复输入密码"/>
            </el-form-item>
            <el-form-item label="邮箱验证码" style = "margin-top: 5px;">
              <el-input v-model="code" style="width: 22.5vw; margin-left: 1rem" maxlength="20" clearable
                        placeholder="输入邮箱收到的验证码"/>
            </el-form-item>

            
            <div style="margin-top: 30px; display:flex;justify-content: center">
              <el-button type="primary"  @click="handle()">
                注册
              </el-button>
              <el-button  @click = "login">
                返回
              </el-button>
            </div>
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
  data() {
    return {
      user_name: "",
      password: "",
      email: "",
      phone: "",
      confirmPassword: "",
      pwd_hash: "",
      code: "",
    };
  },
  methods: {
    login(){
      window.location.href = "/login/user";
    },
    hash() {
      this.pwd_hash = this.$sha256(this.password)
    },
    getCode() {
      axios
        .post("http://127.0.0.1:8000/pricematchhub/email/confirm/", {
          email: this.email,
        })
        .then((response) => {
          console.log(response)
          if(response.data.code == 0) {
            ElMessage.success(response.data.msg)
          } else {
            ElMessage.error(response.data.err)
          }
        })
        .catch((error) => {
          ElMessage.error(error.response.data.err);
        })
    },
    check() {
      if(this.user_name == "") {
        ElMessage.error("未输入用户名")
        return false
      }
      if(this.phone == "") {
        ElMessage.error("未输入手机号")
        return false
      }
      if(this.email == "") {
        ElMessage.error("未输入邮箱")
        return false
      }
      if(this.password.length < 6 || this.password.length > 20) {
        ElMessage.error("密码格式错误，6到20位，只能由大小写字母和数字组成")
        return false
      }
      const passwordRegex = /^[A-Za-z0-9]+$/
      if (!passwordRegex.test(this.password)) {
        ElMessage.error("密码格式错误，只能由大小写字母和数字组成")
        return false
      }
      if(this.password == "") {
        ElMessage.error("未输入密码")
        return false
      }
      if(this.confirmPassword == "") {
        ElMessage.error("请重复密码")
        return false
      }
      if(this.confirmPassword != this.password) {
        ElMessage.error("前后输入密码不一致")
        return false
      }
      return true
    },
    handle() {
      if(!this.check())
        return
      this.hash()
      
      axios
        .post("http://127.0.0.1:8000/pricematchhub/user/add/", {
          user_name: this.user_name,
          phone: this.phone,
          email: this.email,
          pwd_hash: this.pwd_hash,
          code: this.code,
        })
        .then((response) => {
          console.log(response)
          if(response.data.code == 0) {
            ElMessage.success(response.data.msg)
            window.location.href = "/login/user";
          } else {
            ElMessage.error(response.data.err)
          }
        })
        .catch((error) => {
          ElMessage.error(error.response.data.err);
        });
    },
    emailConfirm() {
      const reg = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/
      let str = this.email
      if(reg.test(str)) {
        
      } else {
        ElMessage.error("邮箱格式错误")
      }
    },
  },
  mounted() {

  },
};
</script>
  
  <style scoped>
.RegisterBox {
  height: 500px;
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