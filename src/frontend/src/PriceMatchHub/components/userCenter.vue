<template>
    <el-scrollbar style="width: 100%; height: 100%">
        <div class="header">
            <div class="logo-and-title">
                <img src="../assets/BSlogo.png" alt="Logo" class="circular-image" @click="goToMain" />
                <div class="title">PriceMatchHub</div>
            </div>
        </div>
        <div class="user-info-container">
            <div class="user-info-box">
                <div class="user-info">
                    <strong>用户名:</strong> {{ user_info.user_name }}
                    <el-button class="info-button" @click="">更改密码</el-button>
                </div>
                <div class="user-info">
                    <strong>邮箱:</strong> {{ user_info.email }}
                    <el-button class="info-button" @click="">绑定邮箱</el-button>
                </div>
                <div class="user-info">
                    <strong>手机号:</strong> {{ user_info.phone }}
                    <el-button class="info-button" @click="">更改手机号</el-button>
                </div>
                <div class="user-info">
                    <strong>绑定淘宝账号:</strong> {{ user_info.taobao_account }}
                </div>
                <div class="user-info">
                    <strong>绑定淘宝密码:</strong> {{ user_info.taobao_password }}
                    <el-button class="info-button" @click="this.isDisplayTaobaoBox = true">绑定淘宝</el-button>
                </div>
                <div class="user-info">
                    <strong>绑定京东账号:</strong> {{ user_info.jingdong_account }}
                </div>
                <div class="user-info">
                    <strong>绑定京东密码:</strong> {{ user_info.jingdong_password }}
                    <el-button class="info-button" @click="this.isDisplayJingdongBox= true">绑定京东</el-button>
                </div>
            </div>
        </div>

        <el-dialog v-model="isDisplayTaobaoBox" :title="'绑定淘宝账号'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                账号:
                <el-input v-model="this.taobao.account" style="width: 15vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码:
                <el-input v-model="this.taobao.password" style="width: 15vw;" clearable />
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleTaobao">确认</el-button>
                    <el-button @click="isDisplayTaobaoBox = false">取消</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isDisplayJingdongBox" :title="'绑定京东账号'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                账号:
                <el-input v-model="this.jingdong.account" style="width: 15vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码:
                <el-input v-model="this.jingdong.password" style="width: 15vw;" clearable />
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleJingdong">确认</el-button>
                    <el-button @click="isDisplayJingdongBox = false">取消</el-button>
                </span>
            </template>
        </el-dialog>
    </el-scrollbar> 
</template>
  
<script>
import axios from "axios";
import { ElMessage, ElMessageBox } from "element-plus";
  
export default {
    data() {
      return {
        user_id: 0,
        user_info: {
          user_name: '',
          email: '',
          phone: '',
          taobao_account: '',
          taobao_password: '',
          jingdong_account: '',
          jingdong_password: '',
        },
        isDisplayTaobaoBox: false,
        isDisplayJingdongBox: false,
        taobao: {
            account: '',
            password: '',
        },
        jingdong: {
            account: '',
            password: '',
        },
      };
    },
    methods: {
      goToMain() {
        window.location.href = "/PriceMatchHub/main?user_id=" + this.user_id;
      },
      getDataFromURL() {
        const url = new URL(window.location);
        const params = new URLSearchParams(url.search);
        this.user_id = params.get('user_id');
        this.fetchUserInfo();
      },
      fetchUserInfo() {
        axios
            .post("http://127.0.0.1:8000/pricematchhub/user/get/", {
                user_id: this.user_id
            })
            .then((response) => {
                if(response.data.code == 0) {
                    this.user_info.user_name = response.data.payload.user_name
                    this.user_info.email = response.data.payload.email
                    this.user_info.phone = response.data.payload.phone
                    this.user_info.taobao_account = response.data.payload.taobao_account
                    this.user_info.taobao_password = response.data.payload.taobao_password
                    this.user_info.jingdong_account = response.data.payload.jingdong_account
                    this.user_info.jingdong_password = response.data.payload.jingdong_password
                } else {
                    ElMessage.error(response.data.err)
                }
            })
            .catch((error) => {
                ElMessage.error(error.response.data.err);
            })
      },
      handleTaobao() {
        axios
            .post("http://127.0.0.1:8000/pricematchhub/user/taobao/set", {
                user_id: this.user_id,
                account: this.taobao.account,
                password: this.taobao.password,
            })
            .then((response) => {
                if(response.data.code == 0) {
                    this.fetchUserInfo()
                    this.isDisplayTaobaoBox = false
                    ElMessage.success(response.data.msg)
                } else {
                    ElMessage.error(response.data.err)
                }
            })
            .catch((error) => {
                ElMessage.error(error.response.data.err);
            })
      },
      handleJingdong() {
        axios
            .post("http://127.0.0.1:8000/pricematchhub/user/jingdong/set", {
                user_id: this.user_id,
                account: this.jingdong.account,
                password: this.jingdong.password,
            })
            .then((response) => {
                if(response.data.code == 0) {
                    this.fetchUserInfo()
                    this.isDisplayJingdongBox = false
                    ElMessage.success(response.data.msg)
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
      this.getDataFromURL()
      this.fetchUserInfo()
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
    border-bottom: 1px solid #dddddd;
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

.right-button {
    padding-left: auto;
    border: none;
    background-color: transparent;
    cursor: pointer;
}

.user-info-container {
    display: flex;
    justify-content: center;
    padding-top: 20px;
    width: 100%;
}
 
.user-info-box {
    background-color: #f9f9f9;
    padding: 20px;
    border: 1px solid #dddddd;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 700px;
}
 
.user-info {
    justify-content: space-between;
    width: 100%;
    margin-bottom: 20px;
    position: relative;
}
 
.info-button {
    padding: 5px 10px;
    font-size: 14px;
    cursor: pointer;
    border: 1px solid #dddddd;
    border-radius: 4px;
    background-color: #ffffff;
    transition: background-color 0.3s, border-color 0.3s;
    position: absolute;
    right: 0;
}
 
.info-button:hover {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
  
.circular-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

</style>