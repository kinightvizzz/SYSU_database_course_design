<template>
  <div class="order-detail-page">
    <!-- 返回按钮 -->
    <div class="back-btn-container">
      <button class="back-btn" @click="$router.back()">← 返回</button>
    </div>

    <!-- 订单概览卡片 -->
    <div class="order-overview custom-card fade-in">
      <div class="overview-header">
        <h2 class="order-title">订单详情</h2>
        <span class="order-no-label">订单号：{{ order?.order_no }}</span>
      </div>

      <div v-if="order" class="overview-content">
        <div class="order-status-row">
          <span class="status-label">订单状态：</span>
          <span
            class="order-status"
            :class="getStatusClass(order.order_status)">
            {{ order.order_status }}
          </span>
        </div>

        <div class="order-info-grid">
          <div class="info-item">
            <span class="info-label">总金额：</span>
            <span class="info-value amount">¥{{ order.total_amount }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">下单时间：</span>
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
        <h3 class="items-title">商品明细</h3>
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
      <div v-if="order" class="summary-row">
        <div class="total-summary">
          <span class="total-label">订单总额：</span>
          <span class="total-amount">¥{{ order.total_amount }}</span>
        </div>
      </div>
    </div>

    <!-- 底部操作区域 -->
    <div class="order-actions">
      <button class="action-btn back-action" @click="$router.back()">
        返回
      </button>
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
        已取消: "cancelled",
        已完成: "completed",
      };
      return statusMap[status] || "default";
    },
  },
};
</script>

<style scoped>
.order-detail-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 返回按钮 */
.back-btn-container {
  margin-bottom: 10px;
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

/* 订单概览卡片 */
.order-overview {
  padding: 24px 30px;
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.order-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.order-no-label {
  color: #666;
  font-size: 14px;
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
}

.overview-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-status-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-label {
  color: #333;
  font-weight: 500;
}

.order-status {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.order-status.pending {
  background: #fff7e6;
  color: #fa8c16;
}

.order-status.paid {
  background: #f6ffed;
  color: #52c41a;
}

.order-status.cancelled {
  background: #fff1f0;
  color: #ff4d4f;
}

.order-status.completed {
  background: #f0f5ff;
  color: #1890ff;
}

.order-status.default {
  background: #fafafa;
  color: #8c8c8c;
}

.order-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  color: #666;
  font-size: 14px;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.info-value.amount {
  color: #ff4d4f;
  font-size: 24px;
  font-weight: 600;
}

.info-value.time {
  color: #333;
  font-size: 16px;
}

/* 商品明细卡片 */
.order-items {
  padding: 24px 30px;
}

.items-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.items-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.items-count {
  color: #666;
  font-size: 14px;
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
  padding-top: 16px;
  border-top: 2px solid #f0f0f0;
}

.total-summary {
  display: flex;
  align-items: center;
  gap: 12px;
}

.total-label {
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

.total-amount {
  color: #ff4d4f;
  font-size: 24px;
  font-weight: 600;
}

/* 底部操作区域 */
.order-actions {
  display: flex;
  justify-content: center;
  padding-top: 20px;
  margin-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.action-btn {
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 120px;
}

.back-action {
  background: white;
  border: 1px solid #d9d9d9;
  color: #666;
}

.back-action:hover {
  border-color: #1890ff;
  color: #1890ff;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .order-detail-page {
    padding: 15px;
  }

  .order-overview,
  .order-items {
    padding: 20px;
  }

  .overview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .order-info-grid {
    grid-template-columns: 1fr;
  }

  .table-container {
    margin: 0 -20px;
    padding: 0 20px;
  }

  .summary-row {
    justify-content: center;
  }
}
</style>
