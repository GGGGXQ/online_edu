<template>
	<div class="login box">
		<img src="../assets/login-background.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
      <div class="login_box">
          <div class="title">
            <span class="active">用户注册</span>
          </div>
          <div class="inp">
            <input v-model="user.mobile" type="text" placeholder="手机号码" class="user">
            <input v-model="user.password" type="password" placeholder="登录密码" class="user">
            <input v-model="user.re_password" type="password" placeholder="确认密码" class="user">
            <input v-model="user.code"  type="text" class="code" placeholder="短信验证码">
            <el-button id="get_code" type="primary" @click="send_sms">{{user.sms_btn_text}}</el-button>
<!--            <button class="login_btn" @click="show_captcha">注册</button>-->
            <button class="login_btn" @click="registerhandler">注册</button>
            <p class="go_login" >已有账号 <router-link to="/login">立即登录</router-link></p>
          </div>
      </div>
		</div>
	</div>
</template>

<script setup>
import {reactive, watch} from "vue"
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import "../utils/Tcaptcha.js"
import user from "../api/user";
import settings from "../settings";
const store = useStore()
const router = useRouter()

// 监听数据mobile是否发生变化
watch(()=>user.mobile, (mobile, prevMobile) => {
  if(/1[3-9]\d{9}/.test(user.mobile)){
    // 发送ajax验证手机号是否已经注册
    user.check_mobile().catch(error=>{
      ElMessage.error(error.response.data.errmsg);
    })
  }
})


// 显示登录验证码
const show_captcha = ()=>{
  // 直接生成一个验证码对象
  let  captcha1 = new TencentCaptcha(settings.captcha_app_id, (res)=>{
    // 验证码通过验证以后的回调方法
    if(res && res.ret === 0){
      // 验证通过，发送登录请求
      registerhandler(res)
    }
  });

  // 显示验证码
  captcha1.show();
}


const registerhandler = (res)=> {
  // 注册处理
  if (!/^1[3-9]\d{9}$/.test(user.mobile)) {
    // 错误提示
    ElMessage.error('错了哦，手机号格式不正确！');
    return false // 阻止代码继续往下执行
  }
  if (user.password.length < 6 || user.password.length > 16) {
    ElMessage.error('错了哦，密码必须在6~16个字符之间！');
    return false
  }

  if (user.password !== user.re_password) {
    ElMessage.error('错了哦，密码和确认密码不一致！');
    return false
  }

    // 发送请求
  user.register({
    // 验证码通过的票据信息
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(response=>{
    // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    sessionStorage.removeItem("access");
    sessionStorage.removeItem("refresh");
    console.log(response.data);
    console.log(response.data.access);
    console.log(response.data.refresh);
    // if(user.remember){ // 判断是否记住登录状态
    //   // 记住登录
    //   localStorage.access = response.data.access
    //   localStorage.refresh = response.data.refresh
    // }else{
    //   // 不记住登录，关闭浏览器以后就删除状态
    //   sessionStorage.access = response.data.access;
    //   sessionStorage.refresh = response.data.refresh;
    // }

    // 默认不需要记住登录
    sessionStorage.token = response.data.access;

    // vuex 存储用户登录信息，保存token, 并根据用户的选择，是否记住密码
    console.log(response.data)
    let payload = response.data.access.split(".")[1]
    let payload_data = JSON.parse(atob(payload))
    console.log(payload_data)
    store.commit("login", payload_data);
    // 清空表单信息
    user.mobile = ""
    user.password = ""
    user.code = ""
    user.remember = false
    //  成功提示
    ElMessage.success("注册成功！");
    // 路由跳转到首页
    router.push("/");
  })
}

// 发送短信
const send_sms = ()=> {
  if (!/1[3-9]\d{9}/.test(user.mobile)) {
    ElMessage.error("手机号格式有误！")
    return false
  }

  // 判断是否处于短信发送的冷却状态
  if (user.is_send) {
    ElMessage.error("短信发送过于频繁！")
    return false
  }

  let time = user.sms_interval;
  // 发送短信请求
  user.get_sms_code().then(response=>{
    ElMessage.success("短信发送中，请留意您的手机！");
    // 发送短信后进入冷却状态
    user.is_send = true;
    // 冷却倒计时
    clearInterval(user.interval);
    user.interval = setInterval(()=> {
      if (time < 1) {
        // 退出短信发送的冷却状态
        user.is_send = false
        user.sms_btn_text = "点击获取验证码"
      } else {
        time -= 1;
        user.sms_btn_text = `${time}秒后重新获取`;
      }
    }, 1000)
  }).catch(error=>{
    ElMessage.error(error?.response?.data?.errmsg);
    time = error?.response?.data?.interval;
    // 冷却倒计时
    clearInterval(user.interval);
    user.interval = setInterval(()=>{
      if(time<1){
        // 退出短信发送的冷却状态
        user.is_send = false
        user.sms_btn_text = "点击获取验证码"
      }else{
        time-=1;
        user.sms_btn_text = `${time}秒后重新获取`;
      }
    }, 1000)

  })
}

</script>

<style scoped>
.box {
  width: 100%;
  height: 100vh; /* 确保占满视口高度 */
  position: relative;
  overflow: hidden;
}
.box img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 自适应填满容器 */
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1; /* 背景图放在底层 */
}
.box .login {
  position: relative; /* 前景内容相对定位 */
  z-index: 2; /* 确保前景内容在背景图之上 */
  width: 500px;
  height:600px;
  margin: 0 auto; /* 水平居中 */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 偏移调整垂直居中 */
}
.login-title{
     width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.login_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
    padding-top: 50px;
}
.title{
	font-size: 20px;
	color: #9b9b9b;
	letter-spacing: .32px;
	border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 0 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}
.title span.active{
	color: #4a4a4a;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp .code{
  width: 190px;
  margin-right: 16px;
}
#get_code{
 margin-top: 6px;
}
.inp input{
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
     display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
    vertical-align: middle;
    margin-right: 4px;
}

.inp .rember p span{
    display: inline-block;
  font-size: 12px;
  width: 100px;
}
.login_btn{
    cursor: pointer;
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
    border: none;
    outline: none;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>