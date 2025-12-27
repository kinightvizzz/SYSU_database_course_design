<template>
  <div class="staff-order-page">
    <!-- 返回按钮 -->
    <div class="back-btn-container">
      <button class="back-btn" @click="$router.back()">← 返回订单列表</button>
    </div>

    <!-- 加载状态 -->
    <div v-if="!order" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">加载订单详情中...</p>
    </div>

    <!-- 订单详情内容 -->
    <div v-if="order" class="order-detail-container">
      <!-- 订单概览卡片 -->
      <div class="order-overview custom-card fade-in">
        <div class="overview-header">
          <h2 class="order-title">📦 订单详情（员工）</h2>
          <div class="order-meta">
            <span class="order-no">订单号：{{ order.order_no }}</span>
          </div>
        </div>

        <div class="overview-content">
          <div class="order-info-grid">
            <div class="info-item">
              <span class="info-label">订单状态</span>
              <span
                class="info-value status-badge"
                :class="getStatusClass(order.order_status)">
                {{ order.order_status }}
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">总金额</span>
              <span class="info-value amount">¥{{ order.total_amount }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">下单时间</span>
              <span class="info-value time">{{
                formatTime(order.order_time)
              }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 商品明细卡片 -->
      <div class="order-items custom-card fade-in">
        <div class="items-header">
          <h3 class="items-title">📋 商品明细</h3>
          <span class="items-count">共 {{ items.length }} 件商品</span>
        </div>

        <div class="table-container">
          <table class="items-table">
            <thead>
              <tr>
                <th>商品名</th>
                <th>数量</th>
                <th>单价</th>
                <th>小计</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.product_name">
                <td class="product-name">{{ item.product_name }}</td>
                <td class="quantity">{{ item.quantity }}</td>
                <td class="price">¥{{ item.price }}</td>
                <td class="subtotal">¥{{ item.subtotal }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 汇总行 -->
        <div class="summary-row">
          <div class="total-summary">
            <span class="total-label">订单总额：</span>
            <span class="total-amount">¥{{ order.total_amount }}</span>
          </div>
        </div>
      </div>

      <!-- 操作面板 -->
      <div class="order-actions-panel custom-card fade-in">
        <h3 class="panel-title">🛠️ 订单操作</h3>
        <div class="action-info">
          <p v-if="order.order_status === '已支付'" class="info-text ready">
            ✅ 订单已支付，可以进行发货操作
          </p>
          <p
            v-else-if="order.order_status === '已发货'"
            class="info-text shipped">
            📦 订单已发货
          </p>
          <p
            v-else-if="order.order_status === '已完成'"
            class="info-text completed">
            🎉 订单已完成
          </p>
          <p v-else class="info-text warning">
            ⚠️ 订单状态为 {{ order.order_status }}，暂不能发货
          </p>
        </div>

        <div class="action-buttons">
          <button
            class="ship-btn btn-primary"
            @click="ship"
            :disabled="order.order_status !== '已支付'"
            :title="
              order.order_status !== '已支付'
                ? '只有已支付订单可发货'
                : '确认发货'
            ">
            🚚 确认发货
          </button>
          <button class="back-action" @click="$router.back()">返回列表</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import http from "../api/http";

export default {
  data() {
    return {
      order: null,
      items: [],
      staffId: localStorage.getItem("staffId"),
    };
  },

  async mounted() {
    const orderId = this.$route.params.orderId;
    const res = await http.get(`/orders/${orderId}`);
    this.order = res.data.data.order;
    this.items = res.data.data.items;
  },

  methods: {
    formatTime(timeString) {
      if (!timeString) return "-";
      const date = new Date(timeString);
      return date.toLocaleString("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
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

    async ship() {
      try {
        await http.post("/staff/orders/ship", {
          order_id: this.order.order_id,
          staff_id: Number(this.staffId),
        });
        alert("发货成功");
        this.$router.back();
      } catch (err) {
        alert("发货失败：" + (err.response?.data?.msg || err.message));
      }
    },
  },
};
</script>

<style scoped>
.staff-order-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 返回按钮 */
.back-btn-container {
  margin-bottom: 20px;
}

.back-btn {
  background: none;
  border: none;
  color: #1890ff;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 0;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.3s;
}

.back-btn:hover {
  color: #096dd9;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1890ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #666;
  font-size: 16px;
  font-weight: 500;
}

/* 订单详情容器 */
.order-detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 订单概览卡片 */
.order-overview {
  padding: 30px;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.order-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.order-meta {
  display: flex;
  align-items: center;
  gap: 20px;
}

.order-no {
  color: #666;
  font-size: 14px;
  background: #f5f5f5;
  padding: 6px 12px;
  border-radius: 4px;
}

.overview-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.order-info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.info-value.amount {
  color: #ff4d4f;
  font-size: 28px;
  font-weight: 600;
}

.info-value.time {
  color: #333;
  font-size: 16px;
}

/* 状态标签 */
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  min-width: 80px;
  text-align: center;
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

/* 商品明细卡片 */
.order-items {
  padding: 30px;
}

.items-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.items-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.items-count {
  color: #666;
  font-size: 14px;
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
}

.table-container {
  overflow-x: auto;
  margin: 0 -30px;
  padding: 0 30px;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

.items-table thead {
  background: #fafafa;
}

.items-table th {
  padding: 16px 12px;
  text-align: left;
  color: #333;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid #f0f0f0;
}

.items-table tbody tr {
  transition: background-color 0.3s;
  border-bottom: 1px solid #f0f0f0;
}

.items-table tbody tr:hover {
  background-color: #fafafa;
}

.items-table td {
  padding: 16px 12px;
  color: #333;
  font-size: 14px;
}

.items-table tbody tr:last-child {
  border-bottom: none;
}

.product-name {
  font-weight: 500;
  color: #333;
}

.quantity,
.price,
.subtotal {
  color: #666;
  text-align: right;
}

.subtotal {
  color: #ff4d4f;
  font-weight: 500;
}

/* 汇总行 */
.summary-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
}

.total-summary {
  display: flex;
  align-items: center;
  gap: 16px;
}

.total-label {
  color: #333;
  font-size: 18px;
  font-weight: 500;
}

.total-amount {
  color: #ff4d4f;
  font-size: 28px;
  font-weight: 600;
}

/* 操作面板 */
.order-actions-panel {
  padding: 30px;
  margin-bottom: 40px;
}

.panel-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-info {
  margin-bottom: 30px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.info-text {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.info-text.ready {
  color: #52c41a;
}

.info-text.shipped {
  color: #1890ff;
}

.info-text.completed {
  color: #52c41a;
}

.info-text.warning {
  color: #fa8c16;
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.ship-btn {
  flex: 1;
  padding: 14px 24px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.ship-btn:hover:not(:disabled) {
  background: #096dd9;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(24, 144, 255, 0.3);
}

.ship-btn:disabled {
  background: #f5f5f5;
  color: #bfbfbf;
  cursor: not-allowed;
  opacity: 0.7;
}

.back-action {
  flex: 1;
  padding: 14px 24px;
  background: white;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  color: #666;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.back-action:hover {
  border-color: #1890ff;
  color: #1890ff;
}
</style>
