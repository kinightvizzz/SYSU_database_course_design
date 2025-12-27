<template>
  <div class="admin-page">
    <!-- 管理员欢迎区域 -->
    <div class="admin-welcome custom-card fade-in">
      <div class="welcome-content">
        <h2 class="welcome-title">👑 管理员控制台</h2>
        <p class="admin-info">欢迎您，{{ username }} | 系统管理员</p>
      </div>
      <div class="welcome-stats">
        <div class="stat-item">
          <span class="stat-label">今日订单</span>
          <span class="stat-value">{{ todayOrders || "--" }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">在售商品</span>
          <span class="stat-value">{{ products.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">在职员工</span>
          <span class="stat-value">--</span>
        </div>
      </div>
    </div>

    <!-- 收入统计卡片 -->
    <div class="income-stats custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">📊 按日期统计收入</h3>
      </div>

      <div class="date-input-group">
        <input type="date" v-model="statDate" class="date-input" />
        <button class="query-btn btn-primary" @click="loadDailyIncome">
          查询
        </button>
      </div>

      <div v-if="dailyIncome" class="income-result">
        <div class="income-item">
          <span class="income-label">统计日期</span>
          <span class="income-value date">{{ dailyIncome.stat_date }}</span>
        </div>
        <div class="income-item">
          <span class="income-label">订单数量</span>
          <span class="income-value orders">{{ dailyIncome.order_count }}</span>
        </div>
        <div class="income-item">
          <span class="income-label">总收入</span>
          <span class="income-value total"
            >¥{{ dailyIncome.total_income }}</span
          >
        </div>
      </div>
    </div>

    <!-- 商品销售统计卡片 -->
    <div class="sales-stats custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">📈 商品销售统计</h3>
      </div>

      <div class="table-container">
        <table class="stats-table">
          <thead>
            <tr>
              <th>商品名</th>
              <th>类别</th>
              <th>总销量</th>
              <th>总收入</th>
              <th>平均价格</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in productSales" :key="item.product_id">
              <td class="product-name">{{ item.product_name }}</td>
              <td class="category">{{ item.category }}</td>
              <td class="sold">{{ item.total_sold || 0 }}</td>
              <td class="income">¥{{ item.total_income || 0 }}</td>
              <td class="avg-price">¥{{ item.avg_price || 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 员工管理卡片 -->
    <div class="staff-management custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">👨‍💼 员工信息管理</h3>
      </div>

      <div class="staff-form">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">员工ID</label>
            <input
              v-model="staffIdInput"
              placeholder="请输入员工ID"
              class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">手机号</label>
            <input
              v-model="staffPhone"
              placeholder="请输入手机号"
              class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">状态</label>
            <select v-model="staffStatus" class="form-select">
              <option value="在职">在职</option>
              <option value="离职">离职</option>
            </select>
          </div>
        </div>
        <button class="update-btn btn-primary" @click="updateStaff">
          更新员工信息
        </button>
      </div>
    </div>

    <!-- 商品管理卡片 -->
    <div class="product-management custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">🛍️ 商品管理</h3>
      </div>

      <div class="table-container">
        <table class="products-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>商品名</th>
              <th>类别</th>
              <th>价格</th>
              <th>库存</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.product_id">
              <td class="product-id">{{ p.product_id }}</td>
              <td>
                <input v-model="p.product_name" class="table-input" />
              </td>
              <td>
                <input v-model="p.category" class="table-input" />
              </td>
              <td>
                <input
                  type="number"
                  v-model.number="p.price"
                  class="table-input number"
                  min="0" />
              </td>
              <td>
                <input
                  type="number"
                  v-model.number="p.stock"
                  class="table-input number"
                  min="0" />
              </td>
              <td class="actions">
                <button class="save-btn" @click="updateProduct(p)">保存</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 新增商品卡片 -->
    <div class="add-product custom-card fade-in">
      <div class="section-header">
        <h3 class="section-title">➕ 新增商品</h3>
      </div>

      <div class="add-form">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">商品名</label>
            <input
              v-model="newProduct.name"
              placeholder="请输入商品名"
              class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">价格</label>
            <input
              v-model.number="newProduct.price"
              type="number"
              placeholder="请输入价格"
              class="form-input"
              min="0" />
          </div>
          <div class="form-group">
            <label class="form-label">库存</label>
            <input
              v-model.number="newProduct.stock"
              type="number"
              placeholder="请输入库存"
              class="form-input"
              min="0" />
          </div>
          <div class="form-group">
            <label class="form-label">类别</label>
            <input
              v-model="newProduct.category"
              placeholder="请输入类别"
              class="form-input" />
          </div>
        </div>
        <button class="add-btn btn-primary" @click="addProduct">
          新增商品
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

      // 原有数据
      statDate: "",
      dailyIncome: null,
      productSales: [],
      staffIdInput: "",
      staffPhone: "",
      staffStatus: "在职",

      // 新增数据
      products: [],
      newProduct: {
        name: "",
        price: 0,
        stock: 0,
        category: "",
      },

      // 统计相关
      todayOrders: null,
    };
  },

  async mounted() {
    await this.loadProductSales();
    await this.loadProducts();
  },

  methods: {
    async loadDailyIncome() {
      if (!this.statDate) {
        alert("请选择日期");
        return;
      }
      const res = await http.get(`/admin/daily-income?date=${this.statDate}`);
      this.dailyIncome = res.data.data?.[0] || null;
    },

    async loadProductSales() {
      const res = await http.get("/admin/product-sales");
      this.productSales = res.data.data;
    },

    async updateStaff() {
      if (!this.staffIdInput || !this.staffPhone) {
        alert("请填写员工ID和手机号");
        return;
      }

      try {
        await http.post("/admin/staff/update", {
          staff_id: this.staffIdInput,
          phone: this.staffPhone,
          status: this.staffStatus,
        });
        alert("更新成功");
        // 清空表单
        this.staffIdInput = "";
        this.staffPhone = "";
      } catch (err) {
        alert("更新失败：" + err);
      }
    },

    async loadProducts() {
      const res = await http.get("/admin/products");
      this.products = res.data.data;
    },

    async updateProduct(product) {
      try {
        await http.put(`/admin/products/${product.product_id}`, {
          product_name: product.product_name,
          price: product.price,
          stock: product.stock,
          category: product.category,
        });
        alert("商品更新成功");
      } catch (err) {
        alert("更新失败：" + err);
      }
    },

    async addProduct() {
      if (
        !this.newProduct.name ||
        this.newProduct.price <= 0 ||
        this.newProduct.stock < 0
      ) {
        alert("请填写完整且有效的商品信息");
        return;
      }
      try {
        await http.post("/admin/products/add", {
          product_name: this.newProduct.name,
          price: this.newProduct.price,
          stock: this.newProduct.stock,
          category: this.newProduct.category,
        });
        alert("新增商品成功");
        // 清空输入框
        this.newProduct = { name: "", price: 0, stock: 0, category: "" };
        await this.loadProducts();
      } catch (err) {
        alert("新增商品失败：" + err);
      }
    },
  },
};
</script>

<style scoped>
.admin-page {
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 管理员欢迎区域 */
.admin-welcome {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 40px;
  background: linear-gradient(135deg, #722ed1 0%, #1890ff 100%);
  color: white;
}

.welcome-content {
  flex: 1;
}

.welcome-title {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 10px 0;
  color: white;
}

.admin-info {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
}

.welcome-stats {
  display: flex;
  gap: 60px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  min-width: 100px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: white;
}

/* 收入统计卡片 */
.income-stats {
  padding: 24px 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-input-group {
  display: flex;
  gap: 12px;
  align-items: center;
  max-width: 400px;
  margin-bottom: 20px;
}

.date-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

.date-input:focus {
  border-color: #1890ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
}

.query-btn {
  padding: 10px 20px;
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

.query-btn:hover {
  background: #096dd9;
}

.income-result {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.income-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.income-label {
  font-size: 14px;
  color: #666;
}

.income-value {
  font-size: 18px;
  font-weight: 600;
}

.income-value.date {
  color: #722ed1;
}

.income-value.orders {
  color: #1890ff;
}

.income-value.total {
  color: #52c41a;
  font-size: 24px;
}

/* 销售统计卡片 */
.sales-stats {
  padding: 24px 30px;
}

.table-container {
  overflow-x: auto;
  margin: 0 -30px;
  padding: 0 30px;
}

.stats-table,
.products-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.stats-table thead,
.products-table thead {
  background: #fafafa;
}

.stats-table th,
.products-table th {
  padding: 16px 12px;
  text-align: left;
  color: #333;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid #f0f0f0;
}

.stats-table tbody tr,
.products-table tbody tr {
  transition: background-color 0.3s;
  border-bottom: 1px solid #f0f0f0;
}

.stats-table tbody tr:hover,
.products-table tbody tr:hover {
  background-color: #fafafa;
}

.stats-table td,
.products-table td {
  padding: 16px 12px;
  color: #333;
  font-size: 14px;
}

.stats-table tbody tr:last-child,
.products-table tbody tr:last-child {
  border-bottom: none;
}

.product-name {
  font-weight: 500;
}

.category {
  color: #666;
}

.sold,
.income,
.avg-price {
  text-align: right;
  font-weight: 500;
}

.income {
  color: #52c41a;
}

.avg-price {
  color: #1890ff;
}

/* 员工管理卡片 */
.staff-management {
  padding: 24px 30px;
}

.staff-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-input,
.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus,
.form-select:focus {
  border-color: #1890ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
}

.form-select {
  appearance: none;
  background: white
    url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='%23999' d='M5.5 7.5L10 12l4.5-4.5H5.5z'/%3E%3C/svg%3E")
    no-repeat right 12px center;
  background-size: 16px;
  padding-right: 40px;
}

.update-btn {
  align-self: flex-start;
  padding: 12px 30px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 200px;
}

.update-btn:hover {
  background: #096dd9;
}

/* 商品管理卡片 */
.product-management {
  padding: 24px 30px;
}

.table-input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.table-input:focus {
  border-color: #1890ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
}

.table-input.number {
  text-align: right;
  padding-right: 8px;
}

.product-id {
  color: #666;
  font-weight: 500;
}

.actions {
  text-align: center;
}

.save-btn {
  padding: 6px 16px;
  background: #52c41a;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 80px;
}

.save-btn:hover {
  background: #389e0d;
}

/* 新增商品卡片 */
.add-product {
  padding: 24px 30px;
  margin-bottom: 40px;
}

.add-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.add-form .form-row {
  grid-template-columns: repeat(4, 1fr);
}

.add-btn {
  align-self: flex-start;
  padding: 12px 30px;
  background: #52c41a;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 200px;
}

.add-btn:hover {
  background: #389e0d;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .form-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .add-form .form-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .admin-welcome {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .welcome-stats {
    width: 100%;
    justify-content: space-between;
    gap: 20px;
  }

  .stat-item {
    min-width: auto;
  }

  .form-row,
  .add-form .form-row {
    grid-template-columns: 1fr;
  }

  .income-result {
    grid-template-columns: 1fr;
  }
}
</style>
