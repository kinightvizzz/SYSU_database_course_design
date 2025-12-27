from flask import Blueprint, jsonify
from extensions import get_db_connection

product_bp = Blueprint("product", __name__)

@product_bp.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = """
        SELECT product_id, product_name, price, stock, category
        FROM Product
        """
        cursor.execute(sql)
        products = cursor.fetchall()
    conn.close()

    return jsonify({
        "code": 0,
        "msg": "success",
        "data": products
    })
