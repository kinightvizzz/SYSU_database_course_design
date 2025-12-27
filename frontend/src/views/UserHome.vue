<template>
  <div class="user-page">
    <!-- 用户欢迎区域 -->
    <div class="user-welcome custom-card fade-in">
      <div class="user-info">
        <h2 class="welcome-title">欢迎，{{ username }} 👋</h2>
        <p class="user-id">用户ID: {{ userId }}</p>
      </div>
      <button class="user-detail-btn btn-primary" @click="goToUserDetail">
        查看/修改个人信息
      </button>
    </div>

    <!-- 商品列表 -->
    <div class="products-section custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">商品列表</h3>
        <span class="product-count">共 {{ products.length }} 件商品</span>
      </div>

      <div class="products-grid">
        <div
          v-for="item in products"
          :key="item.product_id"
          class="product-item">
          <div class="product-info">
            <h4 class="product-name">{{ item.product_name }}</h4>
            <div class="product-details">
              <span class="product-price">¥{{ item.price }}</span>
              <span class="product-stock">库存: {{ item.stock }}</span>
            </div>
          </div>
          <button
            class="buy-btn"
            @click="buy(item.product_id)"
            :disabled="item.stock === 0"
            :class="{ disabled: item.stock === 0 }">
            {{ item.stock === 0 ? "已售罄" : "购买" }}
          </button>
        </div>
      </div>
    </div>

    <!-- 我的订单 -->
    <div class="orders-section custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">我的订单</h3>
        <span class="order-count">共 {{ orders.length }} 个订单</span>
      </div>

      <div class="orders-list">
        <div v-for="order in orders" :key="order.order_id" class="order-item">
          <div class="order-header">
            <span
              class="order-no"
              @click="$router.push(`/order/${order.order_id}`)">
              订单号: {{ order.order_no }}
            </span>
            <span
              class="order-status"
              :class="getStatusClass(order.order_status)">
              {{ order.order_status }}
            </span>
          </div>

          <div class="order-body">
            <div class="order-amount">
              金额: <span class="amount">¥{{ order.total_amount }}</span>
            </div>

            <div class="order-actions">
              <!-- 改为三个按钮 -->
              <div
                v-if="order.order_status === '待支付'"
                class="payment-buttons">
                <button
                  class="pay-btn wechat"
                  @click="pay(order.order_id, '微信')">
                  微信支付
                </button>
                <button
                  class="pay-btn alipay"
                  @click="pay(order.order_id, '支付宝')">
                  支付宝
                </button>
                <button
                  class="pay-btn bank"
                  @click="pay(order.order_id, '银行卡')">
                  银行卡
                </button>
              </div>
              <button
                v-if="order.order_status === '待支付'"
                class="cancel-btn"
                @click="cancel(order.order_id)">
                取消
              </button>
            </div>
          </div>
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
      username: localStorage.getItem("username"),
      userId: localStorage.getItem("userId"),
      products: [],
      orders: [],
    };
  },

  async mounted() {
    await this.loadProducts();
    await this.loadOrders();
  },

  methods: {
    async loadProducts() {
      const res = await http.get("/products");
      this.products = res.data.data;
    },

    async loadOrders() {
      const res = await http.get(`/orders/user?user_id=${this.userId}`);
      this.orders = res.data.data;
    },

    async buy(productId) {
      await http.post("/orders", {
        user_id: Number(this.userId),
        product_id: productId,
        quantity: 1,
      });

      alert("下单成功");
      await this.loadOrders();
      await this.loadProducts();
    },

    async pay(orderId, payMethod) {
      try {
        await http.post("/orders/pay", {
          order_id: orderId,
          pay_method: payMethod, // 使用传入的支付方式
        });

        alert("支付成功");
        await this.loadOrders();
        await this.loadProducts();
      } catch (err) {
        alert("支付失败：" + err);
      }
    },

    async cancel(orderId) {
      if (!confirm("确定要取消该订单吗？")) return;

      try {
        await http.post("/orders/cancel", {
          order_id: orderId,
        });

        alert("订单已取消");
        await this.loadOrders();
      } catch (err) {
        alert("取消失败：" + err);
      }
    },

    goToUserDetail() {
      this.$router.push(`/user/${this.userId}`);
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
.user-page {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 用户欢迎区域 */
.user-welcome {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 30px;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: white;
}

.user-info {
  flex: 1;
}

.welcome-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: white;
}

.user-id {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

.user-detail-btn {
  background: white;
  color: #1890ff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.user-detail-btn:hover {
  background: #f0f0f0;
  transform: translateY(-1px);
}

/* 商品列表 */
.products-section {
  padding: 24px 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.product-count,
.order-count {
  color: #666;
  font-size: 14px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  transition: all 0.3s;
}

.product-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 8px 0;
  color: #333;
}

.product-details {
  display: flex;
  gap: 20px;
  align-items: center;
}

.product-price {
  color: #ff4d4f;
  font-size: 18px;
  font-weight: 600;
}

.product-stock {
  color: #666;
  font-size: 14px;
}

.buy-btn {
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
  min-width: 80px;
}

.buy-btn:hover:not(.disabled) {
  background: #096dd9;
  transform: translateY(-1px);
}

.buy-btn.disabled {
  background: #d9d9d9;
  cursor: not-allowed;
}
/* 支付按钮容器 */
.payment-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 基础支付按钮样式 */
.pay-method-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
  color: white;
  min-width: 100px;
}

/* 微信支付按钮 */
.pay-wechat {
  background: #07c160;
}

.pay-wechat:hover {
  background: #06ae56;
  transform: translateY(-1px);
}

/* 支付宝按钮 */
.pay-alipay {
  background: #1296db;
}

.pay-alipay:hover {
  background: #0d8bd2;
  transform: translateY(-1px);
}

/* 银行卡按钮 */
.pay-bank {
  background: #8e44ad;
}

.pay-bank:hover {
  background: #7d3c98;
  transform: translateY(-1px);
}

/* 按钮被点击时效果 */
.pay-method-btn:active {
  transform: translateY(0);
}
/* 订单列表 */
.orders-section {
  padding: 24px 30px;
  margin-bottom: 40px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-item {
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  padding: 16px;
  transition: all 0.3s;
}

.order-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.order-no {
  color: #1890ff;
  font-weight: 500;
  cursor: pointer;
  font-size: 16px;
}

.order-no:hover {
  text-decoration: underline;
}

.order-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
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

.order-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-amount {
  font-size: 14px;
  color: #333;
}

.amount {
  font-size: 18px;
  font-weight: 600;
  color: #ff4d4f;
  margin-left: 4px;
}

.order-actions {
  display: flex;
  gap: 8px;
}

.pay-btn {
  padding: 6px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.pay-btn:hover {
  background: #096dd9;
  transform: translateY(-1px);
}

.cancel-btn {
  padding: 6px 16px;
  background: white;
  color: #666;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.cancel-btn:hover {
  border-color: #ff4d4f;
  color: #ff4d4f;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
  }

  .order-body {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .order-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
