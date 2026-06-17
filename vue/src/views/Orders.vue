<template>
  <div class="orders-page">
    <div class="header">
      <h2>订单管理</h2>
      <div class="filters">
        <el-select
          v-model="statusFilter"
          placeholder="订单状态"
          style="width: 150px; margin-right: 10px;"
          clearable
          @change="loadOrders"
        >
          <el-option label="待付款" value="pending" />
          <el-option label="待发货" value="confirmed" />
          <el-option label="待收货" value="shipped" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
        <el-button type="primary" @click="loadOrders">刷新</el-button>
      </div>
    </div>

    <el-table :data="orders" v-loading="loading" style="width: 100%">
      <el-table-column prop="id" label="订单号" width="100" />
      <el-table-column prop="user_id" label="用户 ID" width="100" />
      <el-table-column label="订单详情" min-width="200">
        <template #default="{ row }">
          <div v-for="(item, index) in row.items" :key="index" class="order-item">
            <span>{{ item.title }} x {{ item.quantity }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="total_amount" label="金额" width="100">
        <template #default="{ row }">
          ¥{{ row.total_amount.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="下单时间" width="180" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button 
            v-if="row.status === 'pending'" 
            size="small" 
            type="success"
            @click="updateStatus(row, 'confirmed')"
          >
            确认订单
          </el-button>
          <el-button 
            v-if="['confirmed', 'paid'].includes(row.status)" 
            size="small" 
            type="primary"
            @click="updateStatus(row, 'shipped')"
          >
            发货
          </el-button>
          <el-button 
            v-if="row.status === 'shipped'" 
            size="small" 
            type="success"
            disabled
          >
            待买家收货
          </el-button>
          <el-button 
            v-if="!['completed', 'cancelled'].includes(row.status)" 
            size="small" 
            type="danger"
            @click="cancelOrder(row)"
          >
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="statistics">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-card">
              <div class="stat-value">{{ stats.pending || 0 }}</div>
              <div class="stat-label">待处理订单</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-card">
              <div class="stat-value">{{ stats.total_orders || 0 }}</div>
              <div class="stat-label">总订单数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-card">
              <div class="stat-value">¥{{ stats.total_amount || 0 }}</div>
              <div class="stat-label">总销售额</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-card">
              <div class="stat-value">{{ stats.completed || 0 }}</div>
              <div class="stat-label">已完成订单</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const orders = ref([])
const loading = ref(false)
const statusFilter = ref('')
const stats = reactive({
  total_orders: 0,
  total_amount: 0,
  pending: 0,
  completed: 0
})

const loadOrders = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/orders')
    if (res.data.success) {
      orders.value = res.data.data
      calculateStats()
    }
  } catch (error) {
    ElMessage.error('加载订单列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.total_orders = orders.value.length
  stats.total_amount = orders.value.reduce((sum, order) => sum + order.total_amount, 0)
  stats.pending = orders.value.filter(o => o.status === 'pending').length
  stats.completed = orders.value.filter(o => o.status === 'completed').length
}

const updateStatus = async (order, newStatus) => {
  try {
    await ElMessageBox.confirm(`确认将订单状态更新为${getStatusText(newStatus)}吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const res = await axios.put(`/api/orders/${order.id}/status`, {
      status: newStatus
    })
    
    if (res.data.success) {
      ElMessage.success('更新成功')
      loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新失败')
      console.error(error)
    }
  }
}

const cancelOrder = async (order) => {
  try {
    await ElMessageBox.confirm(`确定要取消订单 #${order.id} 吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const res = await axios.put(`/api/orders/${order.id}/status`, {
      status: 'cancelled'
    })
    
    if (res.data.success) {
      ElMessage.success('订单已取消')
      loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消失败')
      console.error(error)
    }
  }
}

const getStatusType = (status) => {
  const map = {
    'pending': 'warning',
    'confirmed': 'primary',
    'paid': 'primary',
    'shipped': 'success',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待付款',
    'confirmed': '待发货',
    'paid': '待发货',
    'shipped': '待收货',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.orders-page {
  background: white;
  padding: 20px;
  border-radius: 4px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  font-size: 20px;
  color: #333;
}

.filters {
  display: flex;
  gap: 10px;
}

.order-item {
  padding: 4px 0;
  border-bottom: 1px dashed #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.statistics {
  margin-top: 30px;
}

.stat-card {
  text-align: center;
  padding: 10px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}
</style>
