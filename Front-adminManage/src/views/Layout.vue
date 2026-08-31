<template>
  <div class="layout">
    <!-- 左侧菜单栏 -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">
          <el-icon :size="20"><UserFilled /></el-icon>
        </div>
        <span class="logo-text">后台管理系统</span>
      </div>

      <el-menu
        class="sidebar-menu"
        :default-active="route.path"
        router
        background-color="transparent"
        text-color="rgba(255,255,255,0.72)"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/articles">
          <el-icon><Document /></el-icon>
          <span>文章列表</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <!-- 右侧内容 -->
    <div class="layout-main">
      <header class="topbar">
        <span class="page-title">{{ route.meta.title }}</span>
        <el-dropdown trigger="click" @command="handleCommand">
          <div class="admin-info">
            <el-avatar :size="34" class="admin-avatar">
              {{ userStore.username?.charAt(0)?.toUpperCase() }}
            </el-avatar>
            <span class="admin-name">{{ userStore.username }}</span>
            <el-icon><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout" :icon="SwitchButton">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </header>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowDown,
  Document,
  SwitchButton,
  User,
  UserFilled,
} from '@element-plus/icons-vue'
import { logout as apiLogout } from '../api/auth'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

async function handleCommand(command) {
  if (command !== 'logout') return
  try {
    await apiLogout()
  } catch {
    /* 后端无状态退出失败也不影响本地登出 */
  }
  userStore.clear()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.layout {
  height: 100vh;
  display: flex;
  background: var(--bg-page);
}

/* 左侧菜单 */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: linear-gradient(180deg, #2b2f6e 0%, #3a4a9f 100%);
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 12px rgba(31, 45, 61, 0.12);
  position: relative;
  z-index: 11;
}

.sidebar-logo {
  height: 62px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.logo-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5b7cfa;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.18);
}

.logo-text {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  white-space: nowrap;
}

.sidebar-menu {
  border-right: none;
  padding: 12px 0;
  flex: 1;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 48px;
  line-height: 48px;
  margin: 4px 12px;
  border-radius: 10px;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.16);
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.08);
}

/* 右侧 */
.layout-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.topbar {
  flex-shrink: 0;
  height: 62px;
  background: #fff;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 6px rgba(31, 45, 61, 0.04);
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-main);
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-main);
  padding: 4px 8px;
  border-radius: 20px;
  transition: background 0.2s;
}

.admin-info:hover {
  background: var(--brand-light);
}

.admin-avatar {
  background: var(--brand-gradient);
  color: #fff;
  font-weight: 600;
}

.admin-name {
  font-size: 14px;
}

.content {
  flex: 1;
  overflow-y: auto;
}
</style>
