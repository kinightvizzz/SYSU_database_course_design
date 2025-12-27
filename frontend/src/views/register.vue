<template>
  <div class="register-page">
    <div class="register-container custom-card">
      <div class="register-header">
        <h2 class="register-title">用户注册</h2>
      </div>

      <div class="register-form">
        <!-- 用户名 -->
        <div class="form-group">
          <label>用户名</label>
          <input
            v-model="username"
            placeholder="请输入用户名"
            class="form-input" />
        </div>

        <!-- 手机号 -->
        <div class="form-group">
          <label>手机号</label>
          <input
            v-model="phone"
            placeholder="请输入手机号"
            class="form-input" />
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label>密码</label>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            class="form-input" />
        </div>

        <!-- 确认密码 -->
        <div class="form-group">
          <label>确认密码</label>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            class="form-input" />
        </div>

        <!-- 性别 -->
        <div class="form-group">
          <label>性别</label>
          <select v-model="gender" class="form-select">
            <option value="">请选择性别</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>

        <!-- 身份证号 -->
        <div class="form-group">
          <label>身份证号</label>
          <input
            v-model="id_card"
            placeholder="请输入身份证号"
            class="form-input" />
        </div>

        <!-- 地址 -->
        <div class="form-group">
          <label>地址</label>
          <input
            v-model="address"
            placeholder="请输入地址"
            class="form-input" />
        </div>

        <div class="register-actions">
          <button class="register-btn btn-primary" @click="register">
            注册
          </button>
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
      username: "",
      phone: "",
      password: "",
      confirmPassword: "",
      gender: "",
      id_card: "",
      address: "",
    };
  },
  methods: {
    async register() {
      // ✅ 检查所有字段是否填写
      if (
        !this.username ||
        !this.phone ||
        !this.password ||
        !this.confirmPassword ||
        !this.gender ||
        !this.id_card ||
        !this.address
      ) {
        alert("请填写所有信息");
        return;
      }

      // ✅ 密码一致性检查
      if (this.password !== this.confirmPassword) {
        alert("两次密码输入不一致");
        return;
      }

      try {
        // 调用注册接口
        const res = await http.post("/register", {
          username: this.username,
          phone: this.phone,
          password: this.password,
          gender: this.gender,
          id_card: this.id_card,
          address: this.address,
        });

        if (res.data.code === 0) {
          alert("注册成功，请登录");
          this.$router.push("/login");
        } else {
          alert("注册失败：" + res.data.msg);
        }
      } catch (err) {
        alert("注册接口调用失败：" + err);
      }
    },
  },
};
</script>

<style scoped>
.register-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-title {
  color: #333;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  color: #333;
  font-weight: 500;
  font-size: 14px;
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

.form-input::placeholder {
  color: #bfbfbf;
}

.form-select {
  appearance: none;
  background: white
    url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='%23999' d='M5.5 7.5L10 12l4.5-4.5H5.5z'/%3E%3C/svg%3E")
    no-repeat right 12px center;
  background-size: 16px;
  padding-right: 40px;
}

.register-actions {
  margin-top: 10px;
}

.register-btn {
  width: 100%;
  padding: 12px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  box-sizing: border-box;
  background: #1890ff;
  color: white;
}

.register-btn:hover {
  background: #096dd9;
}

/* 回到登录链接 */
.back-to-login {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.back-to-login a {
  color: #1890ff;
  text-decoration: none;
  font-size: 14px;
}

.back-to-login a:hover {
  text-decoration: underline;
}
</style>
