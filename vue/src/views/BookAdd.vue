<template>
  <div class="book-add">
    <el-card shadow="never">
      <div class="page-header">
        <h2>{{ isEdit ? '✏️ 编辑图书' : '➕ 添加图书' }}</h2>
        <p class="subtitle">填写图书信息，发布后会自动同步到小程序</p>
      </div>
      
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="book-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="书名" prop="title">
              <el-input v-model="form.title" placeholder="请输入书名" clearable />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="作者" prop="author">
              <el-input v-model="form.author" placeholder="请输入作者" clearable />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="价格" prop="price">
              <el-input-number v-model="form.price" :min="0" :precision="2" :step="0.1" style="width: 100%;" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="库存" prop="stock">
              <el-input-number v-model="form.stock" :min="0" :step="1" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类" prop="category">
              <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%;">
                <el-option label="📱 计算机" value="计算机" />
                <el-option label="📚 文学" value="文学" />
                <el-option label="📜 历史" value="历史" />
                <el-option label="💰 经济" value="经济" />
                <el-option label="🎓 教育" value="教育" />
                <el-option label="📦 其他" value="其他" />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="ISBN" prop="isbn">
              <el-input v-model="form.isbn" placeholder="请输入 ISBN 编号" clearable />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="封面图片" prop="cover_image">
          <div class="image-upload">
            <el-input v-model="form.cover_image" placeholder="请输入封面图片 URL 或点击上传" clearable style="margin-bottom: 10px;">
              <template #prefix>
                <el-icon><Picture /></el-icon>
              </template>
            </el-input>
            <el-upload
              action="/api/upload"
              :on-success="handleCoverSuccess"
              :show-file-list="false"
              accept="image/*"
            >
              <el-button type="primary" size="small">
                <el-icon><Upload /></el-icon>
                选择本地图片
              </el-button>
            </el-upload>
            <div v-if="form.cover_image" class="image-preview">
              <el-image :src="form.cover_image" fit="cover" style="width: 100px; height: 100px;" />
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="图书图片">
          <div class="image-upload">
            <el-upload
              action="/api/upload"
              :on-success="handleImageSuccess"
              :file-list="imageList"
              list-type="picture-card"
              accept="image/*"
              multiple
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
            <el-dialog v-model="dialogVisible">
              <img w-full :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>
          </div>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="6"
            placeholder="请输入图书描述，包括内容简介、特色等"
            show-word-limit
            maxlength="1000"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting" size="default">
            <el-icon><Check /></el-icon>
            {{ isEdit ? '更新图书' : '立即发布' }}
          </el-button>
          <el-button @click="cancel" size="default">
            <el-icon><Close /></el-icon>
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { bookAPI } from '../api'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)

const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  author: '',
  price: 0,
  stock: 0,
  category: '',
  isbn: '',
  cover_image: '',
  images: [],
  description: ''
})

const imageList = ref([])
const dialogImageUrl = ref('')
const dialogVisible = ref(false)

const handleCoverSuccess = (response) => {
  if (response.success) {
    form.cover_image = response.url
    ElMessage.success('封面上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

const handleImageSuccess = (response, file, fileList) => {
  if (response.success) {
    imageList.value = fileList
    form.images = fileList.map(f => f.response?.url || f.url)
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

const handleRemove = (file, fileList) => {
  imageList.value = fileList
  form.images = fileList.map(f => f.response?.url || f.url)
}

const handlePictureCardPreview = (file) => {
  dialogImageUrl.value = file.url
  dialogVisible.value = true
}

const rules = {
  title: [{ required: true, message: '请输入书名', trigger: 'blur' }],
  author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }]
}

const loadBook = async () => {
  if (!isEdit.value) return
  
  try {
    const res = await bookAPI.getDetail(route.params.id)
    if (res.data.success) {
      const data = res.data.data
      Object.assign(form, {
        title: data.title,
        author: data.author,
        price: data.price,
        stock: data.stock,
        category: data.category,
        isbn: data.isbn,
        cover_image: data.cover_image,
        description: data.description
      })
      
      // 加载图片
      if (data.images && data.images.length > 0) {
        imageList.value = data.images.map(img => ({
          name: img.image_url,
          url: img.image_url
        }))
        form.images = data.images.map(img => img.image_url)
      }
    }
  } catch (error) {
    ElMessage.error('加载图书信息失败')
    console.error(error)
  }
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true
    
    const data = {
      title: form.title,
      author: form.author,
      price: form.price,
      stock: form.stock,
      category: form.category,
      isbn: form.isbn,
      cover_image: form.cover_image,
      images: form.images,
      description: form.description
    }
    
    let res
    if (isEdit.value) {
      res = await bookAPI.update(route.params.id, data)
    } else {
      res = await bookAPI.create(data)
    }
    
    if (res.data.success) {
      ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
      router.push('/')
    }
  } catch (error) {
    if (error.message !== 'cancel') {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
      console.error(error)
    }
  } finally {
    submitting.value = false
  }
}

const cancel = () => {
  router.push('/')
}

onMounted(() => {
  loadBook()
})
</script>

<style scoped>
.book-add {
  background: white;
  padding: 20px;
  border-radius: 4px;
}

.page-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.page-header h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  color: #999;
  font-size: 14px;
}

.book-form {
  max-width: 900px;
  margin: 0 auto;
}

.image-upload {
  width: 100%;
}

.image-preview {
  margin-top: 10px;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  padding: 10px;
  display: inline-block;
}

:deep(.el-upload-list--picture-card) {
  margin-top: 10px;
}
</style>
