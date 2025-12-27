<template>
  <div class="user-detail-page">
    <!-- 返回按钮 -->
    <div class="back-btn-container">
      <button class="back-btn" @click="$router.back()">← 返回</button>
    </div>

    <div v-if="user" class="user-detail-container custom-card fade-in">
      <!-- 头部标题 -->
      <div class="detail-header">
        <h2 class="detail-title">个人信息</h2>
        <div class="user-badge">
          <span class="user-id">ID: {{ $route.params.userId }}</span>
        </div>
      </div>

      <!-- 表单内容 -->
      <div class="user-form">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">用户名</label>
            <input
              v-model="user.username"
              class="form-input"
              placeholder="请输入用户名" />
          </div>

          <div class="form-group">
            <label class="form-label">手机号</label>
            <input
              v-model="user.phone"
              class="form-input readonly"
              readonly
              placeholder="手机号" />
            <span class="readonly-hint">不可修改</span>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">密码</label>
            <input
              v-model="user.password"
              type="password"
              class="form-input"
              placeholder="如需修改密码请在此输入" />
            <span class="password-hint">留空则不修改密码</span>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">性别</label>
            <div class="gender-options">
              <label class="gender-option">
                <input
                  type="radio"
                  v-model="user.gender"
                  value="男"
                  class="gender-radio" />
                <span class="gender-label">男</span>
              </label>
              <label class="gender-option">
                <input
                  type="radio"
                  v-model="user.gender"
                  value="女"
                  class="gender-radio" />
                <span class="gender-label">女</span>
              </label>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">身份证号</label>
            <input
              v-model="user.id_card"
              class="form-input"
              placeholder="请输入身份证号" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full-width">
            <label class="form-label">地址</label>
            <input
              v-model="user.address"
              class="form-input"
              placeholder="请输入详细地址" />
          </div>
        </div>

        <!-- 保存按钮 -->
        <div class="form-actions">
          <button class="save-btn btn-primary" @click="updateUser">
            保存修改
          </button>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-else class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">加载中...</p>
    </div>
  </div>
</template>

<script>
import http from "../api/http";

export default {
  data() {
    return {
      user: null,
    };
  },
  async mounted() {
    const userId = this.$route.params.userId;
    try {
      const res = await http.get(`/info?user_id=${userId}`);
      if (res.data.code === 0) {
        this.user = res.data.data;
      } else {
        alert(res.data.msg);
      }
    } catch (err) {
      alert("加载用户信息失败：" + err);
    }
  },
  methods: {
    async updateUser() {
      try {
        await http.post("/update", this.user);
        alert("更新成功！");
      } catch (err) {
        alert("更新失败：" + err);
      }
    },
  },
};
</script>

<style scoped>
.user-detail-page {
  max-width: 800px;
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

/* 用户详情容器 */
.user-detail-container {
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.detail-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-id {
  background: #f5f5f5;
  color: #666;
  font-size: 14px;
  padding: 4px 12px;
  border-radius: 4px;
}

/* 表单样式 */
.user-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #1890ff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
}

.form-input::placeholder {
  color: #bfbfbf;
}

.form-input.readonly {
  background-color: #fafafa;
  border-color: #f0f0f0;
  color: #666;
  cursor: not-allowed;
}

.readonly-hint {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.password-hint {
  font-size: 12px;
  color: #fa8c16;
  margin-top: 4px;
}

/* 性别选择 */
.gender-options {
  display: flex;
  gap: 20px;
  margin-top: 4px;
}

.gender-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.gender-radio {
  margin: 0;
  cursor: pointer;
}

.gender-label {
  font-size: 14px;
  color: #333;
  cursor: pointer;
}

.gender-radio:checked + .gender-label {
  color: #1890ff;
  font-weight: 500;
}

/* 保存按钮 */
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-top: 30px;
  border-top: 1px solid #f0f0f0;
}

.save-btn {
  padding: 12px 40px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 160px;
}

.save-btn:hover {
  background: #096dd9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.save-btn:active {
  transform: translateY(0);
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #1890ff;
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
}

/* 响应式调整 */
@media (max-width: 768px) {
  .user-detail-page {
    padding: 15px;
  }

  .user-detail-container {
    padding: 20px;
  }

  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .form-group.full-width {
    grid-column: span 1;
  }

  .save-btn {
    width: 100%;
  }
}
</style>
