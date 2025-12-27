import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import App from "./App.vue";
import router from "./router";
import "./assets/css/global.css";

createApp(App).use(router).mount("#app");
app.use(ElementPlus);
