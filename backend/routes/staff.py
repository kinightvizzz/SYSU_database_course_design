
from flask import Blueprint, jsonify, request
from extensions import get_db_connection
import  pymysql
staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/staff/orders", methods=["GET"])
def staff_orders():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_query_orders_brief")
            orders = cursor.fetchall()
    finally:
        conn.close()

    return jsonify({
        "code": 0,
        "msg": "success",
        "data": orders
    })
@staff_bp.route("/staff/orders/ship", methods=["POST"])
def ship_order():
    data = request.get_json()
    order_id = data.get("order_id")
    staff_id = data.get("staff_id")

    if not all([order_id, staff_id]):
        return jsonify({"code":1,"msg":"missing parameters"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_ship_order", (order_id, staff_id))
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"code":1,"msg":str(e)}), 400
    finally:
        conn.close()

    return jsonify({"code":0,"msg":"order shipped"})
