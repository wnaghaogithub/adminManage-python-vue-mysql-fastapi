<template>
  <div class="login-page">
    <div class="bg-shape shape-1"></div>
    <div class="bg-shape shape-2"></div>
    <div class="bg-shape shape-3"></div>

    <div class="login-card">
      <div class="brand">
        <div class="brand-logo">
          <el-icon :size="26"><Lock /></el-icon>
        </div>
        <h1 class="brand-title">后台管理系统</h1>
        <p class="brand-sub">Admin Management Platform</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        size="large"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-button
          class="login-btn"
          type="primary"
          size="large"
          :loading="loading"
          @click="handleLogin"
        >
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </el-form>

      <div class="tips">
        <el-icon><InfoFilled /></el-icon>
        <span>默认账号：admin&nbsp;&nbsp;/&nbsp;&nbsp;密码：admin123</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, InfoFilled } from '@element-plus/icons-vue'
import { login } from '../api/auth'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const form = reactive({
  username: 'admin',
  password: 'admin123',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const res = await login({ ...form })
    userStore.setLogin(res.token, res.username)
    ElMessage.success(`欢迎回来，${res.username}`)
    router.push('/')
  } catch {
    // 错误提示已由 axios 拦截器统一处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #2b2f6e 0%, #5b7cfa 50%, #8e54e9 100%);
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.55;
  animation: float 9s ease-in-out infinite;
}

.shape-1 {
  width: 380px;
  height: 380px;
  top: -100px;
  left: -80px;
  background: #ff9a5a;
}

.shape-2 {
  width: 300px;
  height: 300px;
  bottom: -90px;
  right: -60px;
  background: #3ee0c4;
  animation-delay: -3s;
}

.shape-3 {
  width: 220px;
  height: 220px;
  bottom: 25%;
  left: 12%;
  background: #ff6b9d;
  animation-delay: -6s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  50% { transform: translateY(-24px) translateX(16px); }
}

.login-card {
  position: relative;
  z-index: 2;
  width: 420px;
  max-width: calc(100vw - 40px);
  padding: 44px 40px 32px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(18px);
  box-shadow: 0 24px 60px rgba(20, 24, 80, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.brand {
  text-align: center;
  margin-bottom: 32px;
}

.brand-logo {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  color: #fff;
  background: var(--brand-gradient);
  box-shadow: 0 10px 24px rgba(91, 124, 250, 0.4);
}

.brand-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2d3d;
  letter-spacing: 1px;
}

.brand-sub {
  margin-top: 6px;
  font-size: 13px;
  color: #a0a8bc;
  letter-spacing: 0.5px;
}

.login-btn {
  width: 100%;
  margin-top: 8px;
  font-size: 16px;
  letter-spacing: 6px;
  border-radius: 10px;
  background: var(--brand-gradient);
  border: none;
  box-shadow: 0 8px 20px rgba(91, 124, 250, 0.35);
}

.login-btn:hover {
  opacity: 0.92;
  box-shadow: 0 10px 26px rgba(91, 124, 250, 0.45);
}

.tips {
  margin-top: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  color: #7a8699;
  background: var(--brand-light);
  border-radius: 8px;
  padding: 10px 0;
}

.tips .el-icon {
  color: var(--brand);
}
</style>
