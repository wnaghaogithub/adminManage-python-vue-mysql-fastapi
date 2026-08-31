<template>
  <div class="page">
    <div class="content-inner">
      <!-- 主卡片 -->
      <div class="panel">
        <div class="toolbar">
          <div class="search-box">
            <el-input
              v-model="query.keyword"
              placeholder="输入文章标题搜索"
              :prefix-icon="Search"
              clearable
              style="width: 240px"
              @keyup.enter="handleSearch"
              @clear="handleSearch"
            />
            <el-select
              v-model="query.type"
              placeholder="文章类型"
              clearable
              style="width: 140px"
              @change="handleSearch"
            >
              <el-option v-for="t in typeOptions" :key="t" :label="t" :value="t" />
            </el-select>
            <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
            <el-button :icon="RefreshLeft" @click="handleReset">重置</el-button>
          </div>
          <el-button type="primary" :icon="Plus" @click="openCreate">新增文章</el-button>
        </div>

        <el-table
          v-loading="loading"
          :data="list"
          stripe
          style="width: 100%"
          :header-cell-style="{ background: '#f7f9fd', color: '#5a6a85', fontWeight: 600 }"
        >
          <el-table-column label="主题图片" width="96" align="center">
            <template #default="{ row }">
              <el-image
                v-if="row.image"
                :src="row.image"
                fit="cover"
                class="thumb"
                :preview-src-list="[row.image]"
                preview-teleported
              />
              <div v-else class="thumb-placeholder">
                <el-icon><Picture /></el-icon>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="title" label="标题" min-width="200">
            <template #default="{ row }">
              <span class="cell-title">{{ row.title }}</span>
            </template>
          </el-table-column>

          <el-table-column label="类型" width="110" align="center">
            <template #default="{ row }">
              <el-tag :type="typeTag(row.type)" effect="light" round>{{ row.type }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="内容预览" min-width="280">
            <template #default="{ row }">
              <span class="cell-preview">{{ contentPreview(row.content) || '暂无内容' }}</span>
            </template>
          </el-table-column>

          <el-table-column label="创建时间" width="170">
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
      :title="isEdit ? '编辑文章' : '新增文章'"
      width="780px"
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
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" maxlength="100" />
        </el-form-item>

        <el-form-item label="主题图片" prop="image">
          <el-upload
            class="cover-uploader"
            action="/api/upload"
            :headers="uploadHeaders"
            :show-file-list="false"
            accept="image/*"
            :before-upload="beforeUpload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
          >
            <div v-if="form.image" class="cover-box">
              <img :src="form.image" class="cover-img" />
              <div class="cover-mask">重新上传</div>
            </div>
            <div v-else class="cover-box cover-empty">
              <el-icon :size="26"><Plus /></el-icon>
              <span>上传图片</span>
            </div>
          </el-upload>
          <div class="upload-tip">点击上传主题图片（jpg / png，≤2MB）</div>
        </el-form-item>

        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择文章类型" style="width: 200px">
            <el-option v-for="t in typeOptions" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <div class="editor-wrap">
            <Toolbar
              class="editor-toolbar"
              :editor="editorRef"
              :default-config="toolbarConfig"
              mode="default"
            />
            <Editor
              v-model="form.content"
              class="editor-body"
              :default-config="editorConfig"
              mode="default"
              @onCreated="handleCreated"
            />
          </div>
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
import { onBeforeUnmount, onMounted, reactive, ref, shallowRef } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Edit, Picture, Plus, RefreshLeft, Search } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { getArticles, createArticle, updateArticle, deleteArticle } from '../api/article'

const typeOptions = ['厨艺', '科学', '编程']

const uploadHeaders = {
  Authorization: `Bearer ${localStorage.getItem('admin_token') || ''}`,
}

const loading = ref(false)
const submitting = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ page: 1, pageSize: 10, keyword: '', type: '' })

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const emptyForm = () => ({
  id: null,
  title: '',
  image: '',
  type: '',
  content: '',
})

