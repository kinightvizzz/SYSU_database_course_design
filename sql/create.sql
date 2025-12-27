-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS sale_platform CHARSET utf8mb4;
USE sale_platform;

-- 2. 创建表
CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    gender CHAR(1) CHECK (gender IN ('男','女')),
    id_card VARCHAR(18) UNIQUE,
    address VARCHAR(255),
    password VARCHAR(255) DEFAULT '123456'
);

CREATE TABLE Product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    category VARCHAR(50),
    INDEX idx_category (category)
);

CREATE TABLE Staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('客服','仓库','管理员')),
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT '在职',
    password VARCHAR(255) DEFAULT '123456',
    INDEX idx_role (role)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) UNIQUE,
    user_id INT NOT NULL,
    staff_id INT,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(20) DEFAULT '待支付' CHECK (
        order_status IN ('待支付','已支付','已发货','已完成','已取消')
    ),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),

    CONSTRAINT fk_order_user
        FOREIGN KEY (user_id) REFERENCES User(user_id),
    CONSTRAINT fk_order_staff
        FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    
    INDEX idx_user_status (user_id, order_status),
    INDEX idx_order_time (order_time)
);

CREATE TABLE Order_Item (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (quantity * price),

    CONSTRAINT fk_item_order
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_item_product
        FOREIGN KEY (product_id) REFERENCES Product(product_id),
    
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
);

CREATE TABLE Payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL UNIQUE,
    pay_method VARCHAR(20) CHECK (pay_method IN ('微信','支付宝','银行卡')),
    pay_amount DECIMAL(10,2) NOT NULL CHECK (pay_amount >= 0),
    pay_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payment_order
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    
    INDEX idx_pay_time (pay_time)
);

-- 3. 触发器
DELIMITER $$

CREATE TRIGGER generate_order_no
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    DECLARE v_seq INT;
    
    IF NEW.order_no IS NULL THEN
        SELECT COALESCE(MAX(SUBSTRING(order_no, -4)), 0) + 1 INTO v_seq 
        FROM Orders 
        WHERE DATE(order_time) = CURDATE();
        
        SET NEW.order_no = CONCAT('ORD', DATE_FORMAT(NOW(), '%Y%m%d'), LPAD(v_seq, 4, '0'));
    END IF;
END$$

CREATE TRIGGER check_stock_before_update
BEFORE UPDATE ON Product
FOR EACH ROW
BEGIN
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '库存不能为负数';
    END IF;
END$$

DELIMITER ;

-- 4. 存储过程
DELIMITER $$

