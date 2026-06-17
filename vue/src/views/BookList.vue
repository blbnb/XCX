<template>
  <div class="book-list">
    <div class="header">
      <div>
        <h2>📖 图书列表</h2>
        <p class="subtitle">管理所有图书信息，支持搜索和筛选</p>
      </div>
      <div class="filters">
        <el-input
          v-model="searchTitle"
          placeholder="搜索书名或作者"
          prefix-icon="Search"
          style="width: 250px; margin-right: 10px;"
          clearable
          @keyup.enter="loadBooks"
        />
        <el-select
          v-model="selectedCategory"
          placeholder="全部分类"
          style="width: 150px; margin-right: 10px;"
          clearable
          @change="loadBooks"
        >
          <el-option
            v-for="cat in categories"
            :key="cat.category"
            :label="cat.category"
            :value="cat.category"
          />
        </el-select>
        <el-button type="primary" @click="loadBooks">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="loadBooks">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <el-card shadow="never" class="table-card">
      <el-table :data="books" v-loading="loading" style="width: 100%" stripe>
        <el-table-column prop="id" label="ID" width="70" align="center" />
        <el-table-column prop="title" label="书名" min-width="180">
          <template #default="{ row }">
            <div class="book-title">
              <el-avatar v-if="row.cover_image" :src="row.cover_image" size="small" style="margin-right: 10px;" />
              <span>{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="author" label="作者" width="120" align="center" />
        <el-table-column prop="price" label="价格" width="100" align="center">
          <template #default="{ row }">
            <span class="price">¥{{ row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.stock > 50 ? 'success' : row.stock > 10 ? 'warning' : 'danger'">
              {{ row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="100" align="center">
          <template #default="{ row }">
            <el-tag size="small" effect="plain">{{ row.category || '未分类' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isbn" label="ISBN" width="150" align="center" />
        <el-table-column label="操作" width="220" fixed="right" align="center">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="editBook(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteBook(row)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadBooks"
        @current-change="loadBooks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { bookAPI } from '../api'

const router = useRouter()

const books = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchTitle = ref('')
const selectedCategory = ref('')
const categories = ref([])

const loadBooks = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    
    const res = await bookAPI.getList(params)
    if (res.data.success) {
      books.value = res.data.data
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('加载图书列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const res = await bookAPI.getCategories()
    if (res.data.success) {
      categories.value = res.data.data
    }
  } catch (error) {
    console.error('加载分类失败', error)
  }
}

const editBook = (row) => {
  router.push(`/edit/${row.id}`)
}

const deleteBook = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除图书《${row.title}》吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const res = await bookAPI.delete(row.id)
    if (res.data.success) {
      ElMessage.success('删除成功')
      loadBooks()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

onMounted(() => {
  loadBooks()
  loadCategories()
})
</script>

<style scoped>
.book-list {
  background: white;
  padding: 20px;
  border-radius: 4px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.header h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 5px;
}

.subtitle {
  font-size: 14px;
  color: #999;
}

.filters {
  display: flex;
  gap: 10px;
  align-items: center;
}

.table-card {
  margin-top: 10px;
}

.book-title {
  display: flex;
  align-items: center;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
