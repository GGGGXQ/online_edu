<script setup>
import {reactive} from "vue";
const store = reactive({
  value2: null,
  colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
})
</script>

<template>
   <h1>首页</h1>
  <el-row>
    <el-button round>圆角按钮</el-button>
    <el-button type="primary" round>主要按钮</el-button>
    <el-button type="success" round>成功按钮</el-button>
    <el-button type="info" round>信息按钮</el-button>
    <el-button type="warning" round>警告按钮</el-button>
    <el-button type="danger" round>危险按钮</el-button>
    <el-rate v-model="store.value2" :colors="store.colors"> </el-rate>
  </el-row>
</template>

<style scoped>

</style>