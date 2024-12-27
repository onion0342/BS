<template>
    <el-scrollbar style="width: 100%; height: 100%">
        <div class="header">
            <div class="logo-and-title">
                <img src="../assets/BSlogo.png" alt="Logo" class="circular-image" @click="this.goToMain" />
                <div class="title">PriceMatchHub</div>
            </div>
            <img src="../assets/backToMain.png" @click="this.goToMain" class="back-icon" />
        </div>
        <div class="user-info-container">
            <div class="user-info-box">
                <div class="user-info">
                    <strong>用户名:</strong> {{ user_info.user_name }}
                    <el-button class="info-button" @click="this.isDisplayPwdChangeBox = true">更改密码</el-button>
                </div>
                <div class="user-info">
                    <strong>邮箱:</strong> {{ user_info.email }}
                    <el-button class="info-button" @click="this.isDisplayEmailChangeBox = true">绑定邮箱</el-button>
                </div>
                <div class="user-info">
                    <strong>手机号:</strong> {{ user_info.phone }}
                    <el-button class="info-button" @click="this.isDisplayPhoneChangeBox = true">更改手机号</el-button>
                </div>
                <div class="user-info">
                    <strong>京东使用微信二维码扫描登录，微信请绑定京东账号</strong>
                </div>
                <div class="user-info">
                    <strong>唯品会使用微信二维码扫描登录，微信请绑定唯品会账号</strong>
                </div>
                <!--
                <div class="user-info">
                    <strong>绑定唯品会账号:</strong> {{ user_info.weipinhui_account }}
                </div>
                <div class="user-info">
                    <strong>绑定唯品会密码:</strong> {{ user_info.weipinhui_password }}
                    <el-button class="info-button" @click="this.isDisplayTaobaoBox = true">绑定唯品会</el-button>
                </div>
                <div class="user-info">
                    <strong>绑定京东账号:</strong> {{ user_info.jingdong_account }}
                </div>
                <div class="user-info">
                    <strong>绑定京东密码:</strong> {{ user_info.jingdong_password }}
                    <el-button class="info-button" @click="this.isDisplayJingdongBox= true">绑定京东</el-button>
                </div>
                -->
            </div>
        </div>
        
        <el-dialog v-model="isDisplayPwdChangeBox" :title="'更改密码'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                原密码:
                <el-input v-model="this.pwdChange.originPwd" style="width: 15vw;" type="password" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                新密码:
                <el-input v-model="this.pwdChange.newPwd" style="width: 15vw;" type="password" clearable />
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handlePwdChange">确认</el-button>
                    <el-button @click="isDisplayPwdChangeBox = false;
                                       this.pwdChange.originPwd = '';
                                       this.pwdChange.newPwd = '';">
                        取消
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isDisplayEmailChangeBox" :title="'修改绑定邮箱'" width="30%"
            align-center>
            <div style="display: flex; align-items: center; margin-left: 2vw; margin-top: 20px;">
                <span style="font-weight: bold; font-size: 1rem;">新邮箱:</span>
                <el-input v-model="emailChange.newEmail" style="width: 13vw; margin-left: 1rem;" clearable />
                <el-button type="primary" @click="this.getCode()" style="margin-left: 1rem;">发送验证码</el-button>
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                验证码:
                <el-input v-model="this.emailChange.code" style="width: 15vw;" clearable />
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleEmailChange">确认</el-button>
                    <el-button @click="isDisplayEmailChangeBox = false;
                                       this.emailChange.newEmail = '';
                                       this.emailChange.code = '';">
                        取消
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isDisplayPhoneChangeBox" :title="'修改绑定手机号'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                新手机号:
                <el-input v-model="this.phoneChange.newPhone" style="width: 15vw;" clearable />
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handlePhoneChange">确认</el-button>
                    <el-button @click="isDisplayPhoneChangeBox = false;
                                       this.phoneChange.newPhone = '';">
                        取消
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isDisplayTaobaoBox" :title="'绑定淘宝账号'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                账号:
                <el-input v-model="this.weipinhui.account" style="width: 15vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码:
                <el-input v-model="this.weipinhui.password" style="width: 15vw;" clearable />
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleTaobao">确认</el-button>
                    <el-button @click="isDisplayTaobaoBox = false;
                                       this.weipinhui.account = '';
                                       this.weipinhui.password = '';">
                        取消
                    </el-button>
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
                    <el-button @click="isDisplayJingdongBox = false;
                                       this.jingdong.account = '';
                                       this.jingdong.password = '';">
                        取消
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </el-scrollbar>
</template>
  