const form = reactive(emptyForm())

const rules = {
  title: [{ required: true, message: '水电费请输入文章标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择文章类型', trigger: 'change' }],
}

// ---- wangEditor ----
const editorRef = shallowRef()
const toolbarConfig = {}
const editorConfig = {
  placeholder: '请输入文章内容...',
  MENU_CONF: {
    uploadImage: {
      server: '/api/upload',
      fieldName: 'file',
      headers: { Authorization: `Bearer ${localStorage.getItem('admin_token') || ''}` },
      customInsert(res, insertFn) {
        insertFn(res.url, '', '')
      },
    },
  },
}

function handleCreated(editor) {
  editorRef.value = editor
}

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor) editor.destroy()
})

function typeTag(type) {
  if (type === '厨艺') return 'warning'
  if (type === '科学') return 'success'
  return 'primary'
}

function stripHtml(html) {
  if (!html) return ''
  const div = document.createElement('div')
  div.innerHTML = html
  return (div.textContent || '').trim()
}

function contentPreview(content) {
  const text = stripHtml(content)
  return text.length > 60 ? `${text.slice(0, 60)}…` : text
}

function formatTime(time) {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-'
}

async function fetchList() {
  loading.value = true
  try {
    const res = await getArticles({ ...query })
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
  query.type = ''
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
    title: row.title,
    image: row.image,
    type: row.type,
    content: row.content,
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
  form.image = res.url
  ElMessage.success('图片上传成功')
}

function handleUploadError() {
  ElMessage.error('图片上传失败，请检查登录状态')
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const payload = {
      title: form.title.trim(),
      image: form.image,
      type: form.type,
      content: form.content,
    }
    if (isEdit.value) {
      await updateArticle(form.id, payload)
      ElMessage.success('文章更新成功')
    } else {
      await createArticle(payload)
      ElMessage.success('文章创建成功')
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
      `确定要删除文章「${row.title}」吗？此操作不可恢复。`,
      '删除确认',
      { type: 'warning', confirmButtonText: '确 定', cancelButtonText: '取 消' }
    )
  } catch {
    return
  }
  await deleteArticle(row.id)
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

.thumb {
  width: 56px;
  height: 40px;
  border-radius: 6px;
  border: 1px solid #eef1f8;
}

.thumb-placeholder {
  width: 56px;
  height: 40px;
  margin: 0 auto;
  border-radius: 6px;
  background: #f7f9fd;
  color: #c0c9da;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cell-title {
  font-weight: 600;
  color: #2b3a55;
}

.cell-preview {
  color: #8a94a8;
  font-size: 13px;
}

.cell-time {
  color: #8a94a8;
  font-size: 13px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

/* 封面上传 */
.cover-uploader :deep(.el-upload) {
  display: inline-flex;
}

.cover-box {
  width: 140px;
  height: 88px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  border: 2px dashed #cdd6e8;
  background: #f7f9fd;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-mask {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.cover-box:hover .cover-mask {
  opacity: 1;
}

.cover-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #9aa7bd;
  font-size: 12px;
}

.upload-tip {
  margin-left: 14px;
  font-size: 12px;
  color: #9aa7bd;
  line-height: 1.5;
}

/* 编辑器 */
.editor-wrap {
  width: 100%;
  border: 1px solid #e5e9f2;
  border-radius: 6px;
  overflow: hidden;
  z-index: 0;
}

.editor-toolbar {
  border-bottom: 1px solid #e5e9f2;
}

.editor-body {
  height: 320px !important;
  overflow-y: hidden;
}

/* 提升 wangEditor 下拉面板层级，避免被弹窗遮挡 */
:deep(.w-e-select-list),
:deep(.w-e-drop-panel),
:deep(.w-e-modal) {
  z-index: 3000 !important;
}
</style>
