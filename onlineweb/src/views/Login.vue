<template>
	<div class="login box">
		<img src="../assets/login-background.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
      <div class="login_box">
          <Login></Login>
      </div>
		</div>
	</div>
</template>

<script setup>
import Login from "../components/Login.vue"

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
  height: 400px;
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
</style>