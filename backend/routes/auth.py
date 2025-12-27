from flask import Blueprint, request, jsonify
from extensions import get_db_connection
import pymysql

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])


def login():
    data = request.get_json()

    phone = data.get("phone")  # 前端传手机号
    password = data.get("password")

    if not all([phone, password]):
        return jsonify({
            "code": 1,
            "msg": "missing parameters"
        }), 400

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            # 1️⃣ 普通用户按手机号登录
            cursor.execute(
                "SELECT user_id, username FROM User WHERE phone=%s AND password=%s",
                (phone, password)
            )
            user = cursor.fetchone()

            if user:
                return jsonify({
                    "code": 0,
                    "msg": "login success",
                    "role": "user",
                    "user_id": user["user_id"],
                    "username": user["username"]
                })

            # 2️⃣ 员工 / 管理员逻辑保持不变
            cursor.execute(
                "SELECT staff_id, name, role FROM Staff WHERE phone=%s AND password=%s",
                (phone, password)
            )
            staff = cursor.fetchone()

            if staff:
                role_map = {
                    "客服": "staff",
                    "仓库": "staff",
                    "管理员": "admin"
                }
                return jsonify({
                    "code": 0,
                    "msg": "login success",
                    "role": role_map.get(staff["role"], "staff"),
                    "staff_id": staff["staff_id"],
                    "username": staff["name"]
                })

            # 3️⃣ 都查不到
            return jsonify({
                "code": 1,
                "msg": "phone or password incorrect"
            })

    finally:
        conn.close()





@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    phone = data.get("phone")
    gender = data.get("gender")
    id_card = data.get("id_card", "")
    address = data.get("address", "")
    password = data.get("password")

    # 参数校验
    if not all([username, phone, gender, password]):
        return jsonify({"code": 1, "msg": "缺少必要参数"}), 400

    if gender not in ["男", "女"]:
        return jsonify({"code": 1, "msg": "性别只能为 男 或 女"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 检查手机号或身份证是否已存在
            cursor.execute("SELECT user_id FROM User WHERE phone=%s OR id_card=%s", (phone, id_card))
            if cursor.fetchone():
                return jsonify({"code": 1, "msg": "手机号或身份证已注册"}), 400

            # 插入新用户
            sql = """
                INSERT INTO User (username, phone, gender, id_card, address, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (username, phone, gender, id_card, address, password))
        conn.commit()
        return jsonify({"code": 0, "msg": "注册成功"})
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"code": 1, "msg": f"数据库错误: {str(e)}"}), 500
    finally:
        conn.close()





@auth_bp.route("/update", methods=["POST"])
def update_user():


    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"code": 1, "msg": "user_id is required"}), 400

    # 构建更新字段
    fields = {}
    for key in ["username", "password", "phone", "gender", "id_card", "address"]:
        if key in data:
            fields[key] = data[key]

    if not fields:
        return jsonify({"code": 1, "msg": "no fields to update"}), 400

    set_clause = ", ".join(f"{k}=%s" for k in fields.keys())
    values = list(fields.values())
    values.append(user_id)  # 最后是 WHERE user_id=?

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = f"UPDATE User SET {set_clause} WHERE user_id=%s"
            cursor.execute(sql, values)
        conn.commit()
        return jsonify({"code": 0, "msg": "update success"})
    except pymysql.MySQLError as e:
        conn.rollback()
        return jsonify({"code": 1, "msg": str(e)}), 400
    finally:
        conn.close()






# 查询用户信息接口
@auth_bp.route("/info", methods=["GET"])
def get_user_info():
    """
    查询用户信息
    前端请求参数：
      - user_id (必须)
    返回：
      - 用户完整信息
    """
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"code": 1, "msg": "user_id is required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT user_id, username, phone, gender, id_card, address FROM User WHERE user_id=%s",
                           (user_id,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"code": 1, "msg": "user not found"}), 404

            return jsonify({"code": 0, "msg": "success", "data": user})
    finally:
        conn.close()