<script>
import axios from "axios";
import { ElMessage, ElMessageBox } from "element-plus";
import { resolveTransitionHooks } from "vue";
  
export default {
    data() {
      return {
        user_id: 0,
        user_info: {
          user_name: '',
          email: '',
          phone: '',
          weipinhui_account: '',
          weipinhui_password: '',
          jingdong_account: '',
          jingdong_password: '',
        },
        isDisplayTaobaoBox: false,
        isDisplayJingdongBox: false,
        isDisplayPwdChangeBox: false,
        isDisplayEmailChangeBox: false,
        isDisplayPhoneChangeBox: false,
        pwdChange: {
            originPwd: '',
            newPwd: '',
        },
        emailChange: {
            newEmail: '',
            code: '',
        },
        phoneChange: {
            newPhone: '',
        },
        weipinhui: {
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
        getCode() {
            axios
                .post("http://127.0.0.1:8000/pricematchhub/email/confirm/", {
                    email: this.emailChange.newEmail,
                })
                .then((response) => {
                //console.log(response)
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
                        this.user_info.weipinhui_account = response.data.payload.weipinhui_account
                        this.user_info.weipinhui_password = response.data.payload.weipinhui_password
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
        hash(pwd) {
            return this.$sha256(pwd)
        },
        handlePwdChange() {
            const originPwdHash = this.hash(this.pwdChange.originPwd)
            const newPwdHash = this.hash(this.pwdChange.newPwd)
            axios
                .post("http://127.0.0.1:8000/pricematchhub/user/password/change", {
                    user_id: this.user_id,
                    originPwdHash: originPwdHash,
                    newPwdHash: newPwdHash,
                })
                .then((response) => {
                    if(response.data.code == 0) {
                        this.isDisplayPwdChangeBox = false
                        this.pwdChange.originPwd = ""
                        this.pwdChange.newPwd = ""
                        ElMessage.success(response.data.msg)
                    } else {
                        ElMessage.error(response.data.err)
                    }
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.err);
                })
        },
        handlePhoneChange() {
            axios
                .post("http://127.0.0.1:8000/pricematchhub/user/phone/change", {
                    user_id: this.user_id,
                    newPhone: this.phoneChange.newPhone
                })
                .then((response) => {
                    if(response.data.code == 0) {
                        this.isDisplayPhoneChangeBox = false
                        this.phoneChange.newPhone = ""
                        this.fetchUserInfo()
                        ElMessage.success(response.data.msg)
                    } else {
                        ElMessage.error(response.data.err)
                    }
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.err);
                })
        },
        handleEmailChange() {
            axios
                .post("http://127.0.0.1:8000/pricematchhub/user/email/change", {
                    user_id: this.user_id,
                    newEmail: this.emailChange.newEmail,
                    code: this.emailChange.code
                })
                .then((response) => {
                    if(response.data.code == 0) {
                        this.isDisplayEmailChangeBox = false
                        this.emailChange.newEmail = ""
                        this.emailChange.code = ""
                        this.fetchUserInfo()
                        ElMessage.success(response.data.msg)
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
                .post("http://127.0.0.1:8000/pricematchhub/user/weipinhui/set", {
                    user_id: this.user_id,
                    account: this.weipinhui.account,
                    password: this.weipinhui.password,
                })
                .then((response) => {
                    if(response.data.code == 0) {
                        this.fetchUserInfo()
                        this.isDisplayTaobaoBox = false
                        this.weipinhui.account = ""
                        this.weipinhui.password = ""
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
                        this.jingdong.account = ""
                        this.jingdong.password = ""
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
    transition: transform 0.3s ease, filter 0.3s ease;
    cursor: pointer;
}
 
.circular-image:hover {
    transform: scale(1.1);
    filter: brightness(1.2);
}

.back-icon {
    width: 30px;
    height: 30px;
    transition: transform 0.3s ease, filter 0.3s ease;
    cursor: pointer;
}

.back-icon:hover {
    transform: scale(1.1);
    filter: brightness(1.2);
}

</style>