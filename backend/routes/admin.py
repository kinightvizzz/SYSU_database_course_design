from flask import Blueprint, request, jsonify
from extensions import get_db_connection
import pymysql

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/daily-income", methods=["GET"])
def daily_income():
    date = request.args.get("date")
    if not date:
        return jsonify({"code":1,"msg":"missing date"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_stat_daily_income", (date,))
            result = cursor.fetchall()
    finally:
        conn.close()

    return jsonify({"code":0,"msg":"success","data":result})

@admin_bp.route("/admin/product-sales", methods=["GET"])
def product_sales():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_stat_product_sales")
            result = cursor.fetchall()
    finally:
        conn.close()

    return jsonify({"code":0,"msg":"success","data":result})
@admin_bp.route("/admin/staff/update", methods=["POST"])
def update_staff():
    data = request.get_json()
    staff_id = data.get("staff_id")
    phone = data.get("phone")
    status = data.get("status")

    if not all([staff_id, phone, status]):
        return jsonify({"code":1,"msg":"missing parameters"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_update_staff", (staff_id, phone, status))
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"code":1,"msg":str(e)}), 400
    finally:
        conn.close()

    return jsonify({"code":0,"msg":"staff updated"})

@admin_bp.route("/admin/products", methods=["GET"])
def admin_get_products():
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    product_id,
                    product_name,
                    price,
                    stock,
                    category
                FROM Product
                ORDER BY product_id DESC
            """)
            products = cursor.fetchall()

        return jsonify({
            "code": 0,
            "msg": "success",
            "data": products
        })

    finally:
        conn.close()
@admin_bp.route("/admin/products/<int:product_id>", methods=["PUT"])
def admin_update_product(product_id):
    data = request.get_json()

    product_name = data.get("product_name")
    price = data.get("price")
    stock = data.get("stock")
    category = data.get("category")

    # 至少更新一个字段
    if all(v is None for v in [product_name, price, stock, category]):
        return jsonify({
            "code": 1,
            "msg": "no fields to update"
        }), 400

    fields = []
    values = []

    if product_name is not None:
        fields.append("product_name=%s")
        values.append(product_name)

    if price is not None:
        fields.append("price=%s")
        values.append(price)

    if stock is not None:
        fields.append("stock=%s")
        values.append(stock)

    if category is not None:
        fields.append("category=%s")
        values.append(category)

    values.append(product_id)

    sql = f"""
        UPDATE Product
        SET {', '.join(fields)}
        WHERE product_id = %s
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)

        conn.commit()

        return jsonify({
            "code": 0,
            "msg": "product updated"
        })

    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({
            "code": 1,
            "msg": str(e)
        }), 400

    finally:
        conn.close()

# 新增商品接口
@admin_bp.route("/admin/products/add", methods=["POST"])
def add_product():
    data = request.get_json()
    product_name = data.get("product_name")
    price = data.get("price")
    stock = data.get("stock")
    category = data.get("category", "")

    if not all([product_name, price is not None, stock is not None]):
        return jsonify({"code": 1, "msg": "缺少必要参数"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO Product (product_name, price, stock, category)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (product_name, price, stock, category))
        conn.commit()

        return jsonify({"code": 0, "msg": "新增商品成功"})
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"code": 1, "msg": f"数据库错误: {str(e)}"}), 500
    finally:
        conn.close()

