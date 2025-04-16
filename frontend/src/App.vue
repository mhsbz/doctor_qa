<script setup>
// 使用路由视图替代直接引入组件
</script>

<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
}

.app-container {
  width: 100%;
  min-height: 100vh;
}
</style>
