<template>
  <div class="page">
    <div class="content-inner">
        <!-- 统计卡片 -->
        <div class="stat-row">
          <div class="stat-card">
            <div class="stat-icon stat-icon-blue">
              <el-icon :size="22"><User /></el-icon>
            </div>
            <div>
              <div class="stat-num">{{ total }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon stat-icon-green">
              <el-icon :size="22"><Finished /></el-icon>
            </div>
            <div>
              <div class="stat-num">{{ list.length }}</div>
              <div class="stat-label">当前页数据</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon stat-icon-purple">
              <el-icon :size="22"><Calendar /></el-icon>
            </div>
            <div>
              <div class="stat-num">{{ ageAvg }}</div>
              <div class="stat-label">平均年龄</div>
            </div>
          </div>
        </div>

        <!-- 主卡片 -->
        <div class="panel">
          <div class="toolbar">
            <div class="search-box">
              <el-input
                v-model="query.keyword"
                placeholder="输入用户名搜索"
                :prefix-icon="Search"
                clearable
                style="width: 260px"
                @keyup.enter="handleSearch"
                @clear="handleSearch"
              />
              <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
              <el-button :icon="RefreshLeft" @click="handleReset">重置</el-button>
            </div>
            <el-button type="primary" :icon="Plus" @click="openCreate">新增用户</el-button>
          </div>

          <el-table
            v-loading="loading"
            :data="list"
            stripe
            style="width: 100%"
            :header-cell-style="{ background: '#f7f9fd', color: '#5a6a85', fontWeight: 600 }"
          >
            <el-table-column label="头像" width="86" align="center">
              <template #default="{ row }">
                <el-avatar :size="44" :src="row.avatar" class="cell-avatar">
                  <el-icon><UserFilled /></el-icon>
                </el-avatar>
              </template>
            </el-table-column>

            <el-table-column prop="username" label="用户名" min-width="120">
              <template #default="{ row }">
                <span class="cell-username">{{ row.username }}</span>
              </template>
            </el-table-column>

            <el-table-column label="省市区" min-width="220">
              <template #default="{ row }">
                <span class="cell-area">
                  <el-icon><Location /></el-icon>
                  {{ [row.province, row.city, row.area].filter(Boolean).join(' ') || '未设置' }}
                </span>
              </template>
            </el-table-column>

            <el-table-column label="年龄" width="90" align="center">
              <template #default="{ row }">
                <el-tag :type="ageType(row.age)" effect="light" round>{{ row.age }} 岁</el-tag>
              </template>
            </el-table-column>

            <el-table-column label="密码" min-width="170">
              <template #default="{ row }">
                <div class="password-cell">
                  <span class="password-text" :class="{ plain: plainRows.has(row.id) }">
                    {{ plainRows.has(row.id) ? row.password : maskPassword(row.password) }}
                  </span>
                  <el-tooltip
                    :content="plainRows.has(row.id) ? '隐藏明文' : '查看明文'"
                    placement="top"
                  >
                    <el-button
                      link
                      type="primary"
                      :icon="plainRows.has(row.id) ? Hide : View"
                      @click="togglePlain(row.id)"
                    />
                  </el-tooltip>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="创建时间" min-width="170">
              <template #default="{ row }">
                <span class="cell-time">{{ formatTime(row.create_time) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="150" align="center" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="Edit" @click="openEdit(row)">编辑</el-button>
                <el-button link type="danger" :icon="Delete" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination">
            <el-pagination
              v-model:current-page="query.page"
              v-model:page-size="query.pageSize"
              :total="total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              background
              @change="fetchList"
            />
          </div>
        </div>
      </div>

    <!-- 新增 / 编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '新增用户'"
      width="520px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
        label-position="right"
      >
        <el-form-item label="头像" prop="avatar">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :headers="uploadHeaders"
            :show-file-list="false"
            accept="image/*"
            :before-upload="beforeUpload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
          >
            <el-avatar :size="72" :src="form.avatar" class="upload-avatar">
              <el-icon :size="28"><Plus /></el-icon>
            </el-avatar>
          </el-upload>
          <div class="upload-tip">点击上传头像（jpg / png，≤2MB）</div>
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" maxlength="50" />
        </el-form-item>

        <el-form-item label="省市区" prop="area">
          <el-cascader
            v-model="form.area"
            :options="regionData"
            placeholder="请选择省市区"
            style="width: 100%"
            filterable
          />
        </el-form-item>

        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="form.age" :min="1" :max="120" controls-position="right" style="width: 160px" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            :placeholder="isEdit ? '留空则不修改密码' : '请输入密码'"
            maxlength="50"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ isEdit ? '保 存' : '新 增' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Calendar,
  Delete,
  Edit,
  Finished,
  Hide,
  Location,
  Plus,
  RefreshLeft,
  Search,
  User,
  UserFilled,
  View,
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import { regionData, codeToText } from 'element-china-area-data'
import { getUsers, createUser, updateUser, deleteUser } from '../api/user'

const uploadHeaders = {
  Authorization: `Bearer ${localStorage.getItem('admin_token') || ''}`,
}

const loading = ref(false)
const submitting = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ page: 1, pageSize: 10, keyword: '' })

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const plainRows = reactive(new Set())

const emptyForm = () => ({
  id: null,
  username: '',
  area: [],
  avatar: '',
  age: 18,
  password: '',
})

const form = reactive(emptyForm())

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度为 2 - 50 个字符', trigger: 'blur' },
  ],
  area: [{ required: true, type: 'array', min: 3, message: '请选择省市区', trigger: 'change' }],
  age: [{ required: true, type: 'number', min: 1, max: 120, message: '请输入有效年龄', trigger: 'blur' }],
  password: [
    {
      validator: (_r, value, callback) => {
        if (!isEdit.value && !value) {
          callback(new Error('请输入密码'))
        } else if (value && value.length < 6) {
          callback(new Error('密码至少 6 位'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

const ageAvg = computed(() => {
  if (!list.value.length) return 0
  return (list.value.reduce((sum, u) => sum + (Number(u.age) || 0), 0) / list.value.length).toFixed(1)
})

function ageType(age) {
  if (age >= 30) return 'primary'
  if (age >= 25) return 'success'
  return 'warning'
}

function maskPassword(plain) {
  if (!plain) return ''
  if (plain.length <= 4) return '*'.repeat(plain.length)
  return `${plain.slice(0, 2)}****${plain.slice(-1)}`
}

// element-china-area-data 的级联 value 是 code，这里做名称 <-> code 转换
function namesToCodes(province, city, area) {
  const prov = regionData.find((x) => x.label === province)
  if (!prov) return []
  if (!city) return [prov.value]
  const c = (prov.children || []).find((x) => x.label === city)
  if (!c) return [prov.value]
  if (!area) return [prov.value, c.value]
  const a = (c.children || []).find((x) => x.label === area)
  if (!a) return [prov.value, c.value]
  return [prov.value, c.value, a.value]
}

function codesToNames(codes) {
  return (codes || []).map((code) => codeToText[code] || code)
}

function togglePlain(id) {
  if (plainRows.has(id)) plainRows.delete(id)
  else plainRows.add(id)
}

function formatTime(time) {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-'
}

async function fetchList() {
  loading.value = true
  try {
    const res = await getUsers({ ...query })
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  query.page = 1
  fetchList()
}

function handleReset() {
  query.keyword = ''
  query.page = 1
  fetchList()
}

function openCreate() {
  isEdit.value = false
  Object.assign(form, emptyForm())
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    username: row.username,
    area: namesToCodes(row.province, row.city, row.area),
    avatar: row.avatar,
    age: row.age,
    password: row.password,
  })
  dialogVisible.value = true
}

function beforeUpload(file) {
  const isImage = /^image\/(png|jpe?g|gif|webp|bmp)$/.test(file.type)
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (file.size / 1024 / 1024 > 2) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }
  return true
}

function handleUploadSuccess(res) {
  form.avatar = res.url
  ElMessage.success('头像上传成功')
}

function handleUploadError() {
  ElMessage.error('头像上传失败，请检查登录状态')
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const areaNames = codesToNames(form.area)
    const payload = {
      username: form.username.trim(),
      province: areaNames[0] || '',
      city: areaNames[1] || '',
      area: areaNames[2] || '',
      avatar: form.avatar,
      age: form.age,
    }
    if (isEdit.value) {
      if (form.password) payload.password = form.password
      await updateUser(form.id, payload)
      ElMessage.success('用户更新成功')
    } else {
      payload.password = form.password
      await createUser(payload)
      ElMessage.success('用户创建成功')
    }
    dialogVisible.value = false
    fetchList()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户「${row.username}」吗？此操作不可恢复。`,
      '删除确认',
      { type: 'warning', confirmButtonText: '确 定', cancelButtonText: '取 消' }
    )
  } catch {
    return
  }
  await deleteUser(row.id)
  ElMessage.success('删除成功')
  if (list.value.length === 1 && query.page > 1) query.page -= 1
  fetchList()
}

onMounted(fetchList)
</script>

<style scoped>
.page {
  min-height: 100%;
}

.content-inner {
  /*max-width: 1200px;*/
  margin: 0 auto;
  padding: 22px 24px 40px;
}

/* 统计卡片 */
.stat-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 18px;
}

.stat-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px 22px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(31, 45, 61, 0.05);
  border: 1px solid #eef1f8;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.stat-icon-blue { background: linear-gradient(135deg, #5b7cfa, #8e54e9); }
.stat-icon-green { background: linear-gradient(135deg, #22c59a, #3ee0c4); }
.stat-icon-purple { background: linear-gradient(135deg, #f78b5a, #f5a623); }

.stat-num {
  font-size: 24px;
  font-weight: 700;
  color: #1f2d3d;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #7a8699;
  margin-top: 2px;
}

/* 主面板 */
.panel {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 4px 16px rgba(31, 45, 61, 0.05);
  border: 1px solid #eef1f8;
  padding: 18px 20px 20px;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  gap: 10px;
  align-items: center;
}

.cell-username {
  font-weight: 600;
  color: #2b3a55;
}

.cell-area {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #5a6a85;
}

.cell-area .el-icon {
  color: #8ea0c0;
}

.password-cell {
  display: flex;
  align-items: center;
  gap: 4px;
}

.password-text {
  font-family: 'Consolas', 'Courier New', monospace;
  letter-spacing: 1px;
  color: #5a6a85;
}

.password-text.plain {
  color: #2b3a55;
  font-weight: 600;
}

.cell-time {
  color: #8a94a8;
  font-size: 13px;
}

.cell-avatar {
  border: 2px solid #eef1f8;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

/* 头像上传 */
.upload-avatar {
  border: 2px dashed #cdd6e8;
  background: #f7f9fd;
  color: #9aa7bd;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-avatar:hover {
  border-color: var(--brand);
  color: var(--brand);
  background: var(--brand-light);
}

.upload-tip {
  margin-left: 14px;
  font-size: 12px;
  color: #9aa7bd;
  line-height: 1.5;
}

:deep(.el-upload) {
  display: inline-flex;
}
</style>
