from flask import Flask
from routes.product import product_bp
from routes.order import order_bp
from routes.staff import staff_bp
from routes.admin import admin_bp
from routes.auth import auth_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求




app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
@app.route("/")
def index():
    return "Sale Platform Backend Running"

if __name__ == "__main__":
    app.run(debug=True)
