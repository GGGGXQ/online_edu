<template>
  <router-view></router-view>
</template>

<script setup>

</script>

<style>
/* 声明全局样式和项目的初始化样式 */
body,h1,h2,h3,h4,p,table,tr,td,ul,li,a,form,input,select,option,textarea{
  margin:0;
  padding: 0;
  font-size: 15px;
}
a{
  text-decoration: none;
  color: #333;
  cursor: pointer;
}
ul,li{
  list-style: none;
}
table{
  border-collapse: collapse; /* 合并边框 */
}
img{
  max-width: 100%;
  max-height: 100%;
}
input{
  outline: none;
}
.cart .el-checkbox .el-checkbox__inner{
  width: 30px;
  height: 30px;
  border: 1px solid #aaa;
}
.cart .el-checkbox .el-checkbox__inner::after{
  height: 17px;
  left: 8px;
  width: 10px;
  border: 3px solid #FFF;
  border-left: 0;
  border-top: 0;
}
</style>