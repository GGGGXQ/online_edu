<script setup>
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {reactive} from "vue";

// 测试CORS的跨域配置是否有问题
import axios from "axios"
const http = axios.create()

// 测试服务端的跨域是否配置成功
http.get("http://api.onlineedu.cn:8000/home/test").then(response=>{
  console.log(response.data);
})

const store = reactive({
  value2: null,
  colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
})

</script>

<template>
  <div class="home">
    <Header></Header>
  </div>
  <el-row>
    <el-button round>圆角按钮</el-button>
    <el-button type="primary" round>主要按钮</el-button>
    <el-button type="success" round>成功按钮</el-button>
    <el-button type="info" round>信息按钮</el-button>
    <el-button type="warning" round>警告按钮</el-button>
    <el-button type="danger" round>危险按钮</el-button>
    <el-rate v-model="store.value2" :colors="store.colors"> </el-rate>
  </el-row>
  <div><Footer></Footer></div>
</template>

<style scoped>

</style>