-- 创建订单
CREATE PROCEDURE sp_create_order (
    IN p_user_id INT,
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_stock INT;
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_order_id INT;
    
    -- 检查库存
    SELECT price, stock INTO v_price, v_stock
    FROM Product
    WHERE product_id = p_product_id;
    
    IF v_stock < p_quantity THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '库存不足';
    END IF;
    
    SET v_total = v_price * p_quantity;
    
    START TRANSACTION;
    
    INSERT INTO Orders(user_id, order_status, total_amount)
    VALUES (p_user_id, '待支付', v_total);
    
    SET v_order_id = LAST_INSERT_ID();
    
    INSERT INTO Order_Item(order_id, product_id, quantity, price)
    VALUES (v_order_id, p_product_id, p_quantity, v_price);
    
    COMMIT;
    
    SELECT v_order_id as order_id;
END$$

-- 查询用户订单
CREATE PROCEDURE sp_query_user_orders (
    IN p_user_id INT
)
BEGIN
    SELECT o.order_id, o.order_no, o.order_time, 
           o.order_status, o.total_amount,
           COUNT(oi.item_id) as item_count
    FROM Orders o
    LEFT JOIN Order_Item oi ON o.order_id = oi.order_id
    WHERE o.user_id = p_user_id
    GROUP BY o.order_id
    ORDER BY o.order_time DESC;
END$$

-- 支付订单
CREATE PROCEDURE sp_pay_order (
    IN p_order_id INT,
    IN p_pay_method VARCHAR(20)
)
BEGIN
    DECLARE v_amount DECIMAL(10,2);
    
    SELECT total_amount INTO v_amount
    FROM Orders
    WHERE order_id = p_order_id AND order_status = '待支付';
    
    IF v_amount IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '订单不存在或状态不正确';
    END IF;
    
    START TRANSACTION;
    
    INSERT INTO Payment(order_id, pay_method, pay_amount)
    VALUES (p_order_id, p_pay_method, v_amount);
    
    UPDATE Orders
    SET order_status = '已支付'
    WHERE order_id = p_order_id;
    
    UPDATE Product p
    JOIN Order_Item oi ON p.product_id = oi.product_id
    SET p.stock = p.stock - oi.quantity
    WHERE oi.order_id = p_order_id;
    
    COMMIT;
END$$

-- 客服查看订单
CREATE PROCEDURE sp_query_orders_brief ()
BEGIN
    SELECT o.order_id, o.order_no, o.order_time,
           u.username, u.phone,
           o.order_status, o.total_amount,
           COUNT(oi.item_id) as item_count
    FROM Orders o
    JOIN User u ON o.user_id = u.user_id
    LEFT JOIN Order_Item oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
    ORDER BY o.order_time DESC;
END$$

-- 发货
CREATE PROCEDURE sp_ship_order (
    IN p_order_id INT,
    IN p_staff_id INT
)
BEGIN
    DECLARE v_status VARCHAR(20);

    SELECT order_status INTO v_status
    FROM Orders
    WHERE order_id = p_order_id;

    IF v_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '订单不存在';
    END IF;

    IF v_status != '已支付' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '当前订单状态不可发货';
    END IF;

    UPDATE Orders
    SET order_status = '已发货',
        staff_id = p_staff_id
    WHERE order_id = p_order_id;
END$$

-- 完成订单
CREATE PROCEDURE sp_complete_order (
    IN p_order_id INT
)
BEGIN
    UPDATE Orders
    SET order_status = '已完成'
    WHERE order_id = p_order_id 
      AND order_status = '已发货';
END$$

-- 取消订单
CREATE PROCEDURE sp_cancel_order (
    IN p_order_id INT
)
BEGIN
    DECLARE v_status VARCHAR(20);
    
    SELECT order_status INTO v_status
    FROM Orders
    WHERE order_id = p_order_id;
    
    IF v_status = '待支付' THEN
        UPDATE Orders
        SET order_status = '已取消'
        WHERE order_id = p_order_id;
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '只能取消待支付的订单';
    END IF;
END$$

-- 按日期统计收入
CREATE PROCEDURE sp_stat_daily_income (
    IN p_date DATE
)
BEGIN
    SELECT DATE(o.order_time) AS stat_date,
           COUNT(o.order_id) AS order_count,
           SUM(o.total_amount) AS total_income
    FROM Orders o
    WHERE DATE(o.order_time) = p_date
      AND o.order_status IN ('已支付','已完成')
    GROUP BY DATE(o.order_time);
END$$

-- 按商品统计销售
CREATE PROCEDURE sp_stat_product_sales ()
BEGIN
    SELECT p.product_id, p.product_name, p.category,
           SUM(oi.quantity) AS total_sold,
           SUM(oi.quantity * oi.price) AS total_income,
           AVG(oi.price) AS avg_price
    FROM Product p
    LEFT JOIN Order_Item oi ON p.product_id = oi.product_id
    LEFT JOIN Orders o ON oi.order_id = o.order_id
    WHERE o.order_status IN ('已支付','已完成') OR o.order_id IS NULL
    GROUP BY p.product_id;
END$$

-- 更新员工信息
CREATE PROCEDURE sp_update_staff (
    IN p_staff_id INT,
    IN p_phone VARCHAR(20),
    IN p_status VARCHAR(20)
)
BEGIN
    UPDATE Staff
    SET phone = p_phone,
        status = p_status
    WHERE staff_id = p_staff_id;
END$$

DELIMITER ;

-- 5. 视图
CREATE VIEW OrderDetail AS
SELECT 
    o.order_id, o.order_no, o.order_time, o.order_status,
    o.total_amount, u.username, u.phone, u.address,
    s.name as staff_name, s.role as staff_role,
    GROUP_CONCAT(CONCAT(p.product_name, '×', oi.quantity)) as products
FROM Orders o
JOIN User u ON o.user_id = u.user_id
LEFT JOIN Staff s ON o.staff_id = s.staff_id
JOIN Order_Item oi ON o.order_id = oi.order_id
JOIN Product p ON oi.product_id = p.product_id
GROUP BY o.order_id;

CREATE VIEW ProductInventory AS
SELECT 
    product_id, product_name, price, stock, category,
    CASE 
        WHEN stock = 0 THEN '缺货'
        WHEN stock < 10 THEN '低库存'
        ELSE '充足'
    END as inventory_status
FROM Product;