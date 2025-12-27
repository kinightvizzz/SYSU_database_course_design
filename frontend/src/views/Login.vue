<template>
  <div class="login-page">
    <div class="login-container custom-card">
      <div class="login-header">
        <h2 class="login-title">用户登录</h2>
      </div>

      <div class="login-form">
        <div class="form-group">
          <label>手机号</label>
          <input
            v-model="phone"
            placeholder="请输入手机号"
            class="form-input"
            type="text" />
        </div>

        <div class="form-group">
          <label>密码</label>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            class="form-input" />
        </div>

        <div class="form-group">
          <label>角色</label>
          <select v-model="role" class="form-select">
            <option value="user">普通用户</option>
            <option value="staff">员工</option>
            <option value="admin">管理员</option>
          </select>
        </div>

        <div class="login-actions">
          <button class="login-btn btn-primary" @click="login">登录</button>

          <button class="register-btn" @click="goRegister">去注册</button>
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
      phone: "",
      password: "",
      role: "user",
    };
  },
  methods: {
    async login() {
      console.log("login clicked");
      try {
        const res = await http.post("/login", {
          phone: this.phone,
          password: this.password,
        });

        console.log("login response:", res.data);

        if (res.data.code === 0) {
          localStorage.setItem("username", res.data.username);
          localStorage.setItem("userRole", res.data.role);

          if (res.data.role === "user") {
            localStorage.setItem("userId", res.data.user_id);
            this.$router.push("/user");
          } else {
            localStorage.setItem("staffId", res.data.staff_id);
            this.$router.push(res.data.role === "staff" ? "/staff" : "/admin");
          }
        } else {
          alert(res.data.msg);
        }
      } catch (err) {
        console.error(err);
        alert("登录请求失败");
      }
    },

    goRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  color: #333;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

.login-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

.login-btn,
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
}

.login-btn {
  background: #1890ff;
  color: white;
}

.login-btn:hover {
  background: #096dd9;
}

.register-btn {
  background: white;
  border: 1px solid #d9d9d9;
  color: #666;
}

.register-btn:hover {
  border-color: #1890ff;
  color: #1890ff;
}
</style>
