<template>
  <div class="staff-page">
    <!-- 员工欢迎区域 -->
    <div class="staff-welcome custom-card fade-in">
      <div class="welcome-content">
        <h2 class="welcome-title">👨‍💼 员工工作台</h2>
        <p class="staff-info">欢迎您，{{ username }} | 员工ID: {{ staffId }}</p>
      </div>
      <div class="welcome-stats">
        <div class="stat-item">
          <span class="stat-label">待处理订单</span>
          <span class="stat-value">{{ pendingOrdersCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">总订单数</span>
          <span class="stat-value">{{ orders.length }}</span>
        </div>
      </div>
    </div>

    <!-- 订单管理区域 -->
    <div class="orders-section custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">📋 订单管理</h3>
        <div class="section-tools">
          <button class="refresh-btn" @click="loadOrders">🔄 刷新列表</button>
        </div>
      </div>

      <div class="table-container">
        <table class="orders-table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>用户名</th>
              <th>手机号</th>
              <th>状态</th>
              <th>总金额</th>
              <th>商品数量</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.order_id">
              <td
                class="order-no"
                @click="$router.push(`/staff/order/${order.order_id}`)">
                {{ order.order_no }}
              </td>
              <td class="username">{{ order.username }}</td>
              <td class="phone">{{ order.phone }}</td>
              <td>
                <span
                  class="status-badge"
                  :class="getStatusClass(order.order_status)">
                  {{ order.order_status }}
                </span>
              </td>
              <td class="amount">¥{{ order.total_amount }}</td>
              <td class="quantity">{{ order.item_count }}</td>
              <td>
                <button
                  class="ship-btn"
                  @click="shipOrder(order.order_id)"
                  :disabled="order.order_status !== '已支付'"
                  :title="
                    order.order_status !== '已支付'
                      ? '只有已支付订单可发货'
                      : '点击发货'
                  ">
                  发货
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 无数据提示 -->
      <div v-if="orders.length === 0" class="no-data">📭 暂无订单数据</div>
    </div>

    <!-- 快速操作面板 -->
    <div class="quick-actions custom-card fade-in">
      <h3 class="section-title">⚡ 快捷操作</h3>
      <div class="actions-grid">
        <button class="action-btn inventory" @click="goToInventory">
          📦 库存管理
        </button>
        <button class="action-btn customers" @click="goToCustomers">
          👥 客户管理
        </button>
        <button class="action-btn reports" @click="goToReports">
          📊 销售报表
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import http from "../api/http";

export default {
  data() {
    return {
      username: localStorage.getItem("username"),
      staffId: localStorage.getItem("staffId"),
      orders: [],
    };
  },
  computed: {
    pendingOrdersCount() {
      return this.orders.filter((order) => order.order_status === "已支付")
        .length;
    },
  },
  async mounted() {
    await this.loadOrders();
  },
  methods: {
    async loadOrders() {
      try {
        const res = await http.get("/staff/orders");
        this.orders = res.data.data;
      } catch (err) {
        alert("加载订单失败：" + err);
      }
    },
    async shipOrder(orderId) {
      try {
        await http.post("/staff/orders/ship", {
          order_id: orderId,
          staff_id: this.staffId,
        });
        alert("发货成功");
        await this.loadOrders(); // 刷新订单列表
      } catch (err) {
        alert("发货失败：" + err);
      }
    },
    getStatusClass(status) {
      const statusMap = {
        待支付: "pending",
        已支付: "paid",
        已发货: "shipped",
        已完成: "completed",
        已取消: "cancelled",
      };
      return statusMap[status] || "default";
    },
    goToInventory() {
      alert("库存管理功能开发中...");
    },
    goToCustomers() {
      alert("客户管理功能开发中...");
    },
    goToReports() {
      alert("销售报表功能开发中...");
    },
  },
};
</script>

<style scoped>
.staff-page {
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 员工欢迎区域 */
.staff-welcome {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 40px;
  background: linear-gradient(135deg, #2d8cf0 0%, #1890ff 100%);
  color: white;
}

.welcome-content {
  flex: 1;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 10px 0;
  color: white;
}

.staff-info {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
}

.welcome-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: white;
}

/* 订单管理区域 */
.orders-section {
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-tools {
  display: flex;
  gap: 10px;
}

.refresh-btn {
  padding: 8px 16px;
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background: #1890ff;
  border-color: #1890ff;
  color: white;
}

/* 表格样式 */
.table-container {
  overflow-x: auto;
  margin: 0 -30px;
  padding: 0 30px;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1000px;
}

.orders-table thead {
  background: #fafafa;
}

.orders-table th {
  padding: 16px 12px;
  text-align: left;
  color: #333;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid #f0f0f0;
}

.orders-table tbody tr {
  transition: background-color 0.3s;
  border-bottom: 1px solid #f0f0f0;
}

.orders-table tbody tr:hover {
  background-color: #fafafa;
}

.orders-table td {
  padding: 16px 12px;
  color: #333;
  font-size: 14px;
  vertical-align: middle;
}

.orders-table tbody tr:last-child {
  border-bottom: none;
}

/* 表格单元格特定样式 */
.order-no {
  color: #1890ff;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
  text-decoration-color: transparent;
  transition: all 0.3s;
}

.order-no:hover {
  text-decoration-color: #1890ff;
}

.username {
  font-weight: 500;
}

.phone {
  color: #666;
}

.amount {
  color: #ff4d4f;
  font-weight: 600;
}

.quantity {
  color: #666;
  text-align: center;
}

/* 状态标签 */
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.pending {
  background: #fff7e6;
  color: #fa8c16;
}

.status-badge.paid {
  background: #f6ffed;
  color: #52c41a;
}

.status-badge.shipped {
  background: #e6f7ff;
  color: #1890ff;
}

.status-badge.completed {
  background: #f6ffed;
  color: #52c41a;
}

.status-badge.cancelled {
  background: #fff1f0;
  color: #ff4d4f;
}

.status-badge.default {
  background: #fafafa;
  color: #8c8c8c;
}

/* 发货按钮 */
.ship-btn {
  padding: 6px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 80px;
}

.ship-btn:hover:not(:disabled) {
  background: #096dd9;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(24, 144, 255, 0.2);
}

.ship-btn:disabled {
  background: #f5f5f5;
  color: #bfbfbf;
  cursor: not-allowed;
  opacity: 0.6;
}

/* 无数据提示 */
.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
  background: #fafafa;
  border-radius: 4px;
  margin-top: 20px;
}

/* 快速操作面板 */
.quick-actions {
  padding: 24px 30px;
  margin-bottom: 40px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.action-btn {
  padding: 24px 20px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  background: white;
  color: #333;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.action-btn:hover {
  border-color: #1890ff;
  color: #1890ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn.inventory {
  border-left: 4px solid #52c41a;
}

.action-btn.customers {
  border-left: 4px solid #1890ff;
}

.action-btn.reports {
  border-left: 4px solid #fa8c16;
}
</style>
