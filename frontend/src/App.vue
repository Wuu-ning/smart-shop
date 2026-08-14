<template>
  <div id="app-container">
    <Navbar />
    <main class="dw-container">
      <router-view />
    </main>
    <footer class="dw-footer">
      <p>智慧商城 &copy; 2026 — AI 评论情感分析系统</p>
    </footer>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style>
/* 全局样式在 theme.css 中定义 */
.dw-footer {
  text-align: center;
  padding: 30px 20px;
  color: var(--dw-gray-light);
  font-size: 13px;
  margin-top: 40px;
  border-top: 1px solid var(--dw-border);
}
</style>
