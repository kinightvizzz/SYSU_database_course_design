from flask import Blueprint, request, jsonify
from extensions import get_db_connection
import pymysql

order_bp = Blueprint("order", __name__)

@order_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not all([user_id, product_id, quantity]):
        return jsonify({"code": 1, "msg": "missing parameters"}), 400

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 调用存储过程：sp_create_order
            cursor.callproc("sp_create_order", (user_id, product_id, quantity))
            result = cursor.fetchone()
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({
            "code": 1,
            "msg": str(e)
        }), 400
    finally:
        conn.close()

    return jsonify({
        "code": 0,
        "msg": "order created",
        "order_id": result["order_id"]
    })
@order_bp.route("/orders/user", methods=["GET"])
def get_user_orders():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"code": 1, "msg": "missing user_id"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 调用存储过程：查询用户订单
            cursor.callproc("sp_query_user_orders", (user_id,))
            orders = cursor.fetchall()
    finally:
        conn.close()

    return jsonify({
        "code": 0,
        "msg": "success",
        "data": orders
    })
@order_bp.route("/orders/pay", methods=["POST"])
def pay_order():
    data = request.get_json()
    order_id = data.get("order_id")
    pay_method = data.get("pay_method")

    if not all([order_id, pay_method]):
        return jsonify({"code":1,"msg":"missing parameters"}),400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 调用存储过程 sp_pay_order
            cursor.callproc("sp_pay_order", (order_id, pay_method))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"code":1,"msg":str(e)}),400
    finally:
        conn.close()

    return jsonify({"code":0,"msg":"payment success"})
@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def order_detail(order_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 订单基本信息
            cursor.execute("""
                SELECT order_id, order_no, order_status, total_amount, order_time
                FROM Orders
                WHERE order_id = %s
            """, (order_id,))
            order = cursor.fetchone()

            if not order:
                return jsonify({"code":1,"msg":"order not found"}), 404

            # 商品明细
            cursor.execute("""
                SELECT p.product_name, oi.quantity, oi.price, oi.subtotal
                FROM Order_Item oi
                JOIN Product p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
            """, (order_id,))
            items = cursor.fetchall()

    finally:
        conn.close()

    return jsonify({
        "code": 0,
        "msg": "success",
        "data": {
            "order": order,
            "items": items
        }
    })


# =========================
# 取消订单（用户）
# =========================
@order_bp.route("/orders/cancel", methods=["POST"])
def cancel_order():
    data = request.get_json()
    order_id = data.get("order_id")

    if not order_id:
        return jsonify({
            "code": 1,
            "msg": "order_id is required"
        }), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 调用存储过程
            cursor.callproc("sp_cancel_order", (order_id,))
        conn.commit()

        return jsonify({
            "code": 0,
            "msg": "订单已取消"
        })

    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({
            "code": 1,
            "msg": str(e)
        }), 400

    finally:
        conn.close()